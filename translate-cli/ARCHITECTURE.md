# Architecture

台灣正體中文翻譯技能包的架構說明。

## 目錄結構

```
translate-cli/
├── package.json              # npm 套件配置
├── tsconfig.json             # TypeScript 配置
├── README.md                 # 專案說明
├── ARCHITECTURE.md           # 架構說明（本文件）
│
├── src/                      # TypeScript 源碼
│   ├── index.ts              # CLI 入口點
│   ├── commands/             # CLI 命令
│   │   ├── init.ts           # 安裝命令
│   │   ├── list.ts           # 列表命令
│   │   ├── info.ts           # 資訊命令
│   │   ├── update.ts         # 更新命令
│   │   └── versions.ts       # 版本命令
│   ├── utils/                # 工具函式
│   │   ├── detect.ts         # 平台偵測
│   │   ├── logger.ts         # 日誌工具
│   │   ├── progress.ts       # 進度條
│   │   └── template.ts       # 模板處理
│   └── types/                # 類型定義
│       └── index.ts          # 類型匯出
│
├── assets/                   # 資源文件
│   ├── taiwan-translate/     # 技能包內容（Source of Truth）
│   │   ├── SKILL.md          # 主技能文件
│   │   ├── CLAUDE.md         # Claude 專用說明
│   │   ├── EXAMPLES.md       # 範例集
│   │   ├── README.md         # 技能包說明
│   │   ├── data/             # 資料檔案
│   │   │   └── glossary.csv  # 詞彙表（2,300+ 詞彙）
│   │   ├── scripts/          # Python 腳本
│   │   │   ├── search.py     # BM25 搜尋引擎
│   │   │   ├── lookup.py     # 詞彙查詢（不代換整句）
│   │   │   └── po.py         # PO 抽取與把關（extract/validate）
│   │   └── references/       # 參考文件
│   │       └── STYLE_GUIDE.md
│   │
│   └── templates/            # 平台模板
│       ├── base/             # 基礎模板
│       │   ├── skill-content.md
│       │   └── quick-reference.md
│       └── platforms/        # 平台配置（14 種）
│           ├── claude.json
│           ├── cursor.json
│           └── ...
│
├── scripts/                  # 建置腳本
│   └── build.js              # esbuild 建置
│
└── dist/                     # 編譯輸出（git ignore）
    └── index.js
```

## 資料流

```
┌─────────────────┐
│  npx tw-translate init
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  src/index.ts   │ CLI 入口
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  commands/init  │ 安裝邏輯
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────────┐
│detect │ │ template  │
└───┬───┘ └─────┬─────┘
    │           │
    ▼           ▼
┌───────────────────────┐
│ 讀取 platforms/*.json │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 複製 taiwan-translate │
│ 到目標資料夾          │
└───────────────────────┘
```

## 平台配置格式

每個平台的 JSON 配置：

```json
{
  "platform": "claude",
  "displayName": "Claude Code",
  "installType": "full",
  "folderStructure": {
    "root": ".claude",
    "skillPath": "skills/tw-translate",
    "filename": "SKILL.md",
    "globalRoot": "~/.claude"
  },
  "sections": {
    "examples": true,
    "references": true,
    "scripts": true,
    "quickReference": true
  }
}
```

## 同步規則

**Source of Truth**: `assets/taiwan-translate/`

修改檔案時：

1. **技能內容** - 修改 `assets/taiwan-translate/`：
   - `SKILL.md` - 主文件
   - `EXAMPLES.md` - 範例
   - `scripts/*.py` - Python 腳本
   - `data/glossary.csv` - 詞彙表

2. **平台配置** - 修改 `assets/templates/platforms/*.json`

3. **CLI 邏輯** - 修改 `src/`

## 建置流程

```bash
# 安裝依賴
npm install

# 建置
npm run build

# 本地測試
node dist/index.js init

# 發布
npm publish
```

## 技術棧

- **Runtime**: Node.js 18+
- **Language**: TypeScript 5.x
- **Bundler**: esbuild
- **CLI Framework**: Commander.js
- **Interactive**: Prompts
- **Styling**: Chalk
