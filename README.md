# OpenShift Docs for AI Agents

Automated pipeline that converts [Red Hat OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/) documentation into clean, AI-agent-friendly GitHub-Flavored Markdown.

## The Problem

OpenShift documentation at `docs.redhat.com` is JavaScript-rendered — when any HTTP client (including AI agents) fetches a page, it returns only CSS/JS scaffolding with **zero actual documentation content**. The [source repo](https://github.com/openshift/openshift-docs) uses AsciiDoc with heavy `include::` directives, attribute substitution, and conditional blocks that require the full AsciiBinder toolchain to resolve.

Neither format is usable by AI agents.

## Usage with AI Agents

Point your agent to the hosted docs index and ask your question:

```
Based on OpenShift docs hosted here
https://github.com/harche/openshift-docs-md/blob/main/docs/AGENTS.md,
can you find out the CLI options for the opm command in OpenShift 4.21?
```

<img width="3466" height="1502" alt="image" src="https://github.com/user-attachments/assets/8246301a-9097-4ba4-a01c-c1cd9cb9afdc" />


The agent will read `AGENTS.md`, navigate to the right version and topic file, and answer from the actual documentation.

## What This Does

1. Clones the [openshift/openshift-docs](https://github.com/openshift/openshift-docs) source repo
2. Auto-discovers the latest N version branches from `_distro_map.yml`
3. Converts each version: AsciiDoc → DocBook XML (asciidoctor) → GitHub-Flavored Markdown (pandoc)
4. Generates per-version and top-level navigation indexes for both humans and AI agents
5. Publishes all versions to GitHub Pages — updated weekly via GitHub Actions

## Output

The pipeline converts multiple versions and organizes them under a single `docs/` directory:

```
docs/
├── index.md              # Top-level version selector
├── index.html            # HTML version selector
├── AGENTS.md             # Points to version-specific AGENTS.md files
├── viewer.html           # Shared markdown viewer
├── 4.22/
│   ├── index.md          # Version-specific table of contents
│   ├── index.html        # Version-specific HTML navigation
│   ├── AGENTS.md         # Version-specific compressed index
│   ├── viewer.html       # Version-specific markdown viewer
│   └── <topic_dir>/
│       └── <file>.md
├── 4.21/
│   └── ...
└── 4.20/
    └── ...
```

Each version directory contains the same four navigation aids:

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

### Run — Full Multi-Version Conversion

Convert the latest 3 versions in one go (same as CI):

```bash
pip install -r requirements.txt
git clone --depth 1 https://github.com/openshift/openshift-docs.git

# Discover versions, convert each, generate top-level index
VERSIONS=$(python convert.py --source-dir ./openshift-docs --discover-versions 3)
rm -rf ./docs && mkdir -p ./docs
for row in $(echo "$VERSIONS" | jq -c '.[]'); do
  VERSION=$(echo "$row" | jq -r '.version')
  BRANCH=$(echo "$row" | jq -r '.branch')
  cd openshift-docs && git fetch --depth 1 origin "$BRANCH" && git checkout FETCH_HEAD && cd ..
  python convert.py --source-dir ./openshift-docs --output-dir "./docs/$VERSION" \
    --distro openshift-enterprise --branch "$BRANCH" --workers 4
done
python convert.py --output-dir ./docs --generate-top-index
```

### Run — Single Version

```bash
pip install -r requirements.txt
git clone --depth 1 --branch enterprise-4.22 \
  https://github.com/openshift/openshift-docs.git

python convert.py --source-dir ./openshift-docs --output-dir ./docs/4.22 \
  --branch enterprise-4.22

# Convert specific topics only
python convert.py --source-dir ./openshift-docs --output-dir ./docs/4.22 \
  --branch enterprise-4.22 --topics welcome,installing,networking
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--source-dir` | *(required for conversion)* | Path to cloned openshift-docs repo |
| `--output-dir` | `./docs` | Output directory for markdown files |
| `--distro` | `openshift-enterprise` | Target distro |
| `--branch` | `main` | Source branch for version attributes |
| `--topic-map` | `_topic_map.yml` | Topic map file name |
| `--topics` | *(all)* | Comma-separated topic dirs to convert |
| `--workers` | `4` | Number of parallel workers |
| `--discover-versions` | | Print latest N version branches as JSON and exit |
| `--generate-top-index` | | Generate top-level index from version subdirectories and exit |

## CI/CD

A GitHub Actions workflow runs every Monday at 6:00 AM UTC. It auto-discovers the latest 3 versions from `_distro_map.yml`, converts each version into its own subdirectory, generates a top-level version selector, and deploys everything to GitHub Pages. It can also be triggered manually with custom distro, version count, and topic parameters.

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
