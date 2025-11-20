#!/usr/bin/env python3
import json
import re
import sys
import os

p = ".secrets.scan.out"
if not os.path.exists(p):
    print("ERROR: .secrets.scan.out not found", file=sys.stderr)
    sys.exit(2)

with open(p, "r", encoding="utf-8") as f:
    s = f.read()

decoder = json.JSONDecoder()
objs = []
idx = 0
slen = len(s)
while True:
    while idx < slen and s[idx].isspace():
        idx += 1
    if idx >= slen:
        break
    try:
        obj, j = decoder.raw_decode(s, idx)
    except Exception:
        m = re.search(r"\{", s[idx:])
        if not m:
            break
        idx += m.start()
        obj, j = decoder.raw_decode(s, idx)
    objs.append(obj)
    idx = j

merged = {}
if objs:
    merged.update({k: v for k, v in objs[0].items() if k != "results"})
merged["results"] = {}
seen = set()

for obj in objs:
    results = obj.get("results") or obj.get("secrets") or {}
    if not isinstance(results, dict):
        continue
    for fname, findings in results.items():
        if not isinstance(findings, list):
            continue
        # Skip quarantined files
        if fname.startswith("secrets-local/") or "/secrets-local/" in fname:
            continue
        out_list = merged["results"].setdefault(fname, [])
        for f in findings:
            if isinstance(f, dict):
                f2 = dict(f)
                # Remove any raw secret values (safety)
                f2.pop("secret", None)
                # Deduplicate key (best-effort)
                h = (
                    f2.get("hashed_secret")
                    or f2.get("hash")
                    or (
                        f2.get("type", "")
                        + str(f2.get("line_number", ""))
                        + (f2.get("plugin") or "")
                    )
                )
                if h in seen:
                    continue
                seen.add(h)
                out_list.append(f2)
            else:
                out_list.append(f)

# Write outputs
with open(".secrets.scan.merged.json", "w", encoding="utf-8") as fh:
    json.dump(merged, fh, indent=2, ensure_ascii=False)

# Write summary
lines = []
lines.append(f"Merged {len(objs)} scan objects")
total = 0
for fname, findings in sorted(merged["results"].items()):
    lines.append(f"{fname}: {len(findings)} findings")
    total += len(findings)
lines.append(f"Total findings (filtered): {total}")
with open(".secrets.scan.summary.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print("WROTE .secrets.scan.merged.json and .secrets.scan.summary.txt", file=sys.stderr)
print("Summary:")
print("\n".join(lines[:200]))
