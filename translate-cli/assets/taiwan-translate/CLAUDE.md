# CLAUDE.md

This file provides guidance to Claude Code when working with this translation skill.

## Skill Overview

Taiwan Translate Skill 是台灣正體中文翻譯工具，使用 WordPress 台灣社群官方詞彙表（2,300+ 詞彙），協助將英文軟體介面翻譯成符合台灣用語習慣的正體中文。

## Available Scripts

```bash
# 搜尋詞彙（BM25 算法）
python scripts/search.py <關鍵字>
python scripts/search.py plugin
python scripts/search.py 外掛 --domain zh
python scripts/search.py theme --format json

# 翻譯文字
python scripts/translate.py "<英文文字>"
python scripts/translate.py "Please select a theme"

# 翻譯 PO/POT 檔案
python scripts/translate.py --po path/to/file.pot
```

## File Structure

```
taiwan-translate/
├── SKILL.md              # Main skill documentation
├── EXAMPLES.md           # Translation examples
├── data/glossary.csv     # Glossary (2,300+ terms)
├── scripts/
│   ├── search.py         # BM25 search engine
│   └── translate.py      # Translation tool
└── references/
    └── STYLE_GUIDE.md    # Style guide
```

## Key Translation Rules

1. **Use Taiwan terminology** - 使用台灣用語而非中國大陸用語
   - file → 檔案（不是「文件」）
   - program → 程式（不是「程序」）
   - plugin → 外掛（不是「插件」）

2. **Language names** - 語言名稱稱「文」不稱「語」
   - English → 英文（不是「英語」）

3. **Brand names** - 品牌名稱保留英文
   - WordPress, Google, Apple

4. **Punctuation** - 使用全形標點符號
   - ，。、；：「」『』（）

## When to Use This Skill

- 翻譯 WordPress 外掛/佈景主題
- 翻譯軟體介面文字
- 查詢標準譯法
- 處理 .po/.pot 檔案
- 任何英文到台灣正體中文的翻譯需求

## Quick Reference

常用詞彙速查：

| English | 台灣正體中文 |
|---------|-------------|
| plugin | 外掛 |
| theme | 佈景主題 |
| settings | 設定 |
| dashboard | 控制台 |
| user | 使用者 |
| file | 檔案 |
| save | 儲存 |
| delete | 刪除 |
| upload | 上傳 |
| download | 下載 |
