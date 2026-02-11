# OpenShift Docs Markdown Converter

## What This Is

Automated pipeline that converts Red Hat OpenShift AsciiDoc documentation into
clean GitHub-Flavored Markdown for AI agent consumption. The source docs at
`docs.redhat.com` are JavaScript-rendered and return no content to HTTP clients.
This project solves that.

## Pipeline

AsciiDoc → DocBook XML (asciidoctor) → Markdown (pandoc) → post-processing

## Key Files

- `convert.py` — Main conversion script. All logic lives here.
- `requirements.txt` — Python deps (pyyaml)
- `.github/workflows/convert.yml` — Weekly CI, deploys to GitHub Pages
- `openshift-docs/` — Cloned source repo (gitignored)
- `docs/` — Generated output (gitignored)

## Running Locally

```bash
# Prerequisites: python 3.12+, asciidoctor (ruby), pandoc
pip install -r requirements.txt
git clone --depth 1 https://github.com/openshift/openshift-docs.git

# Discover latest 3 versions
python convert.py --source-dir ./openshift-docs --discover-versions 3

# Convert a single version into a versioned subdirectory
python convert.py --source-dir ./openshift-docs --output-dir ./docs/4.22 \
  --branch enterprise-4.22

# Generate top-level version selector index
python convert.py --output-dir ./docs --generate-top-index

# Convert specific topics only
python convert.py --source-dir ./openshift-docs --output-dir ./docs/4.22 \
  --branch enterprise-4.22 --topics welcome,installing,networking
```

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--source-dir` | (required for conversion) | Path to cloned openshift-docs repo |
| `--output-dir` | `./docs` | Output directory for Markdown files |
| `--distro` | `openshift-enterprise` | Target distro (openshift-enterprise, openshift-origin, openshift-webscale, openshift-online) |
| `--branch` | `main` | Source branch for version attributes |
| `--topic-map` | `_topic_map.yml` | Topic map file name |
| `--topics` | (all) | Comma-separated topic dirs to convert |
| `--workers` | `4` | Number of parallel workers |
| `--discover-versions N` | | Print latest N version branches as JSON and exit |
| `--generate-top-index` | | Generate top-level index from version subdirectories and exit |

## Output Structure

```
docs/
├── index.md              # Top-level version selector
├── index.html            # HTML version selector
├── AGENTS.md             # Points to version-specific AGENTS.md
├── viewer.html           # Shared markdown viewer
├── 4.22/
│   ├── index.md          # Version-specific ToC
│   ├── index.html        # Version-specific HTML nav
│   ├── AGENTS.md         # Version-specific compressed index
│   ├── viewer.html       # Version-specific markdown viewer
│   └── <topic_dir>/
│       └── <file>.md
├── 4.21/
│   └── ...
└── 4.20/
    └── ...
```

## Generated Index Files

Per-version directories each contain four navigation aids:
- `index.md` — Full table of contents with markdown links
- `index.html` — Static HTML linking to viewer.html for human browsing
- `viewer.html` — Renders raw .md files client-side via marked.js
- `AGENTS.md` — Compressed documentation index for AI agents (pipe-delimited format)

Top-level index files provide a version selector:
- `index.md` — Links to each version's index.md
- `index.html` — HTML version selector
- `AGENTS.md` — Points agents to version-specific AGENTS.md files

## Configuration Sources

- `_distro_map.yml` — Product definitions and version branches
- `_topic_maps/_topic_map.yml` — Navigation hierarchy (OCP)
- `_topic_maps/_topic_map_rosa.yml` — ROSA variant
- `_topic_maps/_topic_map_osd.yml` — OpenShift Dedicated variant
- `_attributes/common-attributes.adoc` — Shared AsciiDoc variables

## Code Conventions

- Single file, no abstractions — all logic in `convert.py`
- `ProcessPoolExecutor` for parallel conversion
- Post-processing cleans pandoc artifacts (empty divs, class annotations, admonition formatting)
- XML sanitization fixes known asciidoctor DocBook bugs before pandoc conversion
