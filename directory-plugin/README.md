<h1 align="center">Taiwan Translate Skill</h1>

<h3 align="center">台灣正體中文翻譯技能包（官方目錄精簡版）</h3>

<p align="center">
  <strong>WordPress zh-TW glossary · China-to-Taiwan term check · .po / .pot translation rules</strong>
</p>

> This is an unofficial community project. It is not made by, endorsed by, or affiliated with the WordPress Foundation, the WordPress Taiwan translation team or Fanhuaji. It contains their public glossary and converter output as data.

This is the **directory edition** of [taiwan-translate-skill](https://github.com/Moksa1123/taiwan-translate-skill): the same glossary, term pairs, translation rules and examples, packaged as JSON and Markdown so it fits the Claude plugin directory. It contains no scripts. For the full edition, with the search tools and the `.po` validator, install the npm package (see Install).

## What it does

| Area | What you get |
|---|---|
| Glossary | 2,627 rows from the WordPress Taiwan GlotPress glossary (2,566 current, 61 from the 2024-03-22 snapshot), each with its source URL, retrieval date and trust level |
| China → Taiwan terms | 135 term pairs (設置 → 設定, 插件 → 外掛): 76 measured against the Fanhuaji Taiwan converter, 30 from official docs, 29 house style |
| Rules | Punctuation, spacing, language names and placeholder rules, each marked official or house style |
| Checklist | A step-by-step check for translated `.po` files that mirrors the full edition's validator |

Claude looks every term up in the JSON files before answering. When the glossary has no entry it says so instead of inventing a "standard" translation.

## When to use

| Use it for | Use something else for |
|---|---|
| English → Taiwan Traditional Chinese for WordPress plugins, themes and software UI | Writing Chinese WordPress articles for SEO |
| Translating `.po` / `.pot` files, fixing Loco Translate warnings | Converting a whole Simplified Chinese text with no software terms |
| Replacing China usage (設置, 默認, 插件) with Taiwan usage | Legal or medical documents |

## Install

```
/plugin install taiwan-translate
```

Full edition with the search tools and the `.po` validator (Claude Code, Cursor, Codex, Gemini CLI, Copilot and more):

```bash
npx taiwan-translate-skill@1.3.1 init
```

## Quick start

| You say | What happens |
|---|---|
| "Translate this plugin's .pot into zh_TW." | Looks up each term, translates, then walks the checklist |
| "How does WordPress Taiwan translate 'sidebar'?" | Quotes the glossary row: 資訊欄 |
| "Is 設置 China usage? What should it be?" | Quotes the term pair: 設定, with its evidence |

## Trigger phrases

English: translate to Traditional Chinese, Taiwan Chinese, zh_TW, translate a WordPress plugin or theme, .po / .pot translation, Loco Translate warning, glossary lookup, China terms to Taiwan terms.

中文：翻譯成繁體中文、台灣用語、正體中文、WP 外掛翻譯、.po 翻譯、Loco 警告、這個詞台灣怎麼說、中國用語改台灣用語。

## What it runs and connects to

| Item | This edition |
|---|---|
| Scripts, hooks, MCP servers | None |
| Files it reads | The JSON and Markdown files in this folder, and the files you ask it to translate |
| Files it writes | None; Claude edits a `.po` file only when you ask |
| Network | None |
| Credentials | None |

No data is sent to the author or anyone else.

## How it's verified

| Check | Result |
|---|---|
| Glossary | Current rows exported from GlotPress on 2026-11-15; every row keeps `doc_url`, `retrieved_on` and `trust` |
| Term pairs | Each pair sent to the Fanhuaji Taiwan converter on 2026-11-15; the converter's output is stored in the row |
| Evals (full edition) | 14 scored questions; with the skill 14/14, without it 0/14 |
| This folder | Generated from the main repository's sources by `scripts/build_directory.py`; `--check` fails if they differ |

## Limits

| Limit | Details |
|---|---|
| No validator | `.po` checks are done by following the checklist; the full edition's `po.py validate` does them automatically |
| No search tool | Terms are found by searching the JSON files |
| Scope | WordPress and software UI terms; not a general dictionary |
| Open questions | `skills/tw-translate/data/pending.json` |

## Repo layout

```
.claude-plugin/              plugin manifest and icon
skills/tw-translate/         SKILL.md, EXAMPLES.md, data/*.json, references/*.md
README.md, LICENSE
```

## License & author

MIT License. Made by Moksa. Glossary data: [WordPress Taiwan GlotPress glossary](https://translate.wordpress.org/locale/zh-tw/default/glossary/). Issues: [GitHub](https://github.com/Moksa1123/taiwan-translate-skill/issues).
