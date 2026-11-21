#!/usr/bin/env python3
"""build_directory.py — generate directory-plugin/, the Claude plugin directory edition.

Unverified publishers may only ship Markdown, text, JSON, YAML and images in a
directory plugin, with the skill under skills/<name>/. This script builds that
folder from the skill in translate-cli/assets/taiwan-translate so nothing is
maintained twice:

    data/*.csv            -> data/*.json (split into parts when over 240 KiB)
    references/*.md       -> references/*.md (script commands rewritten)
    EXAMPLES.md, LICENSE, .claude-plugin/plugin.json and icon.png
    scripts/directory/SKILL.md.tmpl, README.md.tmpl

Scripts, package.json and anything starting with #! are left out. Standard
library only.

Usage:
    python scripts/build_directory.py           # write directory-plugin/
    python scripts/build_directory.py --check   # exit 1 if stale, untracked or unsafe
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "translate-cli" / "assets" / "taiwan-translate"
PKG = ROOT / "translate-cli" / "package.json"
OUT = ROOT / "directory-plugin"
TMPL = ROOT / "scripts" / "directory"
SKILL_DIR = "skills/tw-translate"
REPO = "https://github.com/Moksa1123/taiwan-translate-skill"

MAX_JSON = 240 * 1024   # the directory holds non-image files over 256 KiB for review
ALLOWED_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".png"}

DATA_FILES = {
    "glossary": "WordPress 台灣社群 GlotPress 詞彙表（英文 → 台灣正體）",
    "taiwan-terms": "中國用語 → 台灣用語對照，附繁化姬實測輸出",
    "pending": "查不到、還沒解決的問題",
}

# What the directory's scanner reads as "reads the installer's credentials" or a
# server login. None of these may survive the build.
FORBIDDEN = re.compile(
    r"\bssh\b|\bscp\b|wp-config|\.env\b|id_rsa|id_ed25519|\.pem\b|SSH_KEY"
    r"|process\.env|os\.environ|getenv|\$\{[^}]*\}|\$[A-Za-z_]\w*|<[A-Za-z_ -]*KEY>",
    re.I)

REFERENCE_NOTE = (
    "> 官方目錄精簡版：本資料夾只有參考檔，不含腳本。下文提到 `scripts/` 的指令要裝完整版"
    "（npm 套件 `taiwan-translate-skill`）；精簡版改用搜尋 `data/*.json` 代替。\n"
)


def csv_rows(name: str) -> tuple[list[str], list[dict]]:
    with (SKILL / "data" / f"{name}.csv").open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def to_json(stem: str) -> dict[str, str]:
    """One table as one JSON file, or numbered parts when too large. One row per line so a
    text search returns the whole row."""
    cols, rows = csv_rows(stem)

    def dump(part_rows, part=None, parts=None):
        head = {"source_file": f"translate-cli/assets/taiwan-translate/data/{stem}.csv", "columns": cols}
        if part:
            head["part"] = f"{part} of {parts}"
        lines = [json.dumps(r, ensure_ascii=False) for r in part_rows]
        body = json.dumps(head, ensure_ascii=False, indent=1)[:-2]
        return body + ',\n "rows": [\n  ' + ",\n  ".join(lines) + "\n ]\n}\n"

    whole = dump(rows)
    if len(whole.encode("utf-8")) <= MAX_JSON:
        return {f"{stem}.json": whole}
    n = 2
    while True:
        size = -(-len(rows) // n)
        chunks = [rows[i:i + size] for i in range(0, len(rows), size)]
        texts = [dump(c, i + 1, len(chunks)) for i, c in enumerate(chunks)]
        if all(len(t.encode("utf-8")) <= MAX_JSON for t in texts):
            return {f"{stem}-{i + 1}.json": t for i, t in enumerate(texts)}
        n += 1


def facts() -> dict[str, str]:
    g = csv_rows("glossary")[1]
    t = csv_rows("taiwan-terms")[1]
    latest = max(r["retrieved_on"] for r in g)
    res = (SKILL / "evals" / "RESULTS.md").read_text(encoding="utf-8")
    m = re.search(r"計分題答對率（(\d+) 題） \| \*\*(\d+)/\d+[^|]*\| (\d+)/\d+", res)
    return {
        "PKG_VERSION": json.loads(PKG.read_text(encoding="utf-8"))["version"],
        "GLOSSARY": f"{len(g):,}",
        "GLOSSARY_CURRENT": f"{sum(r['retrieved_on'] == latest for r in g):,}",
        "GLOSSARY_OLD": str(sum(r["retrieved_on"] != latest for r in g)),
        "OLD_DATE": min(r["retrieved_on"] for r in g),
        "RETRIEVED": latest,
        "TERMS": str(len(t)),
        "TERMS_MEASURED": str(sum(r["trust"] == "實測" for r in t)),
        "TERMS_DOCS": str(sum(r["trust"] == "官方文件" for r in t)),
        "TERMS_HOUSE": str(sum(r["trust"] == "站內風格" for r in t)),
        "MEASURED": max(r["measured_on"][:10] for r in t),
        "EVAL_N": m.group(1), "EVAL_WITH": m.group(2), "EVAL_WITHOUT": m.group(3),
    }


def fill(template: str, values: dict) -> str:
    out = template
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        raise SystemExit(f"unfilled placeholders: {left}")
    return out


def reference(text: str) -> str:
    """Point script commands at the JSON files; keep the rest as is."""
    text = text.replace("`data/taiwan-terms.csv`", "`data/taiwan-terms.json`")
    text = text.replace("WP 譯法以 `python scripts/search.py <英文>` 為準",
                        "WP 譯法以搜尋 `data/glossary-*.json` 的結果為準")
    text = text.replace("`data/pending.csv`", "`data/pending.json`（精簡版不能寫入，請回報給使用者）")
    text = re.sub(r"(?m)^> 可用 `python scripts/po\.py validate[^\n]*\n",
                  "> 完整版的 `po.py validate` 會自動偵測此問題（code: `initial-lowercase`）。\n", text)
    first, _, rest = text.partition("\n")
    return f"{first}\n\n{REFERENCE_NOTE}{rest}"


def plugin_json() -> str:
    pj = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    pj["description"] = pj["description"].replace(
        "term lookup with sources, China-to-Taiwan term pairs, and a .po / .pot validator",
        "term lookup with sources, China-to-Taiwan term pairs and .po / .pot translation rules. "
        "Directory edition: reference files only, no scripts; the validator ships in the npm package",
    )
    pj["author"] = {"name": "Moksa"}
    pj["homepage"] = f"{REPO}/tree/main/directory-plugin#readme"
    pj["documentationUrl"] = f"{REPO}/tree/main/directory-plugin#readme"
    pj["privacyPolicyUrl"] = f"{REPO}/tree/main/directory-plugin#what-it-runs-and-connects-to"
    pj["skills"] = [f"./{SKILL_DIR}"]
    return json.dumps(pj, ensure_ascii=False, indent=2) + "\n"


def build() -> dict[str, bytes]:
    values = facts()
    files: dict[str, str | bytes] = {}
    data_rows = []
    for stem, what in DATA_FILES.items():
        parts = to_json(stem)
        for rel, text in parts.items():
            files[f"{SKILL_DIR}/data/{rel}"] = text
        names = "、".join(f"`data/{r}`" for r in parts)
        data_rows.append(f"| {names} | {len(csv_rows(stem)[1])} | {what} |")
    values["DATA_FILES"] = "\n".join(data_rows)
    files[f"{SKILL_DIR}/SKILL.md"] = fill((TMPL / "SKILL.md.tmpl").read_text(encoding="utf-8"), values)
    files["README.md"] = fill((TMPL / "README.md.tmpl").read_text(encoding="utf-8"), values)
    for p in sorted((SKILL / "references").glob("*.md")):
        files[f"{SKILL_DIR}/references/{p.name}"] = reference(p.read_text(encoding="utf-8"))
    files[f"{SKILL_DIR}/EXAMPLES.md"] = (SKILL / "EXAMPLES.md").read_text(encoding="utf-8")
    files["LICENSE"] = (ROOT / "LICENSE").read_text(encoding="utf-8")
    files[".claude-plugin/plugin.json"] = plugin_json()
    files[".claude-plugin/icon.png"] = (ROOT / ".claude-plugin" / "icon.png").read_bytes()

    out = {k: v if isinstance(v, bytes) else v.replace("\r\n", "\n").encode("utf-8") for k, v in files.items()}
    problems = []
    for rel, data in out.items():
        name = Path(rel).name
        if Path(rel).suffix not in ALLOWED_SUFFIXES and name != "LICENSE":
            problems.append(f"{rel}: file type not allowed in the directory edition")
        if name == "package.json":
            problems.append(f"{rel}: package.json not allowed")
        if rel.endswith(".png"):
            continue
        if data.startswith(b"#!"):
            problems.append(f"{rel}: starts with #!")
        if len(data) > 256 * 1024:
            problems.append(f"{rel}: {len(data) // 1024} KiB, over 256 KiB")
        for i, line in enumerate(data.decode("utf-8").splitlines(), 1):
            if FORBIDDEN.search(line):
                problems.append(f"{rel}:{i}: {line.strip()[:100]}")
    if problems:
        raise SystemExit("directory edition would break the directory's rules:\n  " + "\n  ".join(problems))
    return out


def existing() -> dict[str, bytes]:
    if not OUT.exists():
        return {}
    return {p.relative_to(OUT).as_posix(): p.read_bytes() for p in OUT.rglob("*") if p.is_file()}


def untracked(want: dict[str, bytes]) -> list[str]:
    """Generated files git does not track. The directory reads GitHub, not this disk: a file
    a .gitignore rule swallows is missing there."""
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--", "directory-plugin"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return ["git ls-files failed: cannot tell whether directory-plugin/ is committed"]
    tracked = {p[len("directory-plugin/"):] for p in out.split("\0") if p}
    return [f"not tracked by git (ignored or never added): {k}" for k in sorted(set(want) - tracked)]


def differences(want: dict[str, bytes], have: dict[str, bytes]) -> list[str]:
    # a Windows checkout may turn LF into CRLF; that is not drift
    def same(k):
        a, b = want[k], have[k]
        return a == b or (not k.endswith(".png") and a == b.replace(b"\r\n", b"\n"))
    out = [f"missing: {k}" for k in sorted(set(want) - set(have))]
    out += [f"stale (not built from sources): {k}" for k in sorted(set(have) - set(want))]
    out += [f"out of date: {k}" for k in sorted(set(want) & set(have)) if not same(k)]
    return out


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true", help="only compare; exit 1 if stale or untracked")
    args = ap.parse_args()
    want = build()   # exits on forbidden words, file types or sizes
    diff = differences(want, existing())
    if args.check:
        diff += untracked(want)
        if diff:
            print("directory-plugin/ is out of step with its sources (run scripts/build_directory.py):")
            for d in diff:
                print("  x", d)
            return 1
        total = sum(len(v) for v in want.values())
        print(f"directory-plugin/ matches its sources ({len(want)} files, {total // 1024} KiB), "
              "all tracked by git, no forbidden words.")
        return 0
    for rel, data in want.items():
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    stale = [d for d in diff if d.startswith("stale")]
    print(f"wrote {len(want)} files to directory-plugin/")
    for d in stale:
        print("  !", d, "(remove it by hand)")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
