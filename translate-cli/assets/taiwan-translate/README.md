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
│   └── glossary.csv      # 詞彙表（2,300+ 詞彙）
├── scripts/
│   ├── search.py         # BM25 詞彙搜尋引擎
│   └── translate.py      # 自動翻譯工具
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

```bash
# 搜尋詞彙
python scripts/search.py plugin
python scripts/search.py 外掛 --domain zh
python scripts/search.py theme --format json

# 翻譯文字
python scripts/translate.py "Click the Settings button"

# 翻譯 PO 檔案
python scripts/translate.py --po path/to/plugin.pot
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
