#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PO/POT 檔案工具：抽取未翻譯項目 + 翻譯把關（validator）

設計理念：
    本工具「不」翻譯整句。整句翻譯由模型完成（查 lookup.py 詞彙 + 風格指南），
    再用本工具 validate 把關。

子命令：
    extract   抽出未翻譯的 msgid 清單（保留多行/複數/msgctxt/行號），交給模型翻譯
    validate  掃描一份 .po，回報問題（佔位符/首字大小寫/空譯/中國用語/空格…），只報告不改

用法：
    python po.py extract  path/to/file.po
    python po.py extract  path/to/file.po --format json
    python po.py validate path/to/file.po
    python po.py validate path/to/file.po --format json

參考：對齊 Loco Translate / gettext 的常見檢查，並加上台灣中文專屬規則。
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
import argparse
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# PO 解析（健全版）
# ---------------------------------------------------------------------------

# 將 PO 字串字面值中的跳脫序列還原
_UNESCAPE = {
    '\\n': '\n', '\\t': '\t', '\\r': '\r',
    '\\"': '"', '\\\\': '\\',
}
_UNESCAPE_RE = re.compile(r'\\[ntr"\\]')


def _unescape(s: str) -> str:
    return _UNESCAPE_RE.sub(lambda m: _UNESCAPE[m.group(0)], s)


def _extract_quoted(line: str) -> Optional[str]:
    """從 `keyword "..."` 或裸 `"..."` 續行中取出引號內字面值並還原跳脫。"""
    m = re.search(r'"((?:[^"\\]|\\.)*)"', line)
    if m is None:
        return None
    return _unescape(m.group(1))


class POEntry:
    __slots__ = ('line', 'comments', 'flags', 'msgctxt',
                 'msgid', 'msgid_plural', 'msgstr', 'msgstr_plural')

    def __init__(self):
        self.line = 0
        self.comments: List[str] = []
        self.flags: List[str] = []
        self.msgctxt: Optional[str] = None
        self.msgid: str = ''
        self.msgid_plural: Optional[str] = None
        self.msgstr: str = ''
        self.msgstr_plural: Dict[int, str] = {}

    @property
    def is_header(self) -> bool:
        return self.msgid == '' and self.msgctxt is None

    @property
    def is_plural(self) -> bool:
        return self.msgid_plural is not None

    def translations(self) -> List[str]:
        """回傳所有實際譯文（複數展開）。"""
        if self.is_plural:
            return [self.msgstr_plural[k] for k in sorted(self.msgstr_plural)]
        return [self.msgstr]

    def is_untranslated(self) -> bool:
        if self.is_header:
            return False
        if self.is_plural:
            vals = self.msgstr_plural.values()
            return any(not v.strip() for v in vals) or len(vals) == 0
        return not self.msgstr.strip()


def parse_po(path: str) -> List[POEntry]:
    """逐行解析 PO，支援多行字串 / msgctxt / msgid_plural / msgstr[n] / 跳脫。"""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries: List[POEntry] = []
    entry = POEntry()
    started = False
    # 目前正在累加哪個欄位的多行字串：'msgctxt'/'msgid'/'msgid_plural'/'msgstr'/('msgstr', n)
    current = None
    plural_idx = None

    def flush():
        nonlocal entry, started, current, plural_idx
        if started:
            entries.append(entry)
        entry = POEntry()
        started = False
        current = None
        plural_idx = None

    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip('\n')
        stripped = line.strip()

        if stripped == '':
            flush()
            continue

        if stripped.startswith('#'):
            # 新項目的註解；若先前已累積譯文欄位，視為新項目開始
            if started and current is not None:
                flush()
            if not started:
                started = True
                entry.line = lineno
            if stripped.startswith('#,'):
                entry.flags.extend(
                    f.strip() for f in stripped[2:].split(',') if f.strip())
            else:
                entry.comments.append(stripped)
            current = None
            continue

        if stripped.startswith('msgctxt'):
            if started and current in ('msgstr',) or (
                    started and isinstance(current, tuple)):
                flush()
            if not started:
                started = True
                entry.line = lineno
            entry.msgctxt = _extract_quoted(stripped) or ''
            current = 'msgctxt'
            continue

        if stripped.startswith('msgid_plural'):
            entry.msgid_plural = _extract_quoted(stripped) or ''
            current = 'msgid_plural'
            continue

        if stripped.startswith('msgid'):
            if started and (current == 'msgstr' or isinstance(current, tuple)):
                flush()
            if not started:
                started = True
                entry.line = lineno
            entry.msgid = _extract_quoted(stripped) or ''
            current = 'msgid'
            continue

        if stripped.startswith('msgstr['):
            m = re.match(r'msgstr\[(\d+)\]', stripped)
            idx = int(m.group(1)) if m else 0
            entry.msgstr_plural[idx] = _extract_quoted(stripped) or ''
            current = ('msgstr', idx)
            plural_idx = idx
            continue

        if stripped.startswith('msgstr'):
            entry.msgstr = _extract_quoted(stripped) or ''
            current = 'msgstr'
            continue

        # 裸引號續行 "..."（多行字串）
        if stripped.startswith('"'):
            val = _extract_quoted(stripped) or ''
            if current == 'msgctxt':
                entry.msgctxt = (entry.msgctxt or '') + val
            elif current == 'msgid':
                entry.msgid += val
            elif current == 'msgid_plural':
                entry.msgid_plural = (entry.msgid_plural or '') + val
            elif current == 'msgstr':
                entry.msgstr += val
            elif isinstance(current, tuple):
                entry.msgstr_plural[plural_idx] += val
            continue

    flush()
    return entries


# ---------------------------------------------------------------------------
# extract：抽出未翻譯 msgid
# ---------------------------------------------------------------------------

def cmd_extract(path: str, fmt: str) -> int:
    entries = parse_po(path)
    todo = [e for e in entries if e.is_untranslated()]

    if fmt == 'json':
        out = []
        for e in todo:
            item = {'line': e.line, 'msgid': e.msgid}
            if e.msgctxt is not None:
                item['msgctxt'] = e.msgctxt
            if e.is_plural:
                item['msgid_plural'] = e.msgid_plural
            out.append(item)
        print(json.dumps({
            'file': path,
            'total': len(entries),
            'untranslated': len(todo),
            'items': out,
        }, ensure_ascii=False, indent=2))
        return 0

    print(f"\n檔案：{path}")
    print(f"條目總數：{len(entries)}（不含標頭），未翻譯：{len(todo)}")
    print("=" * 72)
    if not todo:
        print("沒有未翻譯的項目。")
        return 0
    for e in todo:
        print(f"\n[L{e.line}]")
        if e.msgctxt:
            print(f"  msgctxt: {e.msgctxt}")
        print(f"  msgid: {e.msgid!r}")
        if e.is_plural:
            print(f"  msgid_plural: {e.msgid_plural!r}")
    print("\n" + "=" * 72)
    print("請由模型依風格指南翻譯以上 msgid（可先用 lookup.py 查詞彙），再回寫並用 validate 把關。")
    return 0


# ---------------------------------------------------------------------------
# validate：把關（只報告不改）
# ---------------------------------------------------------------------------

# printf 風格佔位符：%s %d %1$s %02d %.2f %% 等
# 註：旗標字元集刻意排除空格旗標（" "），否則英文散文中的「% of」「% the」
#     會被誤判為 "% o" 佔位符（空格旗標在 WP i18n 幾乎不會用到）。
_PLACEHOLDER_RE = re.compile(r'%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[bcdeEfFgGosuxX%]')
# HTML 標籤
_TAG_RE = re.compile(r'</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*?)?/?>')
# 句尾標點（半形 + 全形）
_END_PUNCT = '.:!?…。：！？'
# CJK 範圍
_CJK = r'一-鿿㐀-䶿'
# 中英相鄰（缺半形空格）
_CJK_ASCII_RE = re.compile(
    rf'(?:[{_CJK}][A-Za-z0-9]|[A-Za-z0-9][{_CJK}])')
# 全形字後接半形標點
_HALF_PUNCT_AFTER_CJK_RE = re.compile(rf'[{_CJK}][,.:;!?]')


def _placeholders(s: str) -> List[str]:
    return sorted(p for p in _PLACEHOLDER_RE.findall(s) if p != '%%')


def _norm_tag(t: str) -> str:
    # 只取標籤「簽章」：標籤名稱 + 是否為結束標籤/自閉合標籤，**忽略屬性內容**。
    # 因為翻譯 title／alt／placeholder／aria-label 等屬性文字是正常且應該做的，
    # 不應被誤判為「標籤不一致」；真正要抓的是「標籤被刪掉或新增」。
    name_m = re.match(r'</?\s*([a-zA-Z][a-zA-Z0-9]*)', t)
    name = name_m.group(1).lower() if name_m else t.strip().lower()
    closing = '/' if t.lstrip().startswith('</') else ''
    selfclose = '/' if t.rstrip().endswith('/>') else ''
    return closing + name + selfclose


def _tags(s: str) -> List[str]:
    return sorted(_norm_tag(t) for t in _TAG_RE.findall(s))


# 高精確度的「中國用語」對照清單（用於 validate 的雜訊極小化）。
#
# 為何不直接掃 taiwan-terms.csv：
#     該 CSV 是「繁化姬」整篇轉換用規則，內含大量「正體→正體」的單字用詞偏好
#     （例：類→類別、庫→函式庫、對象→物件）。以子字串比對掃描，會在完全正確的
#     台灣用語中誤判（分類、媒體庫、回覆對象…），製造大量假警報——這正是舊版
#     translate.py 子字串比對的同一個坑。
#
# 因此這裡改用「人工精選、可安全子字串比對」的清單：
#     1. 含簡體字者：正體譯文本就不該出現簡體字，子字串比對 100% 安全。
#     2. 少數正體字形但語意明確的中國科技用語（軟件/硬件/插件…），在 WP 介面語境
#        不致與台灣常用詞衝突。
# 仍刻意排除在台灣為合法詞、會造成誤判的多義詞：
#     文件（=document）、程序（=procedure）、質量（=mass）、視頻/網絡之正體歧義等。
_CHINA_TERMS: List[tuple] = [
    # 含簡體字（安全）
    ("主题", "佈景主題"), ("软件", "軟體"), ("硬件", "硬體"), ("数据", "資料"),
    ("服务器", "伺服器"), ("默认", "預設"), ("视频", "影片"), ("音频", "音訊"),
    ("文件夹", "資料夾"), ("鼠标", "滑鼠"), ("质量", "品質"), ("缓存", "快取"),
    ("卸载", "解除安裝"), ("安装", "安裝"), ("网络", "網路"), ("用户", "使用者"),
    ("设置", "設定"), ("屏幕", "螢幕"), ("字体", "字型"), ("内存", "記憶體"),
    ("登录", "登入"), ("注册", "註冊"), ("邮箱", "信箱"), ("复制", "複製"),
    ("粘贴", "貼上"), ("剪贴板", "剪貼簿"), ("打印", "列印"), ("下载", "下載"),
    ("上传", "上傳"), ("链接", "連結"), ("图片", "圖片"), ("帮助", "說明"),
    ("确认", "確認"), ("启用", "啟用"), ("保存", "儲存"),
    ("当前", "目前"), ("访问", "存取"), ("权限", "權限"), ("队列", "佇列"),
    # 註：不收錄「禁用」——在台灣為合法詞（禁用字詞＝disallowed words），非中國用語。
    # 正體字形、語意明確的中國科技用語（WP 介面語境安全）
    ("插件", "外掛"), ("軟件", "軟體"), ("硬件", "硬體"), ("郵件", "郵件"),
]
# 防禦：移除任何 cn 與 tw 相同、或 cn 為 tw 子字串（屬用詞展開而非中國用語）者。
_CHINA_TERMS = [(cn, tw) for (cn, tw) in _CHINA_TERMS if cn != tw and cn not in tw]
_CHINA_TERMS.sort(key=lambda p: len(p[0]), reverse=True)


def load_china_terms(data_dir: str) -> List[tuple]:
    """回傳高精確度的 (中國用語, 台灣用語) 掃描清單（精選，非整份 CSV）。"""
    return _CHINA_TERMS


def _leading_ws(s: str) -> str:
    m = re.match(r'^\s*', s)
    return m.group(0) if m else ''


def _trailing_ws(s: str) -> str:
    m = re.search(r'\s*$', s)
    return m.group(0) if m else ''


def validate_entry(e: POEntry, china_terms: List[tuple]) -> List[Dict]:
    """回傳單一項目的問題清單。"""
    issues: List[Dict] = []

    def add(level, code, msg):
        issues.append({'line': e.line, 'level': level, 'code': code,
                       'msgid': e.msgid, 'msg': msg})

    src = e.msgid
    targets = e.translations()

    # 空譯
    if e.is_untranslated():
        # 原文本身只有空白（如 " " 間隔字串）時，譯文為空白/空是合理的，不算未翻譯。
        if src.strip() == '':
            return issues
        add('error', 'empty', '未翻譯（msgstr 為空）')
        return issues  # 空譯就不再做其他比對

    for tgt in targets:
        if not tgt.strip():
            continue

        # --- B-1 通用檢查 ---
        # 佔位符對齊
        if _placeholders(src) != _placeholders(tgt):
            add('error', 'placeholder',
                f"佔位符不一致：原文 {_placeholders(src)} ≠ 譯文 {_placeholders(tgt)}")

        # HTML 標籤對齊
        if _tags(src) != _tags(tgt):
            add('warning', 'html-tag',
                f"HTML 標籤不一致：原文 {_tags(src)} ≠ 譯文 {_tags(tgt)}")

        # 首尾空白一致
        if _leading_ws(src) != _leading_ws(tgt):
            add('warning', 'leading-space', '開頭空白/換行與原文不一致')
        if _trailing_ws(src) != _trailing_ws(tgt):
            add('warning', 'trailing-space', '結尾空白/換行與原文不一致')

        # 結尾標點
        s_strip, t_strip = src.rstrip(), tgt.rstrip()
        if s_strip and t_strip:
            if s_strip[-1] in _END_PUNCT and t_strip[-1] not in _END_PUNCT:
                add('warning', 'end-punct',
                    f"原文以「{s_strip[-1]}」結尾，譯文缺少對應標點（建議全形）")

        # 首字大小寫（Loco：missing the initial lowercase）
        if s_strip and t_strip:
            if s_strip[0].islower() and s_strip[0].isascii() \
                    and t_strip[0].isupper() and t_strip[0].isascii():
                add('warning', 'initial-lowercase',
                    "原文以小寫字母開頭，譯文卻以大寫英文起頭"
                    "（Loco 會警告 missing the initial lowercase，建議改以中文字或符號開頭）")

        # --- B-2 台灣中文專屬檢查 ---
        # 中國用語
        hit = []
        for cn, tw in china_terms:
            if cn in tgt:
                hit.append(f"{cn}→{tw}")
        if hit:
            shown = '、'.join(hit[:6]) + ('…' if len(hit) > 6 else '')
            add('warning', 'china-term', f"疑似中國用語：{shown}")

        # 先移除佔位符與 HTML 標籤，避免把 %1$s/%2$s 的尾字母（如 "s表"）或標籤
        # 誤判為「中英相鄰缺空格」。佔位符多會被換成連結/數值，其邊界不需要空格。
        tgt_clean = _TAG_RE.sub(' ', _PLACEHOLDER_RE.sub(' ', tgt))

        # 中英之間缺半形空格
        m = _CJK_ASCII_RE.search(tgt_clean)
        if m:
            add('info', 'cjk-space',
                f"中英/數字相鄰處可能缺半形空格（近「{m.group(0)}」）")

        # 全形字後接半形標點
        m = _HALF_PUNCT_AFTER_CJK_RE.search(tgt_clean)
        if m:
            add('info', 'fullwidth-punct',
                f"中文後疑似誤用半形標點（近「{m.group(0)}」，建議全形）")

    return issues


def check_consistency(entries: List[POEntry]) -> List[Dict]:
    """用詞一致性：相同 (msgctxt, msgid) 卻有不同 msgstr。"""
    issues = []
    seen: Dict[tuple, Dict] = {}
    for e in entries:
        if e.is_header or e.is_untranslated() or e.is_plural:
            continue
        key = (e.msgctxt or '', e.msgid)
        if key in seen:
            prev = seen[key]
            if prev['msgstr'] != e.msgstr:
                issues.append({
                    'line': e.line, 'level': 'warning', 'code': 'inconsistent',
                    'msgid': e.msgid,
                    'msg': f"相同原文有不同譯文：L{prev['line']} 「{prev['msgstr']}」 "
                           f"vs L{e.line} 「{e.msgstr}」",
                })
        else:
            seen[key] = {'line': e.line, 'msgstr': e.msgstr}
    return issues


_LEVEL_ORDER = {'error': 0, 'warning': 1, 'info': 2}
_LEVEL_LABEL = {'error': '錯誤', 'warning': '警告', 'info': '提示'}


def cmd_validate(path: str, fmt: str) -> int:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    china_terms = load_china_terms(data_dir)
    entries = parse_po(path)

    all_issues: List[Dict] = []
    for e in entries:
        if e.is_header:
            continue
        all_issues.extend(validate_entry(e, china_terms))
    all_issues.extend(check_consistency(entries))

    counts = {'error': 0, 'warning': 0, 'info': 0}
    for i in all_issues:
        counts[i['level']] += 1

    if fmt == 'json':
        print(json.dumps({
            'file': path,
            'total': len([e for e in entries if not e.is_header]),
            'counts': counts,
            'issues': sorted(all_issues, key=lambda x: (x['line'], _LEVEL_ORDER[x['level']])),
        }, ensure_ascii=False, indent=2))
        return 0

    print(f"\n檔案：{path}")
    print(f"條目：{len([e for e in entries if not e.is_header])}")
    print(f"問題：錯誤 {counts['error']}，警告 {counts['warning']}，提示 {counts['info']}")
    print("=" * 72)
    if not all_issues:
        print("沒有發現問題。")
        return 0
    for i in sorted(all_issues, key=lambda x: (x['line'], _LEVEL_ORDER[x['level']])):
        label = _LEVEL_LABEL[i['level']]
        mid = i['msgid'][:40] + '…' if len(i['msgid']) > 42 else i['msgid']
        print(f"[L{i['line']}] {label}({i['code']}): {i['msg']}")
        print(f"        原文：{mid!r}")
    print("=" * 72)
    print("提示：validator 只報告不修改，是否套用由模型／人判斷。")
    return 0


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='PO/POT 抽取與把關工具（不翻譯整句）')
    sub = parser.add_subparsers(dest='command')

    p_ext = sub.add_parser('extract', help='抽出未翻譯的 msgid 清單')
    p_ext.add_argument('po', help='PO/POT 檔案路徑')
    p_ext.add_argument('--format', choices=['text', 'json'], default='text')

    p_val = sub.add_parser('validate', help='翻譯把關（佔位符/首字/用語/空格…）')
    p_val.add_argument('po', help='PO 檔案路徑')
    p_val.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    if args.command in ('extract', 'validate'):
        if not os.path.exists(args.po):
            print(f"Error: File not found: {args.po}")
            sys.exit(1)

    if args.command == 'extract':
        sys.exit(cmd_extract(args.po, args.format))
    elif args.command == 'validate':
        sys.exit(cmd_validate(args.po, args.format))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
