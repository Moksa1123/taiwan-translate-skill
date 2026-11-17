<h1 align="center">Taiwan Translate Skill</h1>

<h3 align="center">台灣正體中文翻譯技能包</h3>

<p align="center">
  <strong>WordPress 台灣詞彙表 · 中國用語改台灣用語 · .po／.pot 把關</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/python-3-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/glossary-2627-success?style=flat-square" alt="詞彙表">
  <img src="https://img.shields.io/badge/Taiwan%20terms-135-success?style=flat-square" alt="台灣用語對照">
  <img src="https://img.shields.io/badge/AI%20platforms-14-orange?style=flat-square" alt="AI 平台">
  <a href="https://www.npmjs.com/package/taiwan-translate-skill"><img src="https://img.shields.io/npm/v/taiwan-translate-skill?style=flat-square&color=cb3837&logo=npm&logoColor=white&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/taiwan-translate-skill"><img src="https://img.shields.io/npm/dm/taiwan-translate-skill?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm downloads"></a>
  <a href="https://github.com/Moksa1123/taiwan-translate-skill"><img src="https://img.shields.io/github/stars/Moksa1123/taiwan-translate-skill?style=flat-square&logo=github&logoColor=white&color=181717" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
  <a href="https://paypal.me/cccsubcom"><img src="https://img.shields.io/badge/PayPal-支持開發-00457C?style=flat-square&logo=paypal&logoColor=white" alt="PayPal"></a>
</p>

<p align="center"><a href="README.md">English</a> · <strong>正體中文</strong></p>

> 本專案是非官方的社群專案，不是 WordPress 基金會、WordPress 台灣翻譯團隊或繁化姬製作，也與他們無關。本專案讀取他們公開的詞彙表與轉換結果，不附帶他們的軟體。

## 功能

讓 AI 助手使用 WordPress 台灣社群官方詞彙表，外掛、佈景主題和軟體介面字串照台灣用語翻，不會變成中國用語或機器猜的譯法。

| 項目 | 內容 |
|---|---|
| 詞彙表 | 2,627 列詞彙，來自 WordPress 台灣 GlotPress 詞彙表：現行 2,566 列，2024-03-22 GitHub 快照留存 61 列；每列附出處網址、擷取日期與可信度 |
| 中國用語 → 台灣用語 | 135 組用語對照（設置 → 設定、插件 → 外掛）：繁化姬台灣化轉換器實測 76、官方文件 30、站內風格 29 |
| 查詞 | `search.py` 用英文或中文查；`lookup.py` 列出一句話裡所有命中的詞。兩者都不改寫句子：整句由模型翻，詞彙表負責用詞一致 |
| .po／.pot | `po.py extract` 抽出未翻譯項目（複數、msgctxt、多行）；`po.py validate` 檢查佔位符、空譯、標點、中國用語，有錯就回 1 |
| 安裝工具 | `tw-translate init` 把 skill 裝進 14 種 AI 工具（Claude Code、Cursor、Codex、Gemini CLI、Copilot 等） |

模型先查再答。詞彙表查不到時照實說，並把問題記進 `data/pending.csv`，不自己編一個「標準譯法」。

## 適用情境

| 適用 | 不適用，改用 |
|---|---|
| 英文 → 台灣正體中文：WordPress 外掛、佈景主題、軟體介面 | 寫 WordPress 中文文章、SEO → `rankmath-seo-wp` |
| 翻譯或檢查 `.po`／`.pot`、處理 Loco Translate 警告 | 整篇簡轉繁、沒有軟體用語 → 繁化姬網站 |
| 「X 在 WordPress 台灣社群怎麼翻？」 | 法律、醫療等專業文件：詞彙表不涵蓋 |
| 把中國用語（設置、默認、插件）改成台灣用語 | |

## 安裝

| 需求 | 用途 |
|---|---|
| Python 3（只用標準函式庫） | 查詞、lookup、`.po` 工具 |
| Node.js 18 以上 | 只有 `tw-translate` 安裝工具（npx）需要 |
| Windows、macOS 或 Linux | 全部 |

### Step 1：選一種安裝方式

Claude plugin（Claude Code；上架 Claude 目錄後也可從目錄加入）：

```
/plugin marketplace add Moksa1123/taiwan-translate-skill
/plugin install taiwan-translate@taiwan-translate-skill
```

npx（Claude Code 和下表其他 AI 工具）：

```bash
npx taiwan-translate-skill@1.3.0 init                 # 互動式選平台
npx taiwan-translate-skill@1.3.0 init --ai claude --global
```

手動複製：

```bash
git clone https://github.com/Moksa1123/taiwan-translate-skill.git
cp -r taiwan-translate-skill/translate-cli/assets/taiwan-translate ~/.claude/skills/tw-translate
```

| 平台 | `--ai` 參數 | 資料夾 | 全域安裝 |
|---|---|---|---|
| Claude Code | `claude` | `.claude` | 可 |
| Cursor | `cursor` | `.cursor` | 可 |
| Devin Desktop（原 Windsurf） | `windsurf` | `.devin`（舊版 `.windsurf` 仍可偵測） | 不可 |
| Antigravity／通用 Agent | `antigravity` | `.agent` | 可 |
| GitHub Copilot | `copilot` | `.github/skills` | 不可 |
| Kiro | `kiro` | `.kiro` | 不可 |
| OpenAI Codex CLI | `codex` | `.codex` | 不可 |
| Qoder | `qoder` | `.qoder` | 不可 |
| Roo Code | `roocode` | `.roo` | 不可 |
| Gemini CLI | `gemini` | `.gemini` | 不可 |
| Trae | `trae` | `.trae` | 不可 |
| OpenCode | `opencode` | `.opencode` | 不可 |
| Continue | `continue` | `.continue` | 不可 |
| CodeBuddy | `codebuddy` | `.codebuddy` | 不可 |
| 全部 | `all` | | |

## 快速開始

### Step 2：對 AI 助手說

| 你說 | 會發生什麼 |
|---|---|
| 「把這個外掛的 .pot 翻成 zh_TW。」 | 抽出未翻譯項目、逐詞查詞彙表、翻譯，再 validate 到錯誤 0 |
| 「sidebar 在 WordPress 台灣怎麼翻？」 | 查詞並引用那一列：資訊欄（WP 詞彙表） |
| 「設置是中國用語嗎？要改成什麼？」 | 查用語對照：設定，並附那一列的依據 |

### Step 3：自己跑工具

```bash
cd translate-cli/assets/taiwan-translate
python scripts/lookup.py "Please select a theme from the dashboard"
```

```
命中詞彙（僅供翻譯參考，整句翻譯請由模型完成）：
dashboard              控制台            noun     WP
select                 選取             verb     WP
theme                  佈景主題           noun     WP
```

| 指令 | 用途 |
|---|---|
| `python scripts/search.py "<詞>"` | 查詞（`--domain zh` 用中文找英文，`--source fanhuaji` 查中國用語） |
| `python scripts/lookup.py "<句子>"` | 列出一句話裡所有命中的詞 |
| `python scripts/po.py extract <檔>` | 列出未翻譯項目 |
| `python scripts/po.py validate <檔>` | 檢查譯好的 `.po`；exit 0 表示沒有錯誤 |
| `tw-translate list`／`info`／`update` | 安裝工具指令 |

所有參數、輸出範例和常見問題：[docs/guide.md](docs/guide.md)。

## 觸發詞

English: translate to Traditional Chinese, Taiwan Chinese, zh_TW, translate a WordPress plugin or theme, .po / .pot translation, Loco Translate warning, glossary lookup, China terms to Taiwan terms.

中文：翻譯成繁體中文、台灣用語、正體中文、WP 外掛翻譯、.po 翻譯、Loco 警告、這個詞台灣怎麼說、中國用語改台灣用語。

## 會執行與連線的內容

不會自己執行任何東西：這個 plugin 沒有 hook、沒有 MCP 伺服器、沒有背景程式。只有 Claude 照 `SKILL.md` 操作、你同意指令後，工具才會跑。翻譯不需要連網、不需要 API 金鑰，也不會把任何資料傳給作者或第三方。

| 工具 | 讀 | 寫 | 連線 |
|---|---|---|---|
| `scripts/search.py`、`scripts/lookup.py` | `data/glossary.csv`、`data/taiwan-terms.csv` | 不寫 | 不連線 |
| `scripts/po.py extract`、`po.py validate` | 你指定的 `.po`／`.pot` | 不寫（只報告） | 不連線 |
| Claude 照你的要求翻譯檔案時 | 那個 `.po` | 它的 `msgstr` | 不連線 |
| Claude 查不到詞時 | | `data/pending.csv` 加一列 | 不連線 |
| `scripts/test_tools.py`、`scripts/check_numbers.py` | repo 內的檔案 | 系統暫存資料夾裡的小檔（不會刪）；`check_numbers.py --fix` 會改 `SKILL.md` 和 README 裡錯的數字 | 不連線 |
| `tw-translate init`／`update` | 套件內的 skill | 專案裡該 AI 工具的資料夾；加 `--global` 時寫到家目錄 | 不連線 |
| `tw-translate versions` | | 不寫 | `registry.npmjs.org`（查最新版號） |
| `tools/fetch_glossary.py`（維護者用） | `data/glossary.csv`（保留只在快照的列） | `data/glossary.csv` | `translate.wordpress.org`（詞彙表 CSV 匯出） |
| `tools/measure_fanhuaji.py`（維護者用） | `data/taiwan-terms.csv` | `data/taiwan-terms.csv` | `api.zhconvert.org`（只送用語清單，不送你的檔案） |

雙來源策略：兩份來源在發版時就固定寫進 CSV，翻譯時不會去抓。

| 來源 | 順序 | 數量 |
|---|---|---|
| WordPress 台灣詞彙表 | 優先 | 2,627 列詞彙 |
| 繁化姬中國 → 台灣用語 | 詞彙表查不到時 | 135 組用語對照 |
| 兩邊都沒有 | 保留原文，記進 `pending.csv` | |

## 驗證方式

| 檢查 | 結果 | 證據 |
|---|---|---|
| 詞彙表 | 現行列於 2026-11-15 從 GlotPress 匯出；舊列標快照日期 2024-03-22 | `data/glossary.csv` 的 `doc_url`、`retrieved_on`、`trust` 欄 |
| 中國 → 台灣用語 | 每組於 2026-11-15 送進繁化姬台灣化轉換器，轉換器實際輸出存在同一列 | `data/taiwan-terms.csv` 的 `fanhuaji_out`、`measured_on`、`trust` 欄 |
| 自我測試 | 24 項離線測試：CSV 出處、查詞、lookup、`.po` 抽取與把關、`SKILL.md` 的數字 | `python scripts/test_tools.py` |
| evals | 14 題計分題（全部 19 題）；有 skill 14/14，沒有 skill 0/14 | [evals/RESULTS.md](translate-cli/assets/taiwan-translate/evals/RESULTS.md) |
| 文件數字 | `SKILL.md`、兩份 README 和 guide 的每個數字都對得上資料 | `python scripts/check_numbers.py` |

## 限制

| 限制 | 說明 |
|---|---|
| 範圍 | WordPress 與軟體介面用語；不是一般辭典 |
| 風格規則 | 標點、空格規則是站內風格；沒找到可引用的官方 zh-TW 風格指南條文 |
| 舊列 | 只在 2024 快照的列可能是社群刻意刪掉的；同一英文詞以現行列為準 |
| Windows 編碼 | 終端機要用 UTF-8（`chcp 65001`），否則中文可能變亂碼 |
| 待補問題 | [data/pending.csv](translate-cli/assets/taiwan-translate/data/pending.csv) |

## 目錄結構

```
.claude-plugin/              plugin 與 marketplace 設定、圖示
translate-cli/               npm 套件：tw-translate 安裝工具（TypeScript）
  assets/taiwan-translate/   skill 本體：SKILL.md、data/、scripts/、references/、evals/
  assets/templates/          各平台安裝樣板
docs/guide.md                完整說明
README.md、README.zh-TW.md   英文主檔與本檔
```

## 授權與作者

MIT 授權。作者 Moksa（[moksaweb.com](https://moksaweb.com)）。詞彙資料：[WordPress 台灣 GlotPress 詞彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/)。問題回報：[GitHub](https://github.com/Moksa1123/taiwan-translate-skill/issues)。
