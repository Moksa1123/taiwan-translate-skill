#!/usr/bin/env python3
"""
check_numbers.py — SKILL.md 裡的每一個數字都要有來由，而且要對得上資料（skill-SOP 6-1）。

做法照 line-api：先把 SKILL.md 的數字全部找出來（程式碼區塊、行內 `code`、網址除外），
每一個都必須被 RULES 的某一條認領，否則失敗。新增數字時要同時登記一條規則。

規則三種：
    fact   由資料算出來的值，跟 FACTS 比（--fix 可自動改）
    date   日期：必須出現在資料檔的出處欄裡（retrieved_on／measured_on）
    fixed  不從資料來的數字（步驟編號、通過標準），要寫明理由

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


def check(path: Path = SKILL_MD, fix: bool = False) -> tuple[list[str], int]:
    """回傳 (問題清單, 檢查過的數字個數)。"""
    text = path.read_text(encoding="utf-8")
    scan = _masked(text)
    problems: list[str] = []
    covered: set[int] = set()
    edits: list[tuple[int, int, str]] = []
    facts = stats()
    dates = _dates()

    for pattern, kind, arg in RULES:
        found = list(re.finditer(pattern, scan, re.M))
        if not found:
            problems.append(f"規則沒用到（SKILL.md 改過寫法？）：{pattern}")
            continue
        for m in found:
            span = m.span(1) if m.re.groups else m.span()
            if kind == "fixed":
                # 步驟編號規則整行認領會吃掉同行的其他數字，只認領「n. 」本身
                for n in re.finditer(r"(?<![\d.])\d\. |exit 0|錯誤 0|非 0|回 1|0 錯誤", m.group(0)):
                    covered.update(range(m.start() + n.start(), m.start() + n.end()))
                continue
            covered.update(range(*span))
            got = text[span[0]:span[1]]
            if kind == "fact":
                want = str(facts[arg])
                if got != want:
                    problems.append(f"fact {arg}：SKILL.md 寫 {got}，實際 {want}")
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
    problems, n = check(fix=args.fix)
    if not problems:
        print(f"SKILL.md 的 {n} 個數字全部登記且與資料一致。")
        return 0
    print(f"SKILL.md 有 {len(problems)} 個數字問題：")
    for p in problems:
        print("  ✗", p)
    if args.fix:
        print("（fact 已改；其餘要人工處理）")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
