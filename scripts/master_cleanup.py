#!/usr/bin/env python3
"""Master documentation cleanup + Substack tooling orchestrator.

This script consolidates the existing documentation hygiene utilities into a
single entry-point so it can be driven from automation, memos, or scheduled
maintenance runs. Responsibilities:

1. Scan docs/* (excluding archive/reports/substack output) for markdown files.
2. Ensure each file begins with TEC memo-style YAML front matter.
3. Normalize required metadata fields (title, dates, owner checklist, tags,
   approvers) so downstream automation stays predictable.
4. Optionally execute the Substack bundle generator to keep persona exports in
   sync with docs/llm-onboarding.

Usage:
    python scripts/master_cleanup.py [--dry-run] [--skip-substack]
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT_DEFAULT = ROOT / "docs"
SUBSTACK_OUT_DEFAULT = ROOT / "docs" / "substack" / "output"
SKIP_SEGMENTS = (
    "docs/archive/",
    "docs/reports/",
    "docs/substack/output/",
)
DEFAULT_OWNER_CHECKLIST = [
    "[ ] Read and understood",
    "[ ] Cross-linked in TEC_HUB.md and STRUCTURE.md",
    "[ ] Tested commands/steps (if procedural)",
    "[ ] Old version archived if replaced",
]
APPROVER_FALLBACKS: List[Tuple[str, str]] = [
    ("Ely", "Engineering Steward"),
    ("Airth", "Boundary Keeper"),
    ("Adelphia", "Life Everywhere"),
    ("Arcadia", "Story Bridge"),
    ("Kaznak", "Operations Strategist"),
]
FRONT_MATTER_RE = re.compile(
    r"(?s)\A(?P<prefix>\ufeff?(?:[ \t]*\n)*)---\n(?P<yaml>.*?)\n---\n?"
)
CHECKBOX_LINE_RE = re.compile(r"^(\s*-\s*)(\[[^\]]*\].*)$")


def derive_title(path: Path) -> str:
    words = path.stem.replace("_", " ").replace("-", " ").split()
    return " ".join(w.capitalize() for w in words) or path.stem


def slugify_tag(text: str) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", text.lower()).strip("-")
    return slug or "docs"


def derive_tags(path: Path, docs_root: Path) -> List[str]:
    try:
        rel = path.relative_to(docs_root)
        parts = rel.parts[:-1]
    except ValueError:
        parts = path.parts[:-1]
    tags = [slugify_tag(p.replace("_", "-")) for p in parts if p]
    tags = [tag for tag in tags if tag]
    return tags or ["docs"]


def ensure_iso_date(value: Any, fallback: str) -> Tuple[str, bool]:
    if isinstance(value, str):
        try:
            dt.date.fromisoformat(value)
            return value, False
        except ValueError:
            pass
    return fallback, True


def normalize_owner_checklist(value: Any) -> Tuple[List[str], bool]:
    items: List[str] = []
    changed = False
    if isinstance(value, list):
        for entry in value:
            if isinstance(entry, str) and entry.strip():
                normalized = entry.strip()
                if normalized not in items:
                    items.append(normalized)
                else:
                    changed = True
            else:
                changed = True
    else:
        changed = True
    for default in DEFAULT_OWNER_CHECKLIST:
        if default not in items:
            items.append(default)
            changed = True
    return items, changed


def normalize_tags(value: Any, derived: List[str]) -> Tuple[List[str], bool]:
    tags: List[str] = []
    changed = False
    original: List[str] = []
    if isinstance(value, list):
        for entry in value:
            if isinstance(entry, str) and entry.strip():
                original.append(entry.strip())
                tags.append(slugify_tag(entry))
            else:
                changed = True
        if tags != original:
            changed = True
    elif isinstance(value, str) and value.strip():
        tags = [slugify_tag(value)]
        changed = True
    else:
        changed = True
    if not tags:
        tags = derived
        changed = True
    deduped: List[str] = []
    for tag in tags:
        if not tag:
            continue
        if tag not in deduped:
            deduped.append(tag)
        else:
            changed = True
    return deduped, changed


def normalize_related_docs(value: Any) -> Tuple[List[str], bool]:
    changed = False
    docs: List[str] = []
    if isinstance(value, list):
        for entry in value:
            if isinstance(entry, str) and entry.strip():
                docs.append(entry.strip())
            else:
                changed = True
    elif value in (None, "", {}):
        changed = True
    else:
        changed = True
    return docs, changed


def normalize_approvers(value: Any) -> Tuple[List[Dict[str, Any]], bool]:
    normalized: List[Dict[str, Any]] = []
    changed = False
    if isinstance(value, list):
        for entry in value:
            if isinstance(entry, dict):
                persona = entry.get("persona")
                role = entry.get("role")
                if not persona and entry.get("name"):
                    persona = entry["name"]
                if persona and not role:
                    role = guess_role(persona)
                if persona:
                    normalized.append({"persona": persona, "role": role or "Reviewer", **{k: v for k, v in entry.items() if k not in {"persona", "role"}}})
            elif isinstance(entry, str) and entry.strip():
                persona = entry.strip()
                normalized.append({"persona": persona, "role": guess_role(persona)})
                changed = True
    elif isinstance(value, dict) and value.get("persona"):
        normalized.append(
            {
                "persona": value["persona"],
                "role": value.get("role") or guess_role(value["persona"]),
            }
        )
        changed = True
    else:
        changed = True
    if not normalized:
        persona, role = APPROVER_FALLBACKS[0]
        normalized = [{"persona": persona, "role": role}]
        changed = True
    return normalized, changed


def guess_role(persona: str) -> str:
    for name, role in APPROVER_FALLBACKS:
        if persona.lower() == name.lower():
            return role
    return "Reviewer"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def sanitize_yaml_block(block: str) -> str:
    sanitized_lines: List[str] = []
    for line in block.splitlines():
        match = CHECKBOX_LINE_RE.match(line)
        if match:
            quoted = match.group(2).replace('"', '\\"')
            sanitized_lines.append(f'{match.group(1)}"{quoted}"')
        else:
            sanitized_lines.append(line)
    return "\n".join(sanitized_lines)


class DocsCleanupEngine:
    def __init__(self, docs_root: Path, dry_run: bool):
        self.docs_root = docs_root
        self.dry_run = dry_run
        self.today = dt.date.today().isoformat()
        self.report: Dict[str, Any] = {
            "scanned": 0,
            "added_front_matter": [],
            "normalized": [],
            "invalid_front_matter": [],
        }

    def run(self) -> Dict[str, Any]:
        for md in self._collect_markdown_files():
            self.process_file(md)
        return self.report

    def _collect_markdown_files(self) -> List[Path]:
        files: List[Path] = []
        if not self.docs_root.exists():
            return files
        for path in self.docs_root.rglob("*.md"):
            posix_path = path.as_posix()
            if any(seg in posix_path for seg in SKIP_SEGMENTS):
                continue
            files.append(path)
        return sorted(files)

    def process_file(self, path: Path) -> None:
        self.report["scanned"] += 1
        text = path.read_text(encoding="utf-8")
        prefix, yaml_block, body = self._split_front_matter(text)
        rel = relative_path(path)
        if yaml_block is None:
            metadata = self._build_default_metadata(path)
            new_text = self._compose_text(prefix or self._leading_bom(text), metadata, self._strip_leading_blank_lines(text))
            if not self.dry_run:
                path.write_text(new_text, encoding="utf-8")
            self.report["added_front_matter"].append(
                {"path": rel, "applied": not self.dry_run}
            )
            return
        try:
            metadata = yaml.safe_load(sanitize_yaml_block(yaml_block)) or {}
        except yaml.YAMLError as err:
            self.report["invalid_front_matter"].append(
                {"path": rel, "error": str(err)}
            )
            return
        if not isinstance(metadata, dict):
            self.report["invalid_front_matter"].append(
                {"path": rel, "error": "front matter is not a mapping"}
            )
            return
        changed, changed_fields = self._normalize_metadata(metadata, path)
        if not changed:
            return
        new_text = self._compose_text(prefix, metadata, body)
        if not self.dry_run:
            path.write_text(new_text, encoding="utf-8")
        self.report["normalized"].append(
            {"path": rel, "fields": changed_fields, "applied": not self.dry_run}
        )

    def _build_default_metadata(self, path: Path) -> Dict[str, Any]:
        return {
            "title": derive_title(path),
            "date_created": self.today,
            "date_updated": self.today,
            "status": "draft",
            "approvers": [
                {"persona": APPROVER_FALLBACKS[0][0], "role": APPROVER_FALLBACKS[0][1]}
            ],
            "owner_checklist": DEFAULT_OWNER_CHECKLIST[:],
            "tags": derive_tags(path, self.docs_root),
            "related_docs": [],
        }

    def _normalize_metadata(self, metadata: Dict[str, Any], path: Path) -> Tuple[bool, List[str]]:
        changed_fields: List[str] = []
        today = self.today

        def set_field(key: str, value: Any) -> None:
            metadata[key] = value
            if key not in changed_fields:
                changed_fields.append(key)

        if not metadata.get("title"):
            set_field("title", derive_title(path))

        dc, updated_dc = ensure_iso_date(metadata.get("date_created"), today)
        if updated_dc:
            set_field("date_created", dc)

        du, updated_du = ensure_iso_date(metadata.get("date_updated"), today)
        if updated_du:
            set_field("date_updated", du)

        if not metadata.get("status"):
            set_field("status", "draft")

        tags, tags_changed = normalize_tags(metadata.get("tags"), derive_tags(path, self.docs_root))
        if tags_changed:
            set_field("tags", tags)

        owners, owners_changed = normalize_owner_checklist(metadata.get("owner_checklist"))
        if owners_changed:
            set_field("owner_checklist", owners)

        rel_docs, rel_docs_changed = normalize_related_docs(metadata.get("related_docs"))
        if rel_docs_changed:
            set_field("related_docs", rel_docs)

        approvers, approvers_changed = normalize_approvers(metadata.get("approvers"))
        if approvers_changed:
            set_field("approvers", approvers)

        if changed_fields and "date_updated" not in changed_fields:
            set_field("date_updated", today)

        return bool(changed_fields), changed_fields

    def _split_front_matter(self, text: str) -> Tuple[str, str | None, str]:
        match = FRONT_MATTER_RE.match(text)
        if not match:
            return "", None, text
        prefix = match.group("prefix")
        yaml_block = match.group("yaml")
        body = text[match.end() :]
        return prefix, yaml_block, body

    def _compose_text(self, prefix: str, metadata: Dict[str, Any], body: str) -> str:
        yaml_block = yaml.safe_dump(metadata, sort_keys=False).strip()
        formatted_body = self._format_body(body)
        return f"{prefix}---\n{yaml_block}\n---{formatted_body}"

    def _format_body(self, body: str) -> str:
        if not body:
            return "\n"
        if body.startswith(("\n", "\r\n")):
            return body
        return "\n\n" + body

    def _strip_leading_blank_lines(self, text: str) -> str:
        stripped = text.lstrip("\ufeff")
        return stripped.lstrip("\r\n")

    def _leading_bom(self, text: str) -> str:
        return "\ufeff" if text.startswith("\ufeff") else ""


def run_substack_bundle(out_dir: Path, dry_run: bool) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    module_path = ROOT / "scripts" / "generate_substack_bundle.py"
    spec = importlib.util.spec_from_file_location(
        "generate_substack_bundle", module_path
    )
    if not spec or not spec.loader:
        return {"error": f"Unable to load {module_path}"}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    args = ["--out", str(out_dir)]
    if dry_run:
        args.insert(0, "--dry-run")
    buffer = io.StringIO()
    result: Dict[str, Any] = {"dry_run": dry_run, "out_dir": str(out_dir)}
    try:
        with redirect_stdout(buffer):
            module.main(args)  # type: ignore[attr-defined]
    except SystemExit as exc:  # propagate CLI exit codes as structured info
        result["error"] = f"generate_substack_bundle exited with {exc.code}"
    result["stdout"] = buffer.getvalue().strip()
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Master documentation cleanup + Substack bundler"
    )
    parser.add_argument(
        "--docs-root", default=str(DOCS_ROOT_DEFAULT), help="Docs directory to scan"
    )
    parser.add_argument(
        "--substack-out",
        default=str(SUBSTACK_OUT_DEFAULT),
        help="Substack output directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report actions without writing to disk",
    )
    parser.add_argument(
        "--skip-substack",
        action="store_true",
        help="Skip running the Substack bundle generator",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    docs_root = Path(args.docs_root).resolve()
    engine = DocsCleanupEngine(docs_root=docs_root, dry_run=args.dry_run)
    docs_report = engine.run()

    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    summary: Dict[str, Any] = {
        "timestamp": timestamp,
        "dry_run": args.dry_run,
        "docs_root": str(docs_root),
        "docs": docs_report,
    }

    if not args.skip_substack:
        substack_report = run_substack_bundle(
            out_dir=Path(args.substack_out).resolve(), dry_run=args.dry_run
        )
        summary["substack"] = substack_report
    else:
        summary["substack"] = {"skipped": True}

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
