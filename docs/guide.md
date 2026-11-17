# taiwan-translate-skill guide

The long material that used to live in the README: every tool's options and
output, the installer, a verified term table and the FAQ. The README keeps the
short version; the rules the assistant follows are in
[`SKILL.md`](../translate-cli/assets/taiwan-translate/SKILL.md).

All Python commands run from `translate-cli/assets/taiwan-translate/` (or the
installed skill folder) and use only the standard library.

## Look a term up: `scripts/search.py`

```bash
python scripts/search.py plugin                      # English → zh-TW
python scripts/search.py "post type"
python scripts/search.py 外掛 --domain zh             # Chinese → English
python scripts/search.py 設置 --source fanhuaji       # China term → Taiwan term
python scripts/search.py plugin --limit 5 --format json
```

| Option | Values | Default |
|---|---|---|
| `--domain` | `all`, `en` (English column), `zh` (Chinese column) | `all` |
| `--source` | `all`, `wp` (WordPress glossary), `fanhuaji` (China → Taiwan pairs) | `all` |
| `--limit` | number of results | small default |
| `--format` | `table`, `json` | `table` |

```
英文/簡體                     台灣正體               分類       來源
================================================================================
設置                        設定                 ui       FHJ
  └─ settings
```

Simplified characters must be turned into traditional glyphs first
(设置 → 設置); the term pairs are stored in traditional glyphs.

## List the terms in a sentence: `scripts/lookup.py`

```bash
python scripts/lookup.py "Please select a theme from the dashboard"
python scripts/lookup.py --file input.txt
python scripts/lookup.py "Click Settings" --format json
```

```
原文：Please select a theme from the dashboard

命中詞彙（僅供翻譯參考，整句翻譯請由模型完成）：
------------------------------------------------------------------------
dashboard              控制台            noun     WP
select                 選取             verb     WP
theme                  佈景主題           noun     WP
------------------------------------------------------------------------
詞彙來源統計: WP官方 3, 繁化姬 0
```

It matches on word boundaries and never rewrites the sentence. The old
`translate.py` did substring replacement and produced broken text; it now
only points to these tools.

## Translate a .po / .pot: `scripts/po.py`

The workflow: extract untranslated entries → the model translates each one
after looking its terms up → validate → fix until there are no errors.

```bash
python scripts/po.py extract  path/to/plugin.pot
python scripts/po.py extract  path/to/plugin.pot --format json
python scripts/po.py validate path/to/plugin-zh_TW.po
python scripts/po.py validate path/to/plugin-zh_TW.po --format json
```

`extract` keeps multi-line strings, plurals, `msgctxt` and line numbers.
`validate` only reports and never edits the file:

| Level | Checks | Effect |
|---|---|---|
| Error | Empty translation, placeholders (`%s`, `%1$s`) that differ from the source | exit 1 |
| Warning | HTML tags, leading / trailing spaces, end punctuation, initial capital, China terms, inconsistent terms | Read each one; fix it or say why not |

```
條目：1
問題：錯誤 0，警告 2，提示 0
[L6] 警告(end-punct): 原文以「.」結尾，譯文缺少對應標點（建議全形）
[L6] 警告(china-term): 疑似中國用語：保存→儲存
```

Because errors always exit 1, `po.py validate` works as a CI gate.

## Translation rules

| Rule | Example | Basis |
|---|---|---|
| Use the WordPress glossary translation | sidebar → 資訊欄, block pattern → 區塊版面配置 | Official glossary |
| Language names end in 文, not 語 | English → 英文 | Official glossary (language-name rows) |
| Keep brand and product names in English | WordPress, Google | House style |
| Full-width punctuation | 「設定已儲存。」 | House style |
| A half-width space between Chinese and Latin letters or digits | 請使用 WordPress 外掛 | House style |
| No plural markers in Chinese | files → 檔案 | House style |

Full rules: [`references/STYLE_GUIDE.md`](../translate-cli/assets/taiwan-translate/references/STYLE_GUIDE.md).

## Common terms (each looked up with `search.py`)

| English | Taiwan (WordPress glossary) | China term | Taiwan (term pairs) |
|---|---|---|---|
| plugin | 外掛 | 插件 | 外掛 |
| setting | 設定 | 設置 | 設定 |
| default | 預設 | 默認 | 預設 |
| save | 儲存 | 保存 | 儲存 |
| code | 程式碼 | 代碼 | 程式碼 |
| sidebar | 資訊欄 | | |
| featured image | 精選圖片 | | |
| custom field | 自訂欄位 | | |
| post format | 文章格式 | | |
| dashboard | 控制台 | | |

Anything not in this table: run `search.py`. More pairs with their evidence:
[`references/TAIWAN_VS_CHINA.md`](../translate-cli/assets/taiwan-translate/references/TAIWAN_VS_CHINA.md).

## The installer: `tw-translate`

```bash
npx taiwan-translate-skill@1.3.1 init                     # interactive
npx taiwan-translate-skill@1.3.1 init --ai cursor         # one platform
npx taiwan-translate-skill@1.3.1 init --ai all            # every platform
npx taiwan-translate-skill@1.3.1 init --ai claude --global
npm install -g taiwan-translate-skill                     # then: tw-translate <command>
```

| Command | Does |
|---|---|
| `tw-translate init` | Install the skill (`--ai <key>`, `--global`, `--force`) |
| `tw-translate list` | List the supported platforms |
| `tw-translate info` | Version and data sources |
| `tw-translate versions` | Ask the npm registry for the latest version |
| `tw-translate update` | Re-install into every platform folder found in the current project (`--force`) |

`init` copies the skill folder (or, for rule-based tools, a generated rule
file) into the tool's folder in the current project; `--global` writes to
the tool's folder under your home directory where the tool supports it.

## Maintenance

```bash
python scripts/test_tools.py              # offline self-test
python scripts/check_numbers.py           # numbers in SKILL.md, READMEs, this guide
python scripts/check_numbers.py --stats   # current row counts
python tools/fetch_glossary.py            # re-export the GlotPress glossary (network)
python tools/measure_fanhuaji.py          # re-measure the term pairs with Fanhuaji (network)
python evals/grade.py --questions         # eval questions
```

After a re-fetch: `check_numbers.py --fix`, then `test_tools.py`, then re-run
the evals and record them in `evals/RESULTS.md`.

## FAQ

| Question | Answer |
|---|---|
| The assistant doesn't pick up the skill after install | Restart the AI tool; skills load at start-up |
| Chinese output is garbled on Windows | Use a UTF-8 terminal: `chcp 65001`, or in PowerShell `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` |
| How do I get a newer glossary? | `npx taiwan-translate-skill@latest init --force`, or `tw-translate update` |
| Can I add my own terms? | Yes: add rows to `data/glossary.csv` with `en,zh-tw,pos,description`, and mark them with your own `trust` value so they are not mistaken for official rows |
| Which files are supported? | GNU gettext `.po` and `.pot` |
| A term isn't in the glossary | The assistant says so and logs it in `data/pending.csv`; it does not guess a "standard" translation |
