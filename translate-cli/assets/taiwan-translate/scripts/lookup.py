#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣正體中文「詞彙查詢」工具（lookup-only）

設計理念：
    詞彙表的用途是「確保用詞一致的參考」，不是拿來做整句機器翻譯。
    本工具只「列出一句話命中的詞彙與建議譯法」供模型／人翻譯時參考，
    絕不回傳代換後的整句（避免子字串誤代換產生亂碼）。

    整句翻譯請交給模型完成，再用 po.py validate 把關。

雙來源策略:
    1. WP 官方詞彙表 (glossary.csv) - 主要來源
    2. 繁化姬台灣化規則 (taiwan-terms.csv) - 備用來源

用法:
    python lookup.py "<text>"
    python lookup.py "Please select a theme"
    python lookup.py --file input.txt
    python lookup.py "Click Settings" --format json

注意：
    本工具「不」翻譯整句，只列出命中的詞彙建議。
"""

import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import csv
import json
import re
from typing import Dict, List


def load_glossary(csv_path: str) -> Dict[str, List[Dict]]:
    """載入 WP 官方詞彙表（以英文小寫為 key）"""
    glossary: Dict[str, List[Dict]] = {}
    if not os.path.exists(csv_path):
        return glossary
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            en = (row.get('en', '') or '').strip()
            if not en:
                continue
            key = en.lower()
            glossary.setdefault(key, []).append({
                'en': en,
                'zh': row.get('zh-tw', ''),
                'pos': row.get('pos', ''),
                'desc': row.get('description', ''),
                'source': 'wp',
            })
    return glossary


def load_taiwan_terms(csv_path: str) -> Dict[str, List[Dict]]:
    """載入繁化姬台灣化規則（以簡體中文為 key）"""
    terms: Dict[str, List[Dict]] = {}
    if not os.path.exists(csv_path):
        return terms
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cn = (row.get('cn', '') or '').strip()
            tw = (row.get('tw', '') or '').strip()
            if cn and tw and cn != tw:
                terms.setdefault(cn, []).append({
                    'en': cn,            # 簡體中文作為原文
                    'zh': tw,            # 台灣正體作為譯文
                    'pos': row.get('category', ''),
                    'desc': row.get('note', ''),
                    'source': 'fanhuaji',
                })
    return terms


def lookup_terms(text: str, glossary: Dict[str, List[Dict]],
                 taiwan_terms: Dict[str, List[Dict]]) -> List[Dict]:
    """
    在文本中找出命中的詞彙（lookup-only，不做任何代換）。

    英文詞彙以「單字邊界」比對，避免：
        bug → 連 debug 也中
        nd  → 嵌在其他單字中誤匹配
        spam → 整個被換掉
    比對成功不重組句子，只回傳命中的詞彙清單。
    """
    found: List[Dict] = []
    seen = set()

    # --- 英文詞彙（單字邊界比對，較長者優先）---
    text_lower = text.lower()
    for term in sorted(glossary.keys(), key=len, reverse=True):
        # 邊界：前後不可為英數字（含 . _ 視為單字一部分由 \w 處理）
        pattern = r'(?<![A-Za-z0-9])' + re.escape(term) + r'(?![A-Za-z0-9])'
        if re.search(pattern, text_lower):
            for entry in glossary[term]:
                key = (entry['en'], entry['zh'], entry['source'])
                if key not in seen:
                    seen.add(key)
                    found.append(entry)

    # --- 簡體中文用語（直接子字串比對，中文無單字邊界問題）---
    for term in sorted(taiwan_terms.keys(), key=len, reverse=True):
        if term in text:
            for entry in taiwan_terms[term]:
                key = (entry['en'], entry['zh'], entry['source'])
                if key not in seen:
                    seen.add(key)
                    found.append(entry)

    return found


def format_output(original: str, terms: List[Dict]) -> str:
    """格式化輸出（只列詞彙，不輸出整句譯文）"""
    lines = []
    lines.append(f"\n原文：{original}")

    if not terms:
        lines.append("\n（詞彙表中找不到命中的詞彙，請依風格指南由模型翻譯）")
        return '\n'.join(lines)

    lines.append("\n命中詞彙（僅供翻譯參考，整句翻譯請由模型完成）：")
    lines.append("-" * 72)
    lines.append(f"{'原文':<22} {'台灣正體':<14} {'分類':<8} {'來源':<6}")
    lines.append("-" * 72)
    wp_count = fanhuaji_count = 0
    for t in terms:
        en = t['en'][:20] + '..' if len(t['en']) > 22 else t['en']
        zh = t['zh'][:12] + '..' if len(t['zh']) > 14 else t['zh']
        pos = t['pos'][:6] if t['pos'] else '-'
        source = 'WP' if t.get('source') == 'wp' else 'FHJ'
        lines.append(f"{en:<22} {zh:<14} {pos:<8} {source:<6}")
        if t.get('source') == 'wp':
            wp_count += 1
        else:
            fanhuaji_count += 1
    lines.append("-" * 72)
    lines.append(f"詞彙來源統計: WP官方 {wp_count}, 繁化姬 {fanhuaji_count}")
    lines.append("提示：本工具不代換整句，請依命中詞彙與風格指南翻譯。")
    return '\n'.join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='台灣正體中文詞彙查詢工具（lookup-only，不做整句代換）')
    parser.add_argument('text', nargs='?', help='要查詢的文字')
    parser.add_argument('--file', help='輸入文字檔案')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='輸出格式')

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    glossary = load_glossary(os.path.join(data_dir, 'glossary.csv'))
    taiwan_terms = load_taiwan_terms(os.path.join(data_dir, 'taiwan-terms.csv'))

    if not glossary and not taiwan_terms:
        print("Error: No glossary data found")
        sys.exit(1)

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return

    terms = lookup_terms(text, glossary, taiwan_terms)

    if args.format == 'json':
        print(json.dumps({
            'original': text,
            'terms': terms,
            'note': 'lookup-only：本工具不代換整句，整句翻譯請由模型完成。',
        }, ensure_ascii=False, indent=2))
    else:
        print(format_output(text, terms))


if __name__ == '__main__':
    main()
