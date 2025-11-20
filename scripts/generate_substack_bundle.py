#!/usr/bin/env python3
"""Generate Substack-ready Markdown posts from persona/docs content.

This script is intentionally conservative: it only writes files when not in
--dry-run mode. It looks for markdown files in `docs/llm-onboarding/` and
exports those that look like persona documents into `docs/substack/output/`.

Features:
 - Heuristic detection of persona docs (filename or content contains "persona").
 - Preserves existing YAML front-matter; adds a default block when missing.
 - Writes into a slugified filename under `docs/substack/output/`.
"""
from pathlib import Path
import argparse
import datetime
import re

ROOT = Path(__file__).resolve().parent.parent
LLM_ONBOARDING = ROOT / "docs" / "llm-onboarding"
OUT_DIR_DEFAULT = ROOT / "docs" / "substack" / "output"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def looks_like_persona(text: str, filename: str) -> bool:
    """Simple heuristics to decide whether a markdown file is a persona doc.

    This is intentionally permissive; the goal is to capture candidate files
    for human review, not to be perfectly precise.
    """
    fn = filename.lower()
    if "persona" in fn or "personas" in fn:
        return True
    head = text[:2048].lower()
    keywords = ["persona", "persona:", "personas", "approvers:", "persona-id"]
    for k in keywords:
        if k in head:
            return True
    return False


def has_front_matter(text: str) -> bool:
    return text.lstrip().startswith("---")


def ensure_front_matter(text: str, title: str, persona: str = None) -> str:
    if has_front_matter(text):
        return text
    date = datetime.date.today().isoformat()
    fm = {
        "title": title,
        "date": date,
        "author": "LuminAI Codex",
        "tags": ["persona", "substack"],
    }
    if persona:
        fm["persona"] = persona
    fm["approvers"] = ["Airth"]
    yaml_lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            yaml_lines.append(f"{k}:")
            for item in v:
                yaml_lines.append(f'  - "{item}"')
        else:
            yaml_lines.append(f'{k}: "{v}"')
    yaml_lines.append("---\n")
    return "\n".join(yaml_lines) + text


def slug_from_filename(p: Path) -> str:
    name = p.stem
    name = re.sub(r"[^a-zA-Z0-9-_]+", "-", name).strip("-").lower()
    if not name:
        name = "persona"
    return name


def find_persona_files() -> list:
    if not LLM_ONBOARDING.exists():
        return []
    return sorted(LLM_ONBOARDING.glob("*.md"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate Substack-ready posts from persona docs")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files; only print summary")
    parser.add_argument("--out", default=str(OUT_DIR_DEFAULT), help="Output directory")
    args = parser.parse_args(argv)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    files = find_persona_files()
    processed = []

    for f in files:
        text = read_text(f)
        if not looks_like_persona(text, f.name):
            continue
        title = f.name.replace("_", " ").replace("-", " ").replace(".md", "").strip()
        slug = slug_from_filename(f)
        persona_id = slug
        out_path = outdir / f"{slug}.md"

        out_text = ensure_front_matter(text, title=title, persona=persona_id)

        if args.dry_run:
            print(f"[dry-run] would write: {out_path} (source: {f})")
        else:
            out_path.write_text(out_text, encoding="utf-8")
            print(f"wrote: {out_path}")

        processed.append({"source": str(f), "out": str(out_path)})

    print(f"Processed {len(processed)} persona files.")


if __name__ == "__main__":
    main()
