# luminai CLI — README

This document explains the `luminai` CLI (Typer) entrypoints and common workflows for local development and CI integration.

Quick commands

- `luminai config init` — create `~/.luminai/config.toml` interactive config
- `luminai build avatar --manifest path/to/character.json` — run Avatar Forge build for a character bundle
- `luminai serve --env dev` — orchestrate local services for quick testing
- `luminai deploy --target staging` — trigger CI/CD deployment via API

Usage notes

- The CLI reads `LUMINAI_API_KEY` from environment when available; otherwise uses `~/.luminai/config.toml`.
- For local development, run the CLI in an activated virtualenv to ensure dependencies are isolated.

Example (PowerShell)

```pwsh
& .\.venv\Scripts\Activate.ps1
luminai config init
luminai build avatar --manifest docs/personas/miko_exet/character.json
```

Extending the CLI

- New commands should be added under the Python package `luminai` using Typer and include unit tests under `tests/`.

See `docs/deployment/UNIFIED_PLATFORM_BUILD.md` for integration patterns and orchestration examples.
