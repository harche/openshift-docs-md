#!/usr/bin/env python3
"""
Convert OpenShift AsciiDoc documentation to GitHub-Flavored Markdown.

Usage:
    python convert.py --source-dir ./openshift-docs --output-dir ./docs
    python convert.py --source-dir ./openshift-docs --output-dir ./docs --distro openshift-enterprise
    python convert.py --source-dir ./openshift-docs --output-dir ./docs --topics welcome,installing
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import yaml


def parse_distro_map(source_dir: str) -> dict:
    """Parse _distro_map.yml to get product attributes per distro."""
    distro_path = Path(source_dir) / "_distro_map.yml"
    with open(distro_path) as f:
        return yaml.safe_load(f)


def parse_topic_map(source_dir: str, topic_map_file: str = "_topic_map.yml") -> list:
    """Parse _topic_maps/_topic_map.yml to get the doc hierarchy."""
    # The topic map uses --- as record delimiter (multi-document YAML)
    topic_map_path = Path(source_dir) / "_topic_maps" / topic_map_file
    with open(topic_map_path) as f:
        return list(yaml.safe_load_all(f))


def get_distro_attributes(distro_map: dict, distro: str, branch: str = "main") -> dict:
    """Extract product attributes for a given distro and branch."""
    distro_config = distro_map.get(distro, {})
    branches = distro_config.get("branches", {})
    branch_config = branches.get(branch, {})

    return {
        "product-title": distro_config.get("name", "OpenShift Container Platform"),
        "product-version": branch_config.get("name", "4.17"),
        distro: "",  # Set the distro flag (e.g., openshift-enterprise=)
    }


def should_include_topic(topic: dict, distro: str) -> bool:
    """Check if a topic should be included for the target distro."""
    distros = topic.get("Distros", "")
    if not distros:
        return True  # No distro filter = include everywhere
    return distro in distros.split(",")


def convert_file(
    source_file: str,
    dest_file: str,
    attributes: dict,
    source_dir: str,
) -> tuple[bool, str, str]:
    """Convert a single AsciiDoc file to Markdown via DocBook intermediate."""
    source_path = Path(source_file)
    dest_path = Path(dest_file)

    if not source_path.exists():
        return False, str(source_path), f"Source file not found: {source_path}"

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        tmp_xml = tmp.name

    try:
        # Step 1: AsciiDoc → DocBook via asciidoctor
        cmd_asciidoctor = [
            "asciidoctor",
            "-b", "docbook5",
            "--safe-mode", "unsafe",
            "-o", tmp_xml,
        ]
        # Add attributes
        for key, value in attributes.items():
            if value:
                cmd_asciidoctor.extend(["-a", f"{key}={value}"])
            else:
                cmd_asciidoctor.extend(["-a", key])

        cmd_asciidoctor.append(str(source_path))

        result = subprocess.run(
            cmd_asciidoctor,
            capture_output=True,
            text=True,
            cwd=source_dir,
            timeout=60,
        )

        if result.returncode != 0:
            return False, str(source_path), f"asciidoctor error: {result.stderr}"

        # Step 2: DocBook → GFM Markdown via pandoc
        cmd_pandoc = [
            "pandoc",
            "-f", "docbook",
            "-t", "gfm",
            "--wrap=none",
            "-o", str(dest_path),
            tmp_xml,
        ]

        result = subprocess.run(
            cmd_pandoc,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            return False, str(source_path), f"pandoc error: {result.stderr}"

        # Step 3: Post-process the markdown
        content = dest_path.read_text()
        content = post_process_markdown(content)
        dest_path.write_text(content)

        return True, str(source_path), "OK"

    finally:
        if os.path.exists(tmp_xml):
            os.unlink(tmp_xml)


def post_process_markdown(content: str) -> str:
    """Clean up pandoc output artifacts."""
    # Remove empty anchor divs that pandoc sometimes generates
    content = re.sub(r'<div id="[^"]*">\s*</div>\n?', "", content)

    # Clean up excessive blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Fix admonition blocks (NOTE, WARNING, IMPORTANT, TIP, CAUTION)
    for admonition in ["Note", "Warning", "Important", "Tip", "Caution"]:
        content = re.sub(
            rf"\*\*{admonition}\*\*\n\n",
            f"> **{admonition}**: ",
            content,
        )

    # Remove {.title} class annotations pandoc may leave
    content = re.sub(r'\{\.[\w-]+\}', '', content)

    # Strip trailing whitespace
    content = "\n".join(line.rstrip() for line in content.splitlines())

    return content.strip() + "\n"


def collect_topics(
    topics: list,
    base_dir: str,
    distro: str,
) -> list[dict]:
    """Recursively collect all topic files from the topic map."""
    result = []

    for topic in topics:
        if topic is None:
            continue
        if not should_include_topic(topic, distro):
            continue

        sub_topics = topic.get("Topics", [])
        topic_dir = topic.get("Dir", "")
        topic_file = topic.get("File", "")

        current_dir = os.path.join(base_dir, topic_dir) if topic_dir else base_dir

        if topic_file:
            result.append({
                "name": topic.get("Name", ""),
                "file": topic_file,
                "dir": current_dir,
                "source": os.path.join(current_dir, f"{topic_file}.adoc"),
            })

        if sub_topics:
            result.extend(collect_topics(sub_topics, current_dir, distro))

    return result


def generate_index(topic_groups: list, output_dir: str, distro: str) -> None:
    """Generate a navigation index.md from the topic map."""
    index_path = Path(output_dir) / "index.md"
    lines = [
        "# OpenShift Container Platform Documentation",
        "",
        "> Auto-generated Markdown conversion of [openshift/openshift-docs]"
        "(https://github.com/openshift/openshift-docs).",
        "> Designed for AI agent consumption. Updated weekly.",
        "",
        "## Table of Contents",
        "",
    ]

    def render_topics(topics, base_path, indent=0):
        for topic in topics:
            if topic is None:
                continue
            if not should_include_topic(topic, distro):
                continue

            name = topic.get("Name", "Untitled")
            topic_dir = topic.get("Dir", "")
            topic_file = topic.get("File", "")
            sub_topics = topic.get("Topics", [])

            current_path = f"{base_path}/{topic_dir}" if topic_dir else base_path
            prefix = "  " * indent

            if topic_file:
                link = f"{current_path}/{topic_file}.md"
                lines.append(f"{prefix}- [{name}]({link})")
            elif topic_dir:
                lines.append(f"{prefix}- **{name}**")

            if sub_topics:
                render_topics(sub_topics, current_path, indent + 1)

    for group in topic_groups:
        if group is None:
            continue
        if not should_include_topic(group, distro):
            continue

        name = group.get("Name", "Untitled")
        group_dir = group.get("Dir", "")
        sub_topics = group.get("Topics", [])

        lines.append(f"### {name}")
        lines.append("")

        if sub_topics:
            render_topics(sub_topics, group_dir, 0)

        lines.append("")

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert OpenShift AsciiDoc docs to Markdown"
    )
    parser.add_argument(
        "--source-dir",
        required=True,
        help="Path to cloned openshift-docs repo",
    )
    parser.add_argument(
        "--output-dir",
        default="./docs",
        help="Output directory for Markdown files",
    )
    parser.add_argument(
        "--distro",
        default="openshift-enterprise",
        help="Target distro (default: openshift-enterprise)",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Source branch (for version attributes)",
    )
    parser.add_argument(
        "--topic-map",
        default="_topic_map.yml",
        help="Topic map file name (default: _topic_map.yml)",
    )
    parser.add_argument(
        "--topics",
        default="",
        help="Comma-separated list of topic dirs to convert (empty = all)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source_dir)
    output_dir = os.path.abspath(args.output_dir)

    # Verify tools are available
    for tool in ["asciidoctor", "pandoc"]:
        if shutil.which(tool) is None:
            print(f"Error: '{tool}' not found in PATH. Please install it.")
            sys.exit(1)

    # Parse configuration
    print("Parsing distro map...")
    distro_map = parse_distro_map(source_dir)
    attributes = get_distro_attributes(distro_map, args.distro, args.branch)

    print("Parsing topic map...")
    topic_groups = parse_topic_map(source_dir, args.topic_map)

    # Filter to specific topics if requested
    filter_topics = set(args.topics.split(",")) if args.topics else None

    if filter_topics:
        topic_groups = [
            g for g in topic_groups
            if g and g.get("Dir", "") in filter_topics
        ]

    # Collect all files to convert
    all_topics = []
    for group in topic_groups:
        if group is None:
            continue
        if not should_include_topic(group, args.distro):
            continue
        group_dir = group.get("Dir", "")
        sub_topics = group.get("Topics", [])
        if sub_topics:
            all_topics.extend(collect_topics(sub_topics, group_dir, args.distro))

    print(f"Found {len(all_topics)} topics to convert")

    # Clean output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Convert files in parallel
    successes = 0
    failures = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for topic in all_topics:
            src = os.path.join(source_dir, topic["source"])
            dest = os.path.join(
                output_dir, topic["dir"], f"{topic['file']}.md"
            )
            future = executor.submit(
                convert_file, src, dest, attributes, source_dir
            )
            futures[future] = topic

        for future in as_completed(futures):
            topic = futures[future]
            success, path, message = future.result()
            if success:
                successes += 1
            else:
                failures += 1
                print(f"  FAIL: {path} — {message}")

    print(f"\nConversion complete: {successes} succeeded, {failures} failed")

    # Generate navigation index
    print("Generating index...")
    generate_index(topic_groups, output_dir, args.distro)

    print(f"Output written to {output_dir}/")


if __name__ == "__main__":
    main()
