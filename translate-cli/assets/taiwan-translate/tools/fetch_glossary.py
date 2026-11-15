#!/usr/bin/env python3
"""
fetch_glossary.py — 從 WordPress 台灣社群 GlotPress 詞彙表重建 data/glossary.csv（維護者用）。

來源：https://translate.wordpress.org/locale/zh-tw/default/glossary/ 的 CSV 匯出
     （-export/，欄位 en,zh-tw,pos,description）。

輸出欄位：en,zh-tw,pos,description,doc_url,retrieved_on,trust
    - 現行詞彙表裡的列：doc_url＝GlotPress 詞彙表，retrieved_on＝擷取日，trust＝官方文件。
    - 舊檔有、現行詞彙表已沒有這個英文詞的列：保留，沿用舊的 doc_url／retrieved_on
      （第一次轉換時視為 GitHub 快照 ebeba19，2024-03-22），trust＝官方文件。
      搜尋時看 retrieved_on 就知道它是舊版。
    - 舊檔有、但現行詞彙表同一英文詞已改譯的列：丟掉（以現行為準），並印出來。

用法：
    python tools/fetch_glossary.py                  # 連網下載
    python tools/fetch_glossary.py --from-file x.csv --date 2026-11-15   # 用已下載的匯出檔
    python tools/fetch_glossary.py --dry-run        # 只印差異，不寫檔
只用標準函式庫。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "data" / "glossary.csv"
GLOSSARY_URL = "https://translate.wordpress.org/locale/zh-tw/default/glossary/"
EXPORT_URL = GLOSSARY_URL + "-export/"
# 這份 skill 最早的 glossary.csv 與這個 GitHub 檔位元組相同（2026-11-15 以 sha1 核對）
SNAPSHOT_URL = ("https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary/blob/"
                "ebeba191481bbbfc6d1ae4d12c71ab1599dffa7c/TM%20Glossary/locale-zh-tw-glossary.csv")
SNAPSHOT_DATE = "2024-03-22"
FIELDS = ["en", "zh-tw", "pos", "description", "doc_url", "retrieved_on", "trust"]


def key(row: dict) -> tuple[str, str]:
    return row["en"].strip().lower(), row["zh-tw"].strip()


def download() -> str:
    req = urllib.request.Request(EXPORT_URL, headers={"User-Agent": "Mozilla/5.0 (compatible; glossary-fetch)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8-sig")


def build(export_text: str, old_rows: list[dict], date: str) -> tuple[list[dict], list[dict], list[dict]]:
    """回傳 (新列, 保留的舊列, 被改譯取代而丟掉的舊列)。"""
    current = []
    for r in csv.DictReader(io.StringIO(export_text)):
        if not (r.get("en") or "").strip():
            continue
        current.append({"en": r["en"], "zh-tw": r["zh-tw"], "pos": r.get("pos", ""),
                        "description": r.get("description", ""),
                        "doc_url": GLOSSARY_URL, "retrieved_on": date, "trust": "官方文件"})
    cur_keys = {key(r) for r in current}
    cur_en = {r["en"].strip().lower() for r in current}
    kept, dropped = [], []
    for r in old_rows:
        if key(r) in cur_keys:
            continue
        if r["en"].strip().lower() in cur_en:
            dropped.append(r)
            continue
        kept.append({**{f: r.get(f, "") for f in FIELDS[:4]},
                     "doc_url": r.get("doc_url") or SNAPSHOT_URL,
                     "retrieved_on": r.get("retrieved_on") or SNAPSHOT_DATE,
                     "trust": r.get("trust") or "官方文件"})
    rows = current + kept
    rows.sort(key=lambda r: (r["en"].strip().lower(), r["zh-tw"]))
    return rows, kept, dropped


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="重建 data/glossary.csv")
    ap.add_argument("--from-file", help="已下載的 GlotPress 匯出 CSV")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="擷取日（預設今天）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = Path(args.from_file).read_text(encoding="utf-8-sig") if args.from_file else download()
    old = list(csv.DictReader(OUT.open(encoding="utf-8-sig"))) if OUT.exists() else []
    rows, kept, dropped = build(text, old, args.date)
    print(f"現行詞彙表 {len(rows) - len(kept)} 列；保留舊版 {len(kept)} 列；被改譯取代 {len(dropped)} 列")
    for r in dropped:
        print(f"  取代：{r['en']} 「{r['zh-tw']}」")
    if args.dry_run:
        return 0
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"已寫入 {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
