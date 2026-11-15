# 台灣正體中文翻譯技能包

這是 AI 程式助手的翻譯技能包，使用 WordPress 台灣社群官方詞彙表，協助將英文軟體介面翻譯成符合台灣用語習慣的正體中文。

## 目錄結構

```
taiwan-translate/
├── SKILL.md              # 主技能文件（AI 會讀取這個）
├── CLAUDE.md             # Claude 專用說明
├── EXAMPLES.md           # 翻譯範例集
├── README.md             # 本說明文件
├── data/
│   └── glossary.csv      # WP 台灣詞彙表（筆數：scripts/check_numbers.py --stats）
├── scripts/
│   ├── search.py         # BM25 詞彙搜尋引擎
│   ├── lookup.py         # 詞彙查詢（列出命中詞彙，不代換整句）
│   └── po.py             # PO 抽取與把關（extract / validate）
└── references/
    └── STYLE_GUIDE.md    # 翻譯風格指南
```

## 使用方式

### 在 AI 助手中

```
/tw-translate plugin
/tw-translate "Please select a theme"
```

### Python 腳本

> 理念：腳本負責「查詞彙」與「把關」，整句翻譯由模型完成，**不做子字串自動代換**。

```bash
# 搜尋詞彙（BM25）
python scripts/search.py plugin
python scripts/search.py 外掛 --domain zh
python scripts/search.py theme --format json

# 詞彙查詢：列出一句話命中的詞彙（供翻譯參考，不代換整句）
python scripts/lookup.py "Click the Settings button"

# 抽出 PO 未翻譯項目（交給模型翻譯）
python scripts/po.py extract path/to/plugin.pot

# PO 翻譯把關（佔位符/首字/中國用語/空格…）
python scripts/po.py validate path/to/plugin.po
```

## 詞彙表格式

`data/glossary.csv` 包含以下欄位：

| 欄位 | 說明 |
|------|------|
| en | 英文詞彙 |
| zh-tw | 台灣正體中文翻譯 |
| pos | 詞性（noun, verb, adjective...）|
| description | 備註說明 |

## 詞彙表來源

- [WordPress 台灣漢文字彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/)
- [GitHub: WordPress-zh_TW-Glossary](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)

## 授權

MIT License
