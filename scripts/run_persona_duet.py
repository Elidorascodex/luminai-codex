from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime


def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def render_persona_markdown(manifest: dict) -> str:
    header = f"# {manifest.get('name')}\n"
    desc = manifest.get('description', '')
    prompt = manifest.get('system_prompt', '')
    ts = datetime.utcnow().isoformat() + 'Z'
    body_lines = [header, '\n', f"**Generated (dry-run)**: {ts}\n", '\n', f"{desc}\n", '\n', '## System prompt\n', '\n', '```\n', prompt, '\n', '```\n']
    return '\n'.join(body_lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifests_dir = repo_root / "agents" / "manifests"
    out_base = repo_root / "docs" / "substack" / "output" / "duet-dryrun"

    out_base.mkdir(parents=True, exist_ok=True)

    for manifest_file in manifests_dir.glob("*.json"):
        try:
            manifest = load_manifest(manifest_file)
        except Exception:
            # skip unreadable manifests
            continue

        persona_id = manifest.get("id", manifest_file.stem)
        persona_dir = out_base / persona_id
        persona_dir.mkdir(parents=True, exist_ok=True)

        md = render_persona_markdown(manifest)
        out_path = persona_dir / f"draft_{persona_id}.md"
        out_path.write_text(md, encoding="utf-8")

        print(f"Wrote dry-run draft for {persona_id} -> {out_path.relative_to(repo_root)}")

    index_lines = ["# Persona duet dry-run index\n", "\n"]
    for persona_dir in sorted(out_base.iterdir()):
        if persona_dir.is_dir():
            index_lines.append(f"- {persona_dir.name}: {persona_dir}/draft_{persona_dir.name}.md\n")

    (out_base / "index.md").write_text(''.join(index_lines), encoding="utf-8")
    print(f"Persona duet dry-run complete. Output directory: {out_base}")


if __name__ == "__main__":
    main()
