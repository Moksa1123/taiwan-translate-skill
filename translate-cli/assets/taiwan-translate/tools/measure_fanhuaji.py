#!/usr/bin/env python3
"""
measure_fanhuaji.py — 用繁化姬 API 實測 data/taiwan-terms.csv 每一列，填出處與可信度（維護者用）。

做法：把每列的 cn 送進繁化姬「台灣化」轉換器（api.zhconvert.org/convert，converter=Taiwan），
記下輸出，與本表的 tw 比對：
    - 輸出＝tw：trust＝實測（繁化姬真的這樣轉）。
    - 輸出≠tw，但 WP 台灣詞彙表裡 note 的英文詞譯作 tw：trust＝官方文件，doc_url＝WP 詞彙表。
    - 其餘：trust＝站內風格（本 skill 自己的用詞慣例，不是繁化姬的轉換結果）。

輸出欄位：cn,tw,category,note,fanhuaji_out,measured_on,doc_url,trust
用法：
    python tools/measure_fanhuaji.py            # 連網實測並寫回
    python tools/measure_fanhuaji.py --dry-run  # 只印統計
只用標準函式庫。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
TERMS = DATA / "taiwan-terms.csv"
GLOSSARY = DATA / "glossary.csv"
API = "https://api.zhconvert.org/convert"
FHJ_DOC = "https://docs.zhconvert.org/"
WP_GLOSSARY = "https://translate.wordpress.org/locale/zh-tw/default/glossary/"
FIELDS = ["cn", "tw", "category", "note", "fanhuaji_out", "measured_on", "doc_url", "trust"]


def convert(lines: list[str]) -> tuple[list[str], str]:
    data = urllib.parse.urlencode({"converter": "Taiwan", "text": "\n".join(lines)}).encode()
    req = urllib.request.Request(API, data=data, headers={"User-Agent": "Mozilla/5.0 (compatible; glossary-check)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    out = d["data"]["text"].split("\n")
    if len(out) != len(lines):
        raise SystemExit(f"繁化姬回傳 {len(out)} 行，送出 {len(lines)} 行，無法逐列對應")
    return out, d.get("revisions", {}).get("build", "?")


def wp_pairs() -> set[tuple[str, str]]:
    with GLOSSARY.open(encoding="utf-8-sig") as f:
        return {(r["en"].strip().lower(), r["zh-tw"].strip()) for r in csv.DictReader(f)}


def note_en(note: str) -> list[str]:
    """note 欄的英文詞：'file/document' -> ['file', 'document']；去掉括號說明。"""
    note = re.sub(r"\(.*?\)", "", note)
    return [w.strip().lower() for w in note.split("/") if w.strip()]


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="實測 taiwan-terms.csv")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = list(csv.DictReader(TERMS.open(encoding="utf-8-sig")))
    out, build = convert([r["cn"] for r in rows])
    stamp = f"{dt.date.today().isoformat()} api.zhconvert.org converter=Taiwan build={build}"
    wp = wp_pairs()
    tally: dict[str, int] = {}
    for r, o in zip(rows, out):
        r["fanhuaji_out"], r["measured_on"] = o, stamp
        if o == r["tw"]:
            r["doc_url"], r["trust"] = FHJ_DOC, "實測"
        elif any((en, r["tw"]) in wp for en in note_en(r["note"])):
            r["doc_url"], r["trust"] = WP_GLOSSARY, "官方文件"
        else:
            r["doc_url"], r["trust"] = "", "站內風格"
        tally[r["trust"]] = tally.get(r["trust"], 0) + 1
    print(f"{len(rows)} 列：" + "、".join(f"{k} {v}" for k, v in sorted(tally.items())) + f"（{stamp}）")
    if args.dry_run:
        return 0
    with TERMS.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in FIELDS} for r in rows)
    print(f"已寫入 {TERMS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
