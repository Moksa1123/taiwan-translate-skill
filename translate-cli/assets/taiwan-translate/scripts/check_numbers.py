#!/usr/bin/env python3
"""
check_numbers.py — SKILL.md 裡的每一個數字都要有來由，而且要對得上資料（skill-SOP 6-1）。

做法照 line-api：先把 SKILL.md 的數字全部找出來（程式碼區塊、行內 `code`、網址除外），
每一個都必須被 RULES 的某一條認領，否則失敗。新增數字時要同時登記一條規則。

規則三種：
    fact   由資料算出來的值，跟 FACTS 比（--fix 可自動改）
    date   日期：必須出現在資料檔的出處欄裡（retrieved_on／measured_on）
    fixed  不從資料來的數字（步驟編號、通過標準），要寫明理由

在 repo 裡執行時，也用 README_RULES 核對 README.md、README.zh-TW.md、docs/guide.md，
並核對徽章數字、npx 版號與 .claude-plugin/plugin.json 版號（要等於 package.json）。

用法：
    python scripts/check_numbers.py            # 有問題 exit 1
    python scripts/check_numbers.py --fix      # fact 不一致時直接改 SKILL.md
    python scripts/check_numbers.py --stats    # 印目前各資料的筆數（SKILL.md 的數字從這裡來）
只用標準函式庫。
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILL_MD = ROOT / "SKILL.md"
DATA = ROOT / "data"


def _rows(name: str) -> list[dict]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def stats() -> dict[str, int]:
    g = _rows("glossary.csv")
    t = _rows("taiwan-terms.csv")
    latest = max(r["retrieved_on"] for r in g)
    out = {
        "glossary": len(g),
        "glossary_current": sum(r["retrieved_on"] == latest for r in g),
        "glossary_old": sum(r["retrieved_on"] != latest for r in g),
        "terms": len(t),
    }
    for trust in ("實測", "官方文件", "站內風格", "推論"):
        out[f"terms_{trust}"] = sum(r["trust"] == trust for r in t)
    out["pending_open"] = sum(r["status"] != "done" for r in _rows("pending.csv"))
    return out


def _dates() -> set[str]:
    found = {r["retrieved_on"] for r in _rows("glossary.csv")}
    found |= {r["measured_on"][:10] for r in _rows("taiwan-terms.csv")}
    return found


# (正規式, 種類, 參數)。第 1 組是被認領的數字；沒有分組就認領整段比對到的數字。
RULES: list[tuple[str, str, str]] = [
    # ---- 由資料算出來 ----
    (r"(\d+) 列（現行", "fact", "glossary"),
    (r"現行 (\d+) 列", "fact", "glossary_current"),
    (r"舊版快照 (\d+) 列", "fact", "glossary_old"),
    (r"\| (\d+) 列（實測", "fact", "terms"),
    (r"（實測 (\d+)、", "fact", "terms_實測"),
    (r"、官方文件 (\d+)、", "fact", "terms_官方文件"),
    (r"、站內風格 (\d+)）", "fact", "terms_站內風格"),
    # ---- 日期：要出現在資料的出處欄 ----
    (r"20\d\d-\d\d-\d\d", "date", ""),
    # ---- 不從資料來的數字 ----
    (r"(?m)^\| [^|]*\| \d\. .*$|(?<![\d.])\d\. ", "fixed", "步驟編號"),
    (r"exit 0|錯誤 0|非 0|回 1|0 錯誤", "fixed", "驗證器的通過標準（po.py validate 的 exit code）"),
]

# ---- README（repo 根目錄的 README.md／README.zh-TW.md、docs/guide.md）----
# npm 安裝版沒有這些檔，找不到就跳過。
REPO = ROOT.parents[2]
CLI = ROOT.parents[1]
READMES = ["README.md", "README.zh-TW.md", "docs/guide.md"]


def _eval_result() -> tuple[str, str, str, str]:
    res = (ROOT / "evals" / "RESULTS.md").read_text(encoding="utf-8")
    m = re.search(r"計分題答對率（(\d+) 題） \| \*\*(\d+)/\d+[^|]*\| (\d+)/\d+", res)
    total = re.search(r"全部題目（(\d+) 題）", res)
    return m.group(1), m.group(2), m.group(3), total.group(1)


def readme_facts() -> dict[str, str]:
    import json
    types = (CLI / "src" / "types" / "index.ts").read_text(encoding="utf-8")
    union = types.split("export type AIType =", 1)[1].split(";", 1)[0]
    ev = _eval_result()
    pkg = json.loads((CLI / "package.json").read_text(encoding="utf-8"))
    return {
        "platforms": str(len([t for t in re.findall(r"'([a-z]+)'", union) if t != "all"])),
        "self_tests": str(len(re.findall(r"^[ \t]+def test_", (HERE / "test_tools.py").read_text(encoding="utf-8"), re.M))),
        "eval_n": ev[0], "eval_with": ev[1], "eval_without": ev[2], "eval_total": ev[3],
        "node_min": re.search(r"(\d+)", pkg["engines"]["node"]).group(1),
        "pkg_version": pkg["version"],
    }


# 英文、中文兩種寫法擇一，所以 README 允許某條規則在某份檔案沒用到
README_RULES: list[tuple[str, str, str]] = [
    (r"([\d,]+) (?:glossary rows|列詞彙)", "fact", "glossary"),
    (r"(?:([\d,]+) current|現行 ([\d,]+) 列)", "fact", "glossary_current"),
    (r"(?:(\d+) kept from|快照留存 (\d+) 列)", "fact", "glossary_old"),
    (r"(\d+) (?:term pairs|組用語對照)", "fact", "terms"),
    (r"(?:(\d+) measured|實測 (\d+))", "fact", "terms_實測"),
    (r"(?:(\d+) from official docs|官方文件 (\d+))", "fact", "terms_官方文件"),
    (r"(?:(\d+) house style|站內風格 (\d+))", "fact", "terms_站內風格"),
    (r"(?:(\d+) AI tools|(\d+) 種 AI)", "fact", "platforms"),
    (r"(?:(\d+) offline tests|(\d+) 項離線測試)", "fact", "self_tests"),
    (r"(?:(\d+) scored questions|(\d+) 題計分題)", "fact", "eval_n"),
    (r"(?:(\d+) questions in all|全部 (\d+) 題)", "fact", "eval_total"),
    (r"(?:with the skill|(?<!沒)有 skill) (\d+)/\d+", "fact", "eval_with"),
    (r"(?:with the skill|(?<!沒)有 skill) \d+/(\d+)", "fact", "eval_n"),
    (r"(?:without it|沒有 skill) (\d+)/\d+", "fact", "eval_without"),
    (r"(?:without it|沒有 skill) \d+/(\d+)", "fact", "eval_n"),
    (r"Node(?:\.js)? (\d+)", "fact", "node_min"),
    (r"20\d\d-\d\d-\d\d", "date", ""),
    (r"Python 3", "ok", "執行需求（只用標準函式庫）"),
    (r"Step [1-3]", "ok", "快速開始的步驟編號"),
    (r"exits? [01]|回 [01]|非 0|0 errors|錯誤 0", "ok", "po.py validate 的 exit code 與通過標準"),
    (r"</?h[1-6]", "ok", "HTML 標題標籤"),
    (r"2024 (?:snapshot|快照)", "ok", "舊列快照的年份（完整日期由 date 規則核對）"),
    (r"UTF-8|U\+[0-9A-F]{4}", "ok", "編碼名稱"),
]

# 徽章網址裡的數字（網址在一般掃描時被遮掉，這裡另外核對）
BADGE_RULES: list[tuple[str, str]] = [
    (r"badge/glossary-(\d+)-", "glossary"),
    (r"badge/Taiwan%20terms-(\d+)-", "terms"),
    (r"badge/AI%20platforms-(\d+)-", "platforms"),
    (r"badge/self--tests-(\d+)-", "self_tests"),
    (r"badge/node-%3E%3D(\d+)-", "node_min"),
]


def badge_and_pin_problems() -> list[str]:
    import json
    facts = {**stats(), **readme_facts()}
    out: list[str] = []
    for name in READMES:
        text = (REPO / name).read_text(encoding="utf-8")
        for rx, key in BADGE_RULES:
            for got in re.findall(rx, text):
                if got != str(facts[key]):
                    out.append(f"{name} 徽章 {key}：寫 {got}，實際 {facts[key]}")
        for badge in re.findall(r"img\.shields\.io/badge/([^\"?)]+)", text):
            if re.search(r"-\d", badge) and not any(re.search(rx, "badge/" + badge + "-") for rx, _ in BADGE_RULES) \
                    and not badge.startswith(("python-3", "license-", "format-", "PayPal-")):
                out.append(f"{name} 徽章沒有登記在 BADGE_RULES：{badge}")
        for got in re.findall(r"taiwan-translate-skill@(\d+\.\d+\.\d+)", text):
            if got != facts["pkg_version"]:
                out.append(f"{name}：taiwan-translate-skill@{got}，package.json 是 {facts['pkg_version']}")
    pj = REPO / ".claude-plugin" / "plugin.json"
    if pj.exists():
        v = json.loads(pj.read_text(encoding="utf-8"))["version"]
        if v != facts["pkg_version"]:
            out.append(f".claude-plugin/plugin.json 版號 {v}，package.json 是 {facts['pkg_version']}")
    return out


NUM = re.compile(r"\d+(?:[.,]\d+)*")
_MASKS = [
    re.compile(r"^```.*?^```", re.S | re.M),   # 程式碼區塊
    re.compile(r"`[^`\n]+`"),                  # 行內 code
    re.compile(r"\]\([^)\n]*\)"),              # markdown 連結目標
    re.compile(r"https?://[^\s)）（，、|]+"),    # 網址
    re.compile(r"\A---\n.*?\n---\n", re.S),    # frontmatter（zh_TW 等）
]


def _masked(text: str) -> str:
    for rx in _MASKS:
        text = rx.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    return text


def check(path: Path = SKILL_MD, fix: bool = False, rules=None,
          allow_unused: bool = False) -> tuple[list[str], int]:
    """回傳 (問題清單, 檢查過的數字個數)。"""
    rules = RULES if rules is None else rules
    text = path.read_text(encoding="utf-8")
    scan = _masked(text)
    problems: list[str] = []
    covered: set[int] = set()
    edits: list[tuple[int, int, str]] = []
    facts = {**stats(), **(readme_facts() if rules is not RULES else {})}
    dates = _dates()

    for pattern, kind, arg in rules:
        found = list(re.finditer(pattern, scan, re.M))
        if not found:
            if not allow_unused:
                problems.append(f"規則沒用到（{path.name} 改過寫法？）：{pattern}")
            continue
        for m in found:
            spans = [m.span(g) for g in range(1, (m.re.groups or 0) + 1) if m.group(g) is not None]
            span = spans[0] if spans else m.span()
            if kind == "ok":
                covered.update(range(*m.span()))
                continue
            if kind == "fixed":
                # 步驟編號規則整行認領會吃掉同行的其他數字，只認領「n. 」本身
                for n in re.finditer(r"(?<![\d.])\d\. |exit 0|錯誤 0|非 0|回 1|0 錯誤", m.group(0)):
                    covered.update(range(m.start() + n.start(), m.start() + n.end()))
                continue
            covered.update(range(*span))
            got = text[span[0]:span[1]]
            if kind == "fact":
                want = str(facts[arg])
                if "," in got and want.isdigit():
                    want = f"{int(want):,}"
                if got != want:
                    problems.append(f"fact {arg}：{path.name} 寫 {got}，實際 {want}")
                    edits.append((span[0], span[1], want))
            elif kind == "date" and got not in dates:
                problems.append(f"日期 {got} 不在任何資料的出處欄（retrieved_on／measured_on）")

    line_of = lambda pos: text.count("\n", 0, pos) + 1  # noqa: E731
    for m in NUM.finditer(scan):
        if not any(i in covered for i in range(*m.span())):
            problems.append(f"第 {line_of(m.start())} 行的 {m.group(0)} 沒有登記在 RULES")

    if fix and edits:
        for start, end, want in sorted(edits, reverse=True):
            text = text[:start] + want + text[end:]
        path.write_text(text, encoding="utf-8")
    return problems, sum(1 for _ in NUM.finditer(scan))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="SKILL.md 數字核對")
    ap.add_argument("--fix", action="store_true", help="fact 不一致時直接改 SKILL.md")
    ap.add_argument("--stats", action="store_true", help="印目前各資料的筆數")
    args = ap.parse_args()
    if args.stats:
        for k, v in stats().items():
            print(f"{k}\t{v}")
        return 0
    report = [("SKILL.md", *check(fix=args.fix))]
    in_repo = (REPO / "README.md").exists() and (CLI / "src").exists()
    if in_repo:
        for name in READMES:
            report.append((name, *check(REPO / name, fix=args.fix, rules=README_RULES, allow_unused=True)))
        report.append(("徽章／版號", badge_and_pin_problems(), 0))
    bad = 0
    for name, problems, n in report:
        if not problems:
            if n:
                print(f"{name} 的 {n} 個數字全部登記且與資料一致。")
            else:
                print(f"{name} 一致。")
            continue
        bad += 1
        print(f"{name} 有 {len(problems)} 個問題：")
        for p in problems:
            print("  ✗", p)
    if not in_repo:
        print("（不在 repo 裡，README 不檢查）")
    if bad and args.fix:
        print("（fact 已改；其餘要人工處理）")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
