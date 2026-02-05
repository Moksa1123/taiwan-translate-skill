#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣正體中文詞彙搜尋引擎
使用 BM25 算法搜尋詞彙表

雙來源策略:
    1. WP 官方詞彙表 (glossary.csv) - 主要來源
    2. 繁化姬台灣化規則 (taiwan-terms.csv) - 備用來源

用法:
    python search.py <關鍵字> [--domain <domain>] [--limit <n>] [--format json]

範例:
    python search.py plugin
    python search.py 外掛 --domain zh
    python search.py setting --limit 20
    python search.py theme --format json
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
import math
from collections import defaultdict
from typing import List, Dict, Tuple

# BM25 parameters
K1 = 1.5
B = 0.75

def load_glossary(csv_path: str) -> List[Dict]:
    """載入 WP 官方詞彙表"""
    entries = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append({
                'en': row.get('en', ''),
                'zh': row.get('zh-tw', ''),
                'pos': row.get('pos', ''),
                'desc': row.get('description', ''),
                'source': 'wp'  # WordPress 官方
            })
    return entries


def load_taiwan_terms(csv_path: str) -> List[Dict]:
    """載入繁化姬台灣化規則"""
    entries = []
    if not os.path.exists(csv_path):
        return entries
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cn = row.get('cn', '')
            tw = row.get('tw', '')
            # 跳過相同的項目
            if cn and tw and cn != tw:
                entries.append({
                    'en': cn,  # 簡體中文作為搜尋詞
                    'zh': tw,  # 台灣正體
                    'pos': row.get('category', ''),
                    'desc': row.get('note', ''),
                    'source': 'fanhuaji'  # 繁化姬
                })
    return entries


def load_all_sources(data_dir: str) -> Tuple[List[Dict], List[Dict]]:
    """載入所有來源"""
    glossary_path = os.path.join(data_dir, 'glossary.csv')
    terms_path = os.path.join(data_dir, 'taiwan-terms.csv')

    wp_entries = load_glossary(glossary_path) if os.path.exists(glossary_path) else []
    fanhuaji_entries = load_taiwan_terms(terms_path)

    return wp_entries, fanhuaji_entries

def tokenize(text: str) -> List[str]:
    """簡單分詞（空格分割 + 小寫）"""
    return text.lower().split()

def build_index(entries: List[Dict], domain: str = 'all') -> Tuple[Dict, Dict, int, float]:
    """建立倒排索引"""
    doc_freq = defaultdict(int)  # term -> doc count
    doc_lengths = {}  # doc_id -> length
    total_length = 0

    # 建立文檔
    for i, entry in enumerate(entries):
        if domain == 'en':
            text = entry['en']
        elif domain == 'zh':
            text = entry['zh']
        else:
            text = f"{entry['en']} {entry['zh']} {entry['desc']}"

        tokens = tokenize(text)
        doc_lengths[i] = len(tokens)
        total_length += len(tokens)

        seen = set()
        for token in tokens:
            if token not in seen:
                doc_freq[token] += 1
                seen.add(token)

    avg_length = total_length / len(entries) if entries else 0
    return doc_freq, doc_lengths, len(entries), avg_length

def bm25_score(query_tokens: List[str], doc_id: int, entry: Dict,
               doc_freq: Dict, doc_lengths: Dict, n_docs: int, avg_length: float,
               domain: str = 'all') -> float:
    """計算 BM25 分數"""
    if domain == 'en':
        text = entry['en']
    elif domain == 'zh':
        text = entry['zh']
    else:
        text = f"{entry['en']} {entry['zh']} {entry['desc']}"

    doc_tokens = tokenize(text)
    doc_length = doc_lengths[doc_id]

    score = 0.0
    for token in query_tokens:
        if token not in doc_freq:
            continue

        # Term frequency in document
        tf = doc_tokens.count(token)
        if tf == 0:
            continue

        # IDF
        df = doc_freq[token]
        idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)

        # BM25 score component
        numerator = tf * (K1 + 1)
        denominator = tf + K1 * (1 - B + B * (doc_length / avg_length))
        score += idf * (numerator / denominator)

    # Exact match bonus
    query_lower = ' '.join(query_tokens)
    if entry['en'].lower() == query_lower:
        score += 10
    elif query_lower in entry['en'].lower():
        score += 5

    return score

def search(entries: List[Dict], query: str, domain: str = 'all', limit: int = 10) -> List[Dict]:
    """搜尋詞彙"""
    doc_freq, doc_lengths, n_docs, avg_length = build_index(entries, domain)
    query_tokens = tokenize(query)

    results = []
    for i, entry in enumerate(entries):
        score = bm25_score(query_tokens, i, entry, doc_freq, doc_lengths, n_docs, avg_length, domain)
        if score > 0:
            results.append({
                **entry,
                'score': round(score, 4)
            })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]

def format_results(results: List[Dict], format_type: str = 'table') -> str:
    """格式化輸出"""
    if not results:
        return "找不到相關詞彙"

    if format_type == 'json':
        return json.dumps(results, ensure_ascii=False, indent=2)

    # Table format
    lines = []
    lines.append("=" * 80)
    lines.append(f"{'英文/簡體':<25} {'台灣正體':<18} {'分類':<8} {'來源':<8}")
    lines.append("=" * 80)

    wp_count = 0
    fanhuaji_count = 0

    for r in results:
        en = r['en'][:23] + '..' if len(r['en']) > 25 else r['en']
        zh = r['zh'][:16] + '..' if len(r['zh']) > 18 else r['zh']
        pos = r['pos'][:6] if r['pos'] else '-'
        source = 'WP' if r.get('source') == 'wp' else 'FHJ'
        lines.append(f"{en:<25} {zh:<18} {pos:<8} {source:<8}")

        if r.get('source') == 'wp':
            wp_count += 1
        else:
            fanhuaji_count += 1

        if r['desc']:
            desc = r['desc'][:74] + '..' if len(r['desc']) > 76 else r['desc']
            lines.append(f"  └─ {desc}")

    lines.append("=" * 80)
    lines.append(f"共找到 {len(results)} 筆結果 (WP官方: {wp_count}, 繁化姬: {fanhuaji_count})")

    return '\n'.join(lines)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='台灣正體中文詞彙搜尋引擎 (雙來源)')
    parser.add_argument('query', help='搜尋關鍵字')
    parser.add_argument('--domain', choices=['all', 'en', 'zh'], default='all',
                        help='搜尋範圍: all=全部, en=英文, zh=中文')
    parser.add_argument('--limit', type=int, default=10, help='結果數量限制')
    parser.add_argument('--format', choices=['table', 'json'], default='table',
                        help='輸出格式')
    parser.add_argument('--source', choices=['all', 'wp', 'fanhuaji'], default='all',
                        help='來源: all=全部, wp=WP官方, fanhuaji=繁化姬')

    args = parser.parse_args()

    # Find data files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')

    # Load sources based on --source flag
    wp_entries, fanhuaji_entries = load_all_sources(data_dir)

    if args.source == 'wp':
        entries = wp_entries
    elif args.source == 'fanhuaji':
        entries = fanhuaji_entries
    else:
        # 雙來源策略: WP 優先，繁化姬補充
        entries = wp_entries + fanhuaji_entries

    if not entries:
        print("Error: No glossary data found")
        sys.exit(1)

    results = search(entries, args.query, args.domain, args.limit)
    print(format_results(results, args.format))

if __name__ == '__main__':
    main()
