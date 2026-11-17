<h1 align="center">Taiwan Translate Skill</h1>

<h3 align="center">台灣正體中文翻譯技能包</h3>

<p align="center">
  <strong>WordPress zh-TW glossary · China-to-Taiwan term check · .po / .pot validator</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/python-3-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/format-Agent%20Skill-blue?style=flat-square" alt="Agent Skill">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/glossary-2627-success?style=flat-square" alt="Glossary rows">
  <img src="https://img.shields.io/badge/Taiwan%20terms-135-success?style=flat-square" alt="Taiwan term pairs">
  <img src="https://img.shields.io/badge/AI%20platforms-14-orange?style=flat-square" alt="AI platforms">
  <a href="https://www.npmjs.com/package/taiwan-translate-skill"><img src="https://img.shields.io/npm/v/taiwan-translate-skill?style=flat-square&color=cb3837&logo=npm&logoColor=white&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/taiwan-translate-skill"><img src="https://img.shields.io/npm/dm/taiwan-translate-skill?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm downloads"></a>
  <a href="https://github.com/Moksa1123/taiwan-translate-skill"><img src="https://img.shields.io/github/stars/Moksa1123/taiwan-translate-skill?style=flat-square&logo=github&logoColor=white&color=181717" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="https://github.com/Moksa1123/taiwan-translate-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
  <a href="https://paypal.me/cccsubcom"><img src="https://img.shields.io/badge/PayPal-Donate-00457C?style=flat-square&logo=paypal&logoColor=white" alt="PayPal"></a>
</p>

<p align="center"><strong>English</strong> · <a href="https://github.com/Moksa1123/taiwan-translate-skill/blob/main/README.zh-TW.md">正體中文</a></p>

> This is an unofficial community project. It is not made by, endorsed by, or affiliated with the WordPress Foundation, the WordPress Taiwan translation team or Fanhuaji. It reads their public glossary and converter output; neither is bundled as software.

## What it does

Gives an AI assistant the WordPress Taiwan community's official zh-TW glossary, so plugin, theme and software UI strings come out in Taiwan usage instead of China usage or machine guesses.

| Area | What you get |
|---|---|
| Glossary | 2,627 glossary rows from the WordPress Taiwan GlotPress glossary: 2,566 current, 61 kept from the 2024-03-22 GitHub snapshot; every row has its source URL, retrieval date and trust level |
| China → Taiwan terms | 135 term pairs (設置 → 設定, 插件 → 外掛): 76 measured against the Fanhuaji Taiwan converter, 30 from official docs, 29 house style |
| Lookup | `search.py` finds a term in English or Chinese; `lookup.py` lists every glossary hit in a sentence. Neither rewrites the sentence: the model translates, the glossary keeps terms consistent |
| .po / .pot | `po.py extract` pulls untranslated entries (plural, msgctxt, multi-line); `po.py validate` checks placeholders, empty strings, punctuation, China terms, and exits 1 on any error |
| Installer | `tw-translate init` installs the skill into 14 AI tools (Claude Code, Cursor, Codex, Gemini CLI, Copilot and more) |

The model looks a term up before answering. When the glossary has no entry it says so and logs the question in `data/pending.csv` instead of inventing a "standard" translation.

## When to use

| Use it for | Use something else for |
|---|---|
| English → Taiwan Traditional Chinese for WordPress plugins, themes and software UI | Writing Chinese WordPress articles for SEO → `rankmath-seo-wp` |
| Translating or checking `.po` / `.pot` files, fixing Loco Translate warnings | Converting a whole Simplified Chinese text with no software terms → the Fanhuaji site |
| "How does the WordPress Taiwan community translate X?" | Legal or medical documents: the glossary does not cover them |
| Replacing China usage (設置, 默認, 插件) with Taiwan usage | |

## Install

| Need | For |
|---|---|
| Python 3 (standard library only) | The search, lookup and `.po` tools |
| Node.js 18+ | The `tw-translate` installer (npx) only |
| Windows, macOS or Linux | Everything |

### Step 1: Pick an install method

Claude plugin (Claude Code; the Claude directory once listed):

```
/plugin marketplace add Moksa1123/taiwan-translate-skill
/plugin install taiwan-translate@taiwan-translate-skill
```

npx (Claude Code and the other AI tools below):

```bash
npx taiwan-translate-skill@1.3.0 init                 # pick a platform interactively
npx taiwan-translate-skill@1.3.0 init --ai claude --global
```

Manual copy:

```bash
git clone https://github.com/Moksa1123/taiwan-translate-skill.git
cp -r taiwan-translate-skill/translate-cli/assets/taiwan-translate ~/.claude/skills/tw-translate
```

| Platform | `--ai` key | Folder | Global install |
|---|---|---|---|
| Claude Code | `claude` | `.claude` | yes |
| Cursor | `cursor` | `.cursor` | yes |
| Devin Desktop (formerly Windsurf) | `windsurf` | `.devin` (old `.windsurf` still detected) | no |
| Antigravity / generic agent | `antigravity` | `.agent` | yes |
| GitHub Copilot | `copilot` | `.github/skills` | no |
| Kiro | `kiro` | `.kiro` | no |
| OpenAI Codex CLI | `codex` | `.codex` | no |
| Qoder | `qoder` | `.qoder` | no |
| Roo Code | `roocode` | `.roo` | no |
| Gemini CLI | `gemini` | `.gemini` | no |
| Trae | `trae` | `.trae` | no |
| OpenCode | `opencode` | `.opencode` | no |
| Continue | `continue` | `.continue` | no |
| CodeBuddy | `codebuddy` | `.codebuddy` | no |
| All of the above | `all` | | |

## Quick start

### Step 2: Ask the assistant

| You say | What happens |
|---|---|
| "Translate this plugin's .pot into zh_TW." | Extracts untranslated entries, looks up each term, translates, then validates until 0 errors |
| "How does WordPress Taiwan translate 'sidebar'?" | Looks it up and quotes the row: 資訊欄 (WP glossary) |
| "Is 設置 China usage? What should it be?" | Looks it up in the term pairs: 設定, with the evidence for that row |

### Step 3: Run the tools yourself

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

| Command | Does |
|---|---|
| `python scripts/search.py "<term>"` | Look a term up (`--domain zh` for Chinese → English, `--source fanhuaji` for China terms) |
| `python scripts/lookup.py "<sentence>"` | List every glossary hit in a sentence |
| `python scripts/po.py extract <file>` | List untranslated entries |
| `python scripts/po.py validate <file>` | Check a translated `.po`; exit 0 means no errors |
| `tw-translate list` / `info` / `update` | Installer commands |

Every option, sample output and the FAQ: [docs/guide.md](https://github.com/Moksa1123/taiwan-translate-skill/blob/main/docs/guide.md).

## Trigger phrases

English: translate to Traditional Chinese, Taiwan Chinese, zh_TW, translate a WordPress plugin or theme, .po / .pot translation, Loco Translate warning, glossary lookup, China terms to Taiwan terms.

中文：翻譯成繁體中文、台灣用語、正體中文、WP 外掛翻譯、.po 翻譯、Loco 警告、這個詞台灣怎麼說、中國用語改台灣用語。

## What it runs and connects to

Nothing runs on its own: the plugin has no hooks, no MCP servers and no background processes. A tool runs only when Claude follows `SKILL.md` and you approve the command. Translating needs no network access and no API key, and no data is sent to the author or anyone else.

| Tool | Reads | Writes | Connects to |
|---|---|---|---|
| `scripts/search.py`, `scripts/lookup.py` | `data/glossary.csv`, `data/taiwan-terms.csv` | Nothing | Nothing |
| `scripts/po.py extract`, `po.py validate` | The `.po` / `.pot` file you name | Nothing (report only) | Nothing |
| Claude, when you ask it to translate a file | That `.po` file | Its `msgstr` lines | Nothing |
| Claude, when a term is not in the glossary | | One row in `data/pending.csv` | Nothing |
| `scripts/test_tools.py`, `scripts/check_numbers.py` | Files in this repo | Small files in your system temp folder (left there); `check_numbers.py --fix` rewrites wrong numbers in `SKILL.md` and the READMEs | Nothing |
| `tw-translate init` / `update` | The bundled skill | The AI tool's folder in your project, or your home folder with `--global` | Nothing |
| `tw-translate versions` | | Nothing | `registry.npmjs.org` (latest version number) |
| `tools/fetch_glossary.py` (maintainers) | `data/glossary.csv` (keeps snapshot-only rows) | `data/glossary.csv` | `translate.wordpress.org` (glossary CSV export) |
| `tools/measure_fanhuaji.py` (maintainers) | `data/taiwan-terms.csv` | `data/taiwan-terms.csv` | `api.zhconvert.org` (sends only the term list, never your files) |

Both sources are fixed into the CSV files at release time; nothing is fetched while you translate.

| Source | Order | Size |
|---|---|---|
| WordPress Taiwan glossary | first | 2,627 glossary rows |
| Fanhuaji China → Taiwan pairs | when the glossary has no entry | 135 term pairs |
| Neither has it | keep the source text, log it in `pending.csv` | |

## How it's verified

| Check | Result | Evidence |
|---|---|---|
| Glossary | Current rows exported from GlotPress on 2026-11-15; older rows marked with their 2024-03-22 snapshot date | `doc_url`, `retrieved_on`, `trust` columns in `data/glossary.csv` |
| China → Taiwan pairs | Each pair sent to the Fanhuaji Taiwan converter on 2026-11-15; the converter's output is stored next to it | `fanhuaji_out`, `measured_on`, `trust` columns in `data/taiwan-terms.csv` |
| Self-test | 24 offline tests: CSV provenance, search, lookup, `.po` extract and validate, numbers in `SKILL.md` | `python scripts/test_tools.py` |
| Evals | 14 scored questions (19 questions in all); with the skill 14/14, without it 0/14 | [evals/RESULTS.md](https://github.com/Moksa1123/taiwan-translate-skill/blob/main/translate-cli/assets/taiwan-translate/evals/RESULTS.md) |
| Numbers in docs | Every number in `SKILL.md`, these READMEs and the guide matches the data | `python scripts/check_numbers.py` |

## Limits

| Limit | Details |
|---|---|
| Scope | WordPress and software UI terms; not a general dictionary |
| Style rules | Punctuation and spacing rules are house style; no official zh-TW style guide text was found to cite |
| Old rows | Rows only in the 2024 snapshot may have been removed by the community on purpose; current rows win |
| Encoding on Windows | Use a UTF-8 terminal (`chcp 65001`) or Chinese output may look garbled |
| Open questions | [data/pending.csv](https://github.com/Moksa1123/taiwan-translate-skill/blob/main/translate-cli/assets/taiwan-translate/data/pending.csv) |

## Repo layout

```
.claude-plugin/              plugin and marketplace manifests, icon
translate-cli/               npm package: the tw-translate installer (TypeScript)
  assets/taiwan-translate/   the skill: SKILL.md, data/, scripts/, references/, evals/
  assets/templates/          per-platform install templates
docs/guide.md                the long guide
README.md, README.zh-TW.md   this file and its Chinese version
```

## License & author

MIT License. Made by Moksa ([moksaweb.com](https://moksaweb.com)). Glossary data: [WordPress Taiwan GlotPress glossary](https://translate.wordpress.org/locale/zh-tw/default/glossary/). Issues: [GitHub](https://github.com/Moksa1123/taiwan-translate-skill/issues).
