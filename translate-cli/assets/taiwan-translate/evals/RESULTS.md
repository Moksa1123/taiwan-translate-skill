# evals 結果

最新的在最上面。題目與評分標準見 `cases.json`，評分程式 `grade.py`。

## 2026-11-15 第 1 輪

- skill 版本：repo commit 7bf2c9f 之後（SKILL.md 五段、glossary 2026-11-15 GlotPress 重抓）。
- 評分規則在本輪作答後修正一處：`rich-snippet` 原本有 `must_not: 複合式摘要`，但有 skill 的正確答案在說明舊稱時提到「複合式摘要」而被誤判；已拿掉 must_not（只看 must「複合式搜尋結果」，沒 skill 的答案「複合式摘要」仍判錯）。下表用修正後的規則評分。
- 5 題沒 skill 也答對（`block-pattern`、`template-part`、`tagline`、`archive`、`dark-pattern-absent`），已在 `cases.json` 標 `retired`，下次換題。其中 `dark-pattern-absent` 的「沒有收錄」正規式會比對到沒 skill 答案裡的「有沒有收錄」，算評分漏洞；正規式已改成不接受「有沒有收錄」，此題仍退役。
- 有 skill 的作答者對 `dark-pattern-absent` 照鐵則回「查不到，待補」，已記進 `data/pending.csv`。


| 項目 | 有 skill | 沒有 skill |
|---|---|---|
| 計分題答對率（14 題） | **14/14（100.0%）** | 0/14（0.0%） |
| 全部題目（19 題） | 19/19 | 5/19 |
| 模型 | claude-opus-5-5 | claude-opus-5-5 |
| 作答方式 | subagent 讀 SKILL.md、用 search.py 查 | subagent 不用任何工具，憑記憶作答 |
| 答案檔 | `evals/runs/2026-11-15-with-skill.json` | `evals/runs/2026-11-15-without-skill.json` |

| 題目 | 可信度 | 有 skill | 沒有 skill | 備註 |
|---|---|---|---|---|
| `block-pattern` | 官方文件 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `sidebar` | 官方文件 | ✅ | ❌ |  |
| `breadcrumb` | 官方文件 | ✅ | ❌ |  |
| `nonce` | 官方文件 | ✅ | ❌ |  |
| `heartbeat` | 官方文件 | ✅ | ❌ |  |
| `drop-in` | 官方文件 | ✅ | ❌ |  |
| `modal` | 官方文件 | ✅ | ❌ |  |
| `template-part` | 官方文件 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `rich-snippet` | 官方文件 | ✅ | ❌ |  |
| `headless-cms` | 官方文件 | ✅ | ❌ |  |
| `vibe-coding` | 官方文件 | ✅ | ❌ |  |
| `deprecated` | 官方文件 | ✅ | ❌ |  |
| `fallback` | 官方文件 | ✅ | ❌ |  |
| `tagline` | 官方文件 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `archive` | 官方文件 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |
| `media-caption` | 官方文件 | ✅ | ❌ |  |
| `abkhazian` | 官方文件 | ✅ | ❌ |  |
| `taxonomy-term` | 官方文件 | ✅ | ❌ |  |
| `dark-pattern-absent` | 官方文件 | ✅ | ✅ | 沒 skill 也對：不計分，要換題 |

