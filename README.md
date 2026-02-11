# OpenShift Docs → Markdown

Automated pipeline that converts [Red Hat OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/) documentation into clean, AI-agent-friendly GitHub-Flavored Markdown.

## The Problem

OpenShift documentation at `docs.redhat.com` is JavaScript-rendered — when any HTTP client (including AI agents) fetches a page, it returns only CSS/JS scaffolding with **zero actual documentation content**. The [source repo](https://github.com/openshift/openshift-docs) uses AsciiDoc with heavy `include::` directives, attribute substitution, and conditional blocks that require the full AsciiBinder toolchain to resolve.

Neither format is usable by AI agents.

## What This Does

1. Clones the [openshift/openshift-docs](https://github.com/openshift/openshift-docs) source repo
2. Converts AsciiDoc → DocBook XML (asciidoctor) → GitHub-Flavored Markdown (pandoc)
3. Generates navigation indexes for both humans and AI agents
4. Publishes to GitHub Pages — updated weekly via GitHub Actions

## Output

The conversion produces four navigation aids alongside the markdown files:

| File | Purpose |
|------|---------|
| `index.md` | Full table of contents with markdown links |
| `index.html` | Human-browseable HTML navigation |
| `viewer.html` | Client-side markdown renderer (marked.js) |
| `AGENTS.md` | Compressed pipe-delimited index for AI agents |

### AGENTS.md

The `AGENTS.md` file is a compressed, pointer-based documentation index designed for AI agent consumption. Instead of embedding full documentation, it maps every section to its files using a pipe-delimited format:

```
|networking/network_security:{network-policy-apis.md,configuring-ipsec-ovn.md,...}
|storage/container_storage_interface:{persistent-storage-csi.md,persistent-storage-csi-ebs.md,...}
```

This approach is based on Vercel's research showing that [AGENTS.md outperforms skills in agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals). Key design choices:

- **Pointer-based, not content-embedded** — keeps the index small (~70KB for 1,700+ docs) while letting agents retrieve specific files on demand
- **Retrieval-led reasoning** — instructs agents to read referenced files rather than relying on potentially outdated training data
- **Existence-verified** — only indexes files that were actually generated, so agents never reference missing docs

## Supported Distros

| Distro | Flag |
|--------|------|
| OpenShift Container Platform | `openshift-enterprise` (default) |
| OKD | `openshift-origin` |
| ROSA | `openshift-webscale` |
| OpenShift Dedicated | `openshift-online` |

## Quick Start

### Prerequisites

- Python 3.12+
- [asciidoctor](https://asciidoctor.org/) (Ruby)
- [pandoc](https://pandoc.org/)

### Run

```bash
pip install -r requirements.txt
git clone --depth 1 https://github.com/openshift/openshift-docs.git

# Convert all topics
python convert.py --source-dir ./openshift-docs --output-dir ./docs

# Convert specific topics
python convert.py --source-dir ./openshift-docs --output-dir ./docs \
  --topics welcome,installing,networking

# Target a different distro or branch
python convert.py --source-dir ./openshift-docs --output-dir ./docs \
  --distro openshift-origin --branch enterprise-4.18
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--source-dir` | *(required)* | Path to cloned openshift-docs repo |
| `--output-dir` | `./docs` | Output directory for markdown files |
| `--distro` | `openshift-enterprise` | Target distro |
| `--branch` | `main` | Source branch for version attributes |
| `--topic-map` | `_topic_map.yml` | Topic map file name |
| `--topics` | *(all)* | Comma-separated topic dirs to convert |
| `--workers` | `4` | Number of parallel workers |

## CI/CD

A GitHub Actions workflow runs every Monday at 6:00 AM UTC, converting the latest docs and deploying to GitHub Pages. It can also be triggered manually with custom branch, distro, and topic parameters.

## How It Works

```
AsciiDoc (.adoc)
    │
    ▼
DocBook XML (asciidoctor resolves includes, attributes, conditionals)
    │
    ▼
XML sanitization (fixes known asciidoctor bugs)
    │
    ▼
GitHub-Flavored Markdown (pandoc)
    │
    ▼
Post-processing (clean up admonitions, empty divs, pandoc artifacts)
    │
    ▼
Navigation indexes (index.md, index.html, viewer.html, AGENTS.md)
```
