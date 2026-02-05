#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣正體中文翻譯工具

雙來源策略:
    1. WP 官方詞彙表 (glossary.csv) - 主要來源
    2. 繁化姬台灣化規則 (taiwan-terms.csv) - 備用來源

用法:
    python translate.py "<English text>"
    python translate.py --file input.txt
    python translate.py --po path/to/file.po

範例:
    python translate.py "Please select a theme"
    python translate.py "Click the Settings button"
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
from typing import Dict, List, Tuple

def load_glossary(csv_path: str) -> Dict[str, List[Dict]]:
    """載入 WP 官方詞彙表（以英文為 key）"""
    glossary = {}
    if not os.path.exists(csv_path):
        return glossary
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            en = row.get('en', '').lower()
            if en:
                if en not in glossary:
                    glossary[en] = []
                glossary[en].append({
                    'en': row.get('en', ''),
                    'zh': row.get('zh-tw', ''),
                    'pos': row.get('pos', ''),
                    'desc': row.get('description', ''),
                    'source': 'wp'
                })
    return glossary


def load_taiwan_terms(csv_path: str) -> Dict[str, List[Dict]]:
    """載入繁化姬台灣化規則（以簡體中文為 key）"""
    terms = {}
    if not os.path.exists(csv_path):
        return terms
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cn = row.get('cn', '')
            tw = row.get('tw', '')
            # 跳過相同的項目
            if cn and tw and cn != tw:
                cn_lower = cn.lower()
                if cn_lower not in terms:
                    terms[cn_lower] = []
                terms[cn_lower].append({
                    'en': cn,  # 簡體中文作為原文
                    'zh': tw,  # 台灣正體作為譯文
                    'pos': row.get('category', ''),
                    'desc': row.get('note', ''),
                    'source': 'fanhuaji'
                })
    return terms


def merge_glossaries(wp_glossary: Dict, fanhuaji_terms: Dict) -> Dict[str, List[Dict]]:
    """合併詞彙表 (WP 優先)"""
    merged = dict(wp_glossary)  # Copy WP glossary

    # Add Fanhuaji terms that don't exist in WP
    for key, entries in fanhuaji_terms.items():
        if key not in merged:
            merged[key] = entries
        # If key exists in WP, WP takes priority (don't add Fanhuaji)

    return merged

def find_terms(text: str, glossary: Dict) -> List[Dict]:
    """在文本中找出詞彙表中的詞彙"""
    found = []
    text_lower = text.lower()

    # Sort by length (longer terms first) to match compound terms
    sorted_terms = sorted(glossary.keys(), key=len, reverse=True)

    for term in sorted_terms:
        if term in text_lower:
            entries = glossary[term]
            for entry in entries:
                found.append(entry)
            # Mark as found (simple approach)
            text_lower = text_lower.replace(term, ' ' * len(term))

    return found

def translate_text(text: str, glossary: Dict) -> Tuple[str, List[Dict]]:
    """翻譯文本"""
    found_terms = find_terms(text, glossary)

    # Build translation suggestions
    translations = []
    result = text

    for entry in found_terms:
        # Replace English with Chinese (case insensitive)
        pattern = re.compile(re.escape(entry['en']), re.IGNORECASE)
        result = pattern.sub(entry['zh'], result)
        translations.append(entry)

    return result, translations

def format_output(original: str, translated: str, terms: List[Dict]) -> str:
    """格式化輸出"""
    lines = []
    lines.append(f"\n原文：{original}")
    lines.append(f"譯文：{translated}")

    if terms:
        lines.append("\n詞彙對照：")
        lines.append("-" * 70)
        lines.append(f"{'原文':<22} {'台灣正體':<14} {'分類':<8} {'來源':<8}")
        lines.append("-" * 70)
        seen = set()
        wp_count = 0
        fanhuaji_count = 0
        for t in terms:
            key = f"{t['en']}:{t['zh']}"
            if key not in seen:
                seen.add(key)
                en = t['en'][:20] + '..' if len(t['en']) > 22 else t['en']
                zh = t['zh'][:12] + '..' if len(t['zh']) > 14 else t['zh']
                pos = t['pos'][:6] if t['pos'] else '-'
                source = 'WP' if t.get('source') == 'wp' else 'FHJ'
                lines.append(f"{en:<22} {zh:<14} {pos:<8} {source:<8}")
                if t.get('source') == 'wp':
                    wp_count += 1
                else:
                    fanhuaji_count += 1
        lines.append("-" * 70)
        lines.append(f"詞彙來源統計: WP官方 {wp_count}, 繁化姬 {fanhuaji_count}")

    return '\n'.join(lines)

def translate_po_file(po_path: str, glossary: Dict) -> Tuple[int, int]:
    """翻譯 .po 檔案"""
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse PO file
    entries = re.findall(r'msgid "(.*?)"\nmsgstr "(.*?)"', content, re.DOTALL)

    translated_count = 0
    total_empty = 0

    new_content = content
    for msgid, msgstr in entries:
        if not msgstr.strip() and msgid.strip():
            total_empty += 1
            translated, _ = translate_text(msgid, glossary)
            if translated != msgid:
                old = f'msgid "{msgid}"\nmsgstr "{msgstr}"'
                new = f'msgid "{msgid}"\nmsgstr "{translated}"'
                new_content = new_content.replace(old, new)
                translated_count += 1

    # Write back
    output_path = po_path.replace('.po', '-translated.po')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return translated_count, total_empty

def main():
    import argparse

    parser = argparse.ArgumentParser(description='台灣正體中文翻譯工具 (雙來源)')
    parser.add_argument('text', nargs='?', help='要翻譯的文字')
    parser.add_argument('--file', help='輸入文字檔案')
    parser.add_argument('--po', help='翻譯 PO 檔案')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='輸出格式')

    args = parser.parse_args()

    # Find glossary files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    glossary_path = os.path.join(data_dir, 'glossary.csv')
    terms_path = os.path.join(data_dir, 'taiwan-terms.csv')

    # Load both sources
    wp_glossary = load_glossary(glossary_path)
    fanhuaji_terms = load_taiwan_terms(terms_path)

    # Merge with WP priority
    glossary = merge_glossaries(wp_glossary, fanhuaji_terms)

    if not glossary:
        print("Error: No glossary data found")
        sys.exit(1)

    if args.po:
        if not os.path.exists(args.po):
            print(f"Error: File not found: {args.po}")
            sys.exit(1)
        translated, total = translate_po_file(args.po, glossary)
        output_path = args.po.replace('.po', '-translated.po')
        print(f"\n翻譯完成！")
        print(f"  空白條目：{total}")
        print(f"  已翻譯：{translated}")
        print(f"  輸出檔案：{output_path}")

    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
        translated, terms = translate_text(text, glossary)
        print(format_output(text, translated, terms))

    elif args.text:
        translated, terms = translate_text(args.text, glossary)
        if args.format == 'json':
            print(json.dumps({
                'original': args.text,
                'translated': translated,
                'terms': terms
            }, ensure_ascii=False, indent=2))
        else:
            print(format_output(args.text, translated, terms))

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
