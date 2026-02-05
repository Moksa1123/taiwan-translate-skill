<div align="center">

# Taiwan Translate Skill

**台灣正體中文翻譯技能包**

為 AI 程式助手提供專業的台灣在地化翻譯能力

[![npm version](https://img.shields.io/npm/v/taiwan-translate-skill.svg?style=flat-square&color=cb3837)](https://www.npmjs.com/package/taiwan-translate-skill)
[![npm downloads](https://img.shields.io/npm/dm/taiwan-translate-skill.svg?style=flat-square&color=blue)](https://www.npmjs.com/package/taiwan-translate-skill)
[![node](https://img.shields.io/node/v/taiwan-translate-skill.svg?style=flat-square&color=339933)](https://nodejs.org)
[![platforms](https://img.shields.io/badge/platforms-14-orange?style=flat-square)](https://github.com/Moksa1123/taiwan-translate-skill#支援的-ai-平台)
[![license](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg?style=flat-square&logo=paypal)](https://paypal.me/cccsubcom)

[安裝](#快速安裝) · [使用方式](#使用方式) · [平台支援](#支援的-ai-平台) · [詞彙表](#詞彙表)

</div>

---

## 功能特色

| 功能 | 說明 |
|------|------|
| **2,300+ 專業詞彙** | 來自 WordPress 台灣社群官方詞彙表，持續更新 |
| **14 種 AI 平台** | 支援 Claude Code、Cursor、Windsurf、Copilot 等主流 AI 助手 |
| **BM25 智能搜尋** | 高效能詞彙搜尋引擎，支援模糊匹配 |
| **自動翻譯工具** | 支援純文字和 PO/POT 檔案批次翻譯 |
| **台灣在地化** | 使用台灣正體中文用語，非中國簡轉繁 |
| **零依賴搜尋** | Python 腳本無需安裝額外套件 |

---

## 專案結構

```
taiwan-translate-skill/
├── src/                      # TypeScript 原始碼
│   ├── index.ts              # CLI 入口
│   ├── commands/             # CLI 命令
│   │   ├── init.ts           # 安裝命令
│   │   ├── list.ts           # 列出平台
│   │   ├── info.ts           # 版本資訊
│   │   ├── update.ts         # 更新命令
│   │   └── versions.ts       # 檢查版本
│   ├── types/                # TypeScript 類型定義
│   └── utils/                # 工具函式
│       ├── detect.ts         # 平台偵測
│       ├── logger.ts         # 日誌輸出
│       ├── progress.ts       # 進度顯示
│       └── template.ts       # 範本處理
├── assets/
│   ├── taiwan-translate/     # 技能包內容
│   │   ├── SKILL.md          # 主技能檔案
│   │   ├── CLAUDE.md         # Claude 專用指引
│   │   ├── EXAMPLES.md       # 翻譯範例
│   │   ├── data/
│   │   │   └── glossary.csv  # 詞彙表 (2,300+ 詞彙)
│   │   ├── scripts/
│   │   │   ├── search.py     # BM25 搜尋引擎
│   │   │   └── translate.py  # 自動翻譯工具
│   │   └── references/
│   │       └── STYLE_GUIDE.md
│   └── templates/
│       ├── base/             # 基礎範本
│       └── platforms/        # 14 種平台設定
├── dist/                     # 編譯輸出
├── package.json
└── tsconfig.json
```

---

## 快速安裝

### 自動安裝（推薦）

```bash
npx taiwan-translate-skill init
```

互動式安裝程序會自動偵測你的 AI 助手並引導安裝。

### 指定平台安裝

```bash
# 安裝到特定平台
npx taiwan-translate-skill init --ai claude
npx taiwan-translate-skill init --ai cursor
npx taiwan-translate-skill init --ai windsurf

# 安裝到所有支援的平台
npx taiwan-translate-skill init --ai all

# 全域安裝（所有專案都能用）
npx taiwan-translate-skill init --ai claude --global
```

### 全域安裝 CLI

```bash
npm install -g taiwan-translate-skill

# 然後使用
tw-translate init
tw-translate list
tw-translate info
```

---

## 使用方式

安裝完成後，在 AI 助手中使用斜線命令：

### 基本指令

| 指令 | 說明 | 範例 |
|------|------|------|
| `/tw-translate <詞彙>` | 搜尋詞彙翻譯 | `/tw-translate plugin` |
| `/tw-translate "<文字>"` | 翻譯整段文字 | `/tw-translate "Select a theme"` |
| `/tw-translate --po <檔案>` | 翻譯 PO/POT 檔案 | `/tw-translate --po zh_TW.pot` |

### 搜尋詞彙

```
/tw-translate plugin
/tw-translate dashboard
/tw-translate settings
```

**輸出範例：**
```
搜尋結果 (3 筆)

1. plugin -> 外掛
   原文: plugin
   翻譯: 外掛

2. plugins -> 外掛
   原文: plugins
   翻譯: 外掛

3. plugin editor -> 外掛編輯器
   原文: plugin editor
   翻譯: 外掛編輯器
```

### 翻譯文字

```
/tw-translate "Please select a theme from the dashboard"
```

**輸出範例：**
```
原文: Please select a theme from the dashboard
翻譯: 請從控制台選擇一個佈景主題
```

### 翻譯 PO/POT 檔案

```
/tw-translate --po path/to/your-plugin-zh_TW.pot
```

---

## Python 腳本（進階）

技能包包含 Python 腳本，可在終端機直接使用：

### 搜尋詞彙

```bash
# 搜尋英文詞彙
python scripts/search.py plugin
python scripts/search.py "post type"

# 搜尋中文詞彙
python scripts/search.py 外掛 --domain zh
python scripts/search.py 佈景主題 --domain zh

# 精確搜尋
python scripts/search.py plugin --exact

# 限制結果數量
python scripts/search.py plugin --limit 5
```

### 翻譯文字

```bash
# 翻譯單段文字
python scripts/translate.py "Please select a theme"

# 翻譯 PO 檔案
python scripts/translate.py --po path/to/file.pot

# 輸出到新檔案
python scripts/translate.py --po input.pot --output output.po
```

---

## 支援的 AI 平台

<table>
<tr>
<th>平台</th>
<th>資料夾</th>
<th>全域安裝</th>
<th>說明</th>
</tr>
<tr>
<td><b>Claude Code</b></td>
<td><code>.claude</code></td>
<td align="center">V</td>
<td>Anthropic 官方 CLI</td>
</tr>
<tr>
<td><b>Cursor</b></td>
<td><code>.cursor</code></td>
<td align="center">V</td>
<td>AI-first 程式編輯器</td>
</tr>
<tr>
<td><b>Windsurf</b></td>
<td><code>.windsurf</code></td>
<td align="center">-</td>
<td>Codeium IDE</td>
</tr>
<tr>
<td><b>Antigravity</b></td>
<td><code>.agent</code></td>
<td align="center">V</td>
<td>AI Agent 平台</td>
</tr>
<tr>
<td><b>GitHub Copilot</b></td>
<td><code>.github</code></td>
<td align="center">-</td>
<td>GitHub AI 助手</td>
</tr>
<tr>
<td><b>Kiro</b></td>
<td><code>.kiro</code></td>
<td align="center">-</td>
<td>AWS AI IDE</td>
</tr>
<tr>
<td><b>Codex</b></td>
<td><code>.codex</code></td>
<td align="center">-</td>
<td>OpenAI Codex CLI</td>
</tr>
<tr>
<td><b>Qoder</b></td>
<td><code>.qoder</code></td>
<td align="center">-</td>
<td>Qodo AI 助手</td>
</tr>
<tr>
<td><b>Roo Code</b></td>
<td><code>.roo</code></td>
<td align="center">-</td>
<td>Roo-Cline AI 助手</td>
</tr>
<tr>
<td><b>Gemini</b></td>
<td><code>.gemini</code></td>
<td align="center">-</td>
<td>Google Gemini CLI</td>
</tr>
<tr>
<td><b>Trae</b></td>
<td><code>.trae</code></td>
<td align="center">-</td>
<td>ByteDance AI IDE</td>
</tr>
<tr>
<td><b>OpenCode</b></td>
<td><code>.opencode</code></td>
<td align="center">-</td>
<td>開源 AI 編輯器</td>
</tr>
<tr>
<td><b>Continue</b></td>
<td><code>.continue</code></td>
<td align="center">-</td>
<td>開源 AI 程式助手</td>
</tr>
<tr>
<td><b>CodeBuddy</b></td>
<td><code>.codebuddy</code></td>
<td align="center">-</td>
<td>Tencent AI 助手</td>
</tr>
</table>

---

## 台灣 vs 中國用語對照

本技能包使用台灣正體中文用語，與中國簡體轉繁體不同：

| 英文 | 台灣正體 | 中國用語 |
|------|----------|----------|
| Plugin | 外掛 | 插件 |
| Theme | 佈景主題 | 主題 |
| Widget | 小工具 | 部件/小部件 |
| Dashboard | 控制台 | 儀表板 |
| Settings | 設定 | 設置 |
| Category | 分類 | 類別/分類 |
| Tag | 標籤 | 標籤 |
| Sidebar | 側邊欄 | 邊欄 |
| Shortcode | 短代碼 | 簡碼 |
| Permalink | 永久連結 | 固定連結 |
| Excerpt | 摘要 | 摘錄 |
| Featured Image | 特色圖片 | 精選圖片 |
| Custom Field | 自訂欄位 | 自定義字段 |
| Post Format | 文章格式 | 日誌形式 |

---

## 詞彙表

詞彙表來自 WordPress 台灣社群官方維護的詞彙表：

- **來源**: [WordPress 台灣漢文字彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/)
- **GitHub**: [WordPress-Taiwan/WordPress-zh_TW-Glossary](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)
- **詞彙數量**: 2,300+
- **更新頻率**: 隨 WordPress 版本更新

### 詞彙涵蓋範圍

- WordPress 核心介面
- 常見外掛設定
- 佈景主題選項
- 區塊編輯器
- REST API 相關
- 電商相關術語

---

## CLI 命令

```bash
# 顯示所有命令
tw-translate --help

# 安裝技能包（互動式）
tw-translate init

# 列出支援的平台
tw-translate list

# 顯示版本資訊
tw-translate info

# 檢查可用版本
tw-translate versions

# 更新已安裝的技能包
tw-translate update
```

---

## 常見問題

<details>
<summary><b>安裝後找不到 /tw-translate 命令？</b></summary>

請重新啟動你的 AI 助手（如 Claude Code、Cursor）。技能會在重啟後自動載入。

</details>

<details>
<summary><b>Python 腳本執行出現亂碼？</b></summary>

Windows 用戶請確保終端機使用 UTF-8 編碼：

```bash
chcp 65001
```

或在 PowerShell 中：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

</details>

<details>
<summary><b>如何更新詞彙表？</b></summary>

執行更新命令：

```bash
tw-translate update
```

或重新安裝：

```bash
npx taiwan-translate-skill@latest init --force
```

</details>

<details>
<summary><b>可以自訂詞彙嗎？</b></summary>

可以！編輯 `data/glossary.csv` 檔案，新增你的自訂詞彙：

```csv
en,zh-tw,pos,description
your-term,你的翻譯,noun,備註說明
```

</details>

<details>
<summary><b>支援哪些 PO 檔案格式？</b></summary>

支援標準的 GNU gettext 格式：
- `.po` - 翻譯檔案
- `.pot` - 翻譯模板

</details>

---

## 貢獻

歡迎提交 Issue 和 Pull Request！

- [GitHub Issues](https://github.com/Moksa1123/taiwan-translate-skill/issues)
- [Pull Requests](https://github.com/Moksa1123/taiwan-translate-skill/pulls)

### 開發

```bash
# Clone 專案
git clone https://github.com/Moksa1123/taiwan-translate-skill.git
cd taiwan-translate-skill/translate-cli

# 安裝依賴
npm install

# 編譯
npm run build

# 測試
npm run dev -- init
```

---

## 授權

MIT License

---

<div align="center">

**Made with love for Taiwan WordPress Community**

[WordPress 台灣正體中文](https://tw.wordpress.org/) | [台灣社群詞彙表](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)

</div>
