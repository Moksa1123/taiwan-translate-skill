<div align="center">

# Taiwan Translate Skill

**台灣正體中文翻譯技能包**

為 AI 程式助手提供專業的台灣在地化翻譯能力

[![npm version](https://img.shields.io/npm/v/taiwan-translate-skill.svg?style=flat-square&color=cb3837)](https://www.npmjs.com/package/taiwan-translate-skill)
[![npm downloads](https://img.shields.io/npm/dm/taiwan-translate-skill.svg?style=flat-square&color=blue)](https://www.npmjs.com/package/taiwan-translate-skill)
[![node](https://img.shields.io/node/v/taiwan-translate-skill.svg?style=flat-square&color=339933)](https://nodejs.org)
[![platforms](https://img.shields.io/badge/platforms-14-orange?style=flat-square)](#支援的-ai-平台)
[![license](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg?style=flat-square&logo=paypal)](https://paypal.me/cccsubcom)

[快速開始](#快速開始) | [功能特色](#功能特色) | [支援平台](#支援的-ai-平台) | [貢獻指南](CONTRIBUTING.md)

</div>

---

## 功能特色

| 功能 | 說明 |
|------|------|
| **2,600+ 官方詞彙** | WordPress 台灣社群官方詞彙表 |
| **雙來源策略** | WP 官方優先，繁化姬台灣化規則備用 |
| **14 種 AI 平台** | 支援 Claude Code、Cursor、Devin Desktop（原 Windsurf）、Copilot 等 |
| **BM25 智能搜尋** | 高效能詞彙搜尋引擎 |
| **PO/POT 翻譯** | 支援 WordPress 翻譯檔案格式 |

---

## 快速開始

```bash
npx taiwan-translate-skill init
```

選擇你的 AI 平台，技能包會自動安裝到對應目錄。

---

## 支援的 AI 平台

| 平台 | 說明 |
|------|------|
| `claude` | Claude Code CLI |
| `cursor` | Cursor Editor |
| `windsurf` | Devin Desktop（原 Windsurf，2026/6 改名；裝到 `.devin/`，舊版 `.windsurf/` 仍可偵測） |
| `copilot` | GitHub Copilot（Agent Skills，裝到 `.github/skills/`） |
| `antigravity` | Antigravity / Generic Agent |
| `kiro` | Kiro（AWS AI IDE） |
| `codex` | OpenAI Codex CLI |
| `qoder` | Qoder |
| `roocode` | Roo Code |
| `gemini` | Gemini CLI |
| `trae` | Trae（ByteDance AI IDE） |
| `opencode` | OpenCode |
| `continue` | Continue Extension |
| `codebuddy` | CodeBuddy |
| `all` | 安裝到所有平台 |

---

## 專案結構

```
taiwan-translate-skill/
├── translate-cli/              # NPM 套件
│   ├── src/                    # TypeScript 原始碼
│   ├── assets/
│   │   └── taiwan-translate/   # 技能包內容
│   │       ├── SKILL.md        # 主技能檔案
│   │       ├── data/
│   │       │   ├── glossary.csv      # WP 官方詞彙表
│   │       │   └── taiwan-terms.csv  # 繁化姬規則
│   │       └── scripts/
│   │           ├── search.py         # BM25 搜尋
│   │           ├── lookup.py         # 詞彙查詢（不代換整句）
│   │           └── po.py             # PO 抽取與把關
│   └── package.json
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── CLAUDE.md
```

---

## 雙來源策略

```
查詢詞彙 → WP 官方詞彙表 → 找到 → 使用 WP 官方翻譯
              ↓
            找不到
              ↓
         繁化姬台灣化規則 → 找到 → 使用繁化姬翻譯
              ↓
            找不到
              ↓
           保持原文
```

| 來源 | 優先順序 | 詞彙數量 |
|------|----------|----------|
| WP 官方 | 1 (最高) | 2,600+ |
| 繁化姬 | 2 (備用) | 130+ |

---

## 詞彙表來源

- [WordPress 台灣漢文字彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/)
- [GitHub: WordPress-zh_TW-Glossary](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)
- [繁化姬 Fanhuaji](https://github.com/Fanhuaji/Sublime-Fanhuaji)

---

## 貢獻

歡迎提交 Issue 和 Pull Request！

詳細指南請參考 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 授權

MIT License - 詳見 [LICENSE](LICENSE)

---

<div align="center">

**Made with love for Taiwan WordPress Community**

[WordPress 台灣正體中文](https://tw.wordpress.org/) | [台灣社群詞彙表](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)

</div>
