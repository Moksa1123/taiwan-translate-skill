# Taiwan Translate Skill - Claude Code 專案指南

此專案為 AI 程式助手提供台灣正體中文翻譯能力。

## 專案結構

```
taiwan-translate-skill/
├── translate-cli/              # NPM 套件（主要開發目錄）
│   ├── src/                    # TypeScript 原始碼
│   │   ├── index.ts            # CLI 入口
│   │   ├── commands/           # CLI 命令
│   │   ├── types/              # 類型定義
│   │   └── utils/              # 工具函式
│   ├── assets/
│   │   └── taiwan-translate/   # 技能包內容
│   │       ├── SKILL.md        # 主技能檔案
│   │       ├── data/           # 詞彙表
│   │       └── scripts/        # Python 工具
│   ├── dist/                   # 編譯輸出
│   └── package.json
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── CLAUDE.md                   # 此檔案
```

## 開發命令

```bash
cd translate-cli

# 安裝依賴
npm install

# 編譯 TypeScript
npm run build

# 本地測試
node dist/index.js init
node dist/index.js list
node dist/index.js info
```

## 技能包內容

### 詞彙表

- `data/glossary.csv` - WP 官方詞彙表（2,300+ 詞彙）
- `data/taiwan-terms.csv` - 繁化姬台灣化規則（130+ 詞彙）

### Python 工具

- `scripts/search.py` - BM25 詞彙搜尋引擎
- `scripts/lookup.py` - 詞彙查詢（列出命中詞彙，**不**代換整句）
- `scripts/po.py` - PO 抽取與把關（`extract` / `validate`）
- `scripts/translate.py` - **已停用**（舊版子字串自動代換會產生亂碼，導向新工具）

## 核心理念

**模型翻譯 + 腳本參考與把關。** 詞彙表僅供參考，不得用子字串自動代換翻譯整句。
標準工作流程：抽取未翻譯 → 模型翻譯（查詞彙＋規則）→ validator 把關 → 回寫。

## 雙來源策略

1. WP 官方詞彙表（優先）
2. 繁化姬台灣化規則（備用）
3. 保持原文（找不到時）

## 支援的 AI 平台

共 14 種：claude, cursor, windsurf, copilot, cline, roo, aider, continue, codegpt, cody, tabnine, amazon-q, gemini, all

## 注意事項

- TypeScript 編譯輸出到 `dist/`
- CLI 入口點是 `dist/index.js`
- 技能包安裝到各平台對應目錄
- Python 腳本無需額外依賴
