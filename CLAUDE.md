# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- `mkdocs serve` — Start dev server with live reload at http://127.0.0.1:8000
- `mkdocs build` — Build static site into `site/` directory
- `mkdocs gh-deploy` — Deploy built site to `gh-pages` branch on GitHub

## Dependencies

- Python package: `mkdocs` (v1.6.1), `mkdocs-material` (v9.7.6)
- No `requirements.txt` exists — install with `pip install mkdocs mkdocs-material`

## Architecture

- **`mkdocs.yml`** — Site configuration; defines nav, extra CSS, and Markdown extensions
- **`docs/`** — Source markdown files that make up the site content
  - `index.md` — Homepage
  - `notes/markdown-syntax-basic.md` — Basic Markdown syntax tutorial
  - `notes/markdown-syntax-extended.md` — Extended syntax tutorial (tables, fenced code, etc.)
  - `作品集.md` — Portfolio page (placeholder)
  - `styles/custom.css` — Custom CSS for admonitions/alerts and typography
  - `images/` — Images used in docs
- **`site/`** — Generated output from `mkdocs build` (not gitignored — should be added to `.gitignore`)
- **`basics-bold.litcoffee`** — Standalone Literate CoffeeScript snippet (not part of the MkDocs site)

## Markdown Extensions Enabled

- Admonitions (`!!!note`, `!!!example`, `!!!tip`)
- Tables, fenced code blocks with syntax highlighting
- Strikethrough/subscript (`pymdownx.tilde`)
- Superscript (`pymdownx.caret`)
- Highlight (`pymdownx.mark`)
- Task lists with custom checkboxes
- Emoji via Twemoji (`pymdownx.emoji`)
- Definition lists (`def_list`)

## Notes

- No `.gitignore` exists — `site/` and other generated files will be tracked by git unless ignored
- Project pages site deployed via GitHub Pages (`gh-pages` branch)
- Author: Jiaying (<sisuzanel@163.com>)
