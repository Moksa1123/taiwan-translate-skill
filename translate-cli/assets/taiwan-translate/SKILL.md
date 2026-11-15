---
name: tw-translate
description: 台灣正體中文翻譯工具。使用 WordPress 台灣社群官方詞彙表，翻譯軟體介面、外掛、佈景主題等文字。支援 .po/.pot 檔案翻譯、詞彙查詢、文字翻譯。觸發：翻譯成繁體中文、台灣用語、正體中文、WP 外掛翻譯、.po 翻譯、Loco 警告、這個詞台灣怎麼說、中國用語改台灣用語。Use for Traditional Chinese (Taiwan, zh_TW) translation of WordPress plugins/themes and software UI, .po/.pot files, glossary lookup.
user-invocable: true
---

# 台灣正體中文翻譯技能

模型負責翻整句，腳本負責「查詞彙」與「把關」。詞彙表是確保用詞一致的參考，**不做子字串自動代換**（舊版 `translate.py` 這樣做會產生亂碼，已停用）。

## 資料出處

| 資料 | 來源 | 筆數 | 日期 | 可信度 |
|---|---|---|---|---|
| `data/glossary.csv` | [WordPress 台灣社群 GlotPress 詞彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/) 的 CSV 匯出 | 2627 列（現行 2566 列＋舊版快照 61 列） | 現行列擷取於 2026-11-15；舊版列來自 GitHub 快照 2024-03-22 | 官方文件 |
| `data/taiwan-terms.csv` | 簡體／中國用語 → 台灣用語對照，每列送進[繁化姬](https://docs.zhconvert.org/)台灣化轉換器實測 | 135 列（實測 76、官方文件 30、站內風格 29） | 2026-11-15 實測 | 每列 `trust` 欄 |
| `references/TAIWAN_VS_CHINA.md` | 常見中國用語對照，每列標依據 | — | 同上 | 每列「依據」欄 |
| `references/STYLE_GUIDE.md` | 標點、空格、語氣規則 | — | — | 站內風格（稱文不稱語除外，見下） |

- 每列都有出處欄：glossary 是 `doc_url`＋`retrieved_on`＋`trust`；taiwan-terms 是 `fanhuaji_out`（繁化姬實際輸出）＋`measured_on`＋`doc_url`＋`trust`。
- `retrieved_on` 是 2024-03-22 的列＝現行詞彙表已經沒有，只能當參考；同一英文詞以現行列為準。
- 「站內風格」＝本 skill 的慣例，不是官方規則，不可對使用者說成「WP 官方規定」。
- 筆數由 `python scripts/check_numbers.py --stats` 產生，`scripts/test_tools.py` 核對本檔每個數字。

## 用法

**何時用**：英文或簡體中文 → 台灣正體中文，尤其是 WordPress 外掛／佈景主題、軟體介面字串、.po/.pot 檔；查「某個詞 WP 台灣社群怎麼譯」；把中國用語改成台灣用語。

**何時不用**：

| 需求 | 交給 |
|---|---|
| 寫 WordPress 中文文章、SEO 分數 | `rankmath-seo-wp` |
| 整篇簡轉繁、不涉及軟體用語 | 繁化姬網站（zhconvert.org）直接轉 |
| 法律、醫療等專業文件 | 本 skill 的詞彙表不涵蓋，照實告訴使用者 |

**唯一入口**：`python scripts/search.py "<詞>"`。其他工具從它延伸：

| 工具 | 誰用 | 做什麼 |
|---|---|---|
| `scripts/search.py` | 使用者路徑 | 查詞（英文或正體字中文；簡體字要先轉成正體字形再查，例 设置→設置），列出譯法與來源（WP／FHJ） |
| `scripts/lookup.py` | 使用者路徑 | 列出一句英文裡命中的所有詞彙（單字邊界比對，不代換整句） |
| `scripts/po.py extract` | 使用者路徑 | 抽出 .po/.pot 未翻譯項目（保留多行、複數、msgctxt、行號） |
| `scripts/po.py validate` | 使用者路徑 | 翻譯把關，有錯回非 0 |
| `scripts/check_numbers.py`、`scripts/test_tools.py` | 維護者 | 數字核對、自我測試（離線） |
| `tools/fetch_glossary.py`、`tools/measure_fanhuaji.py` | 維護者 | 重建兩份 CSV（要連網） |

只用 Python 標準函式庫。

## 路由

> **鐵則：先查再答，不憑記憶。** 每個專有名詞、介面用語都要先用 `search.py`／`lookup.py` 查。
> 查不到就照實說「詞彙表查不到」，在答案裡標「待補」，並把問題記進 `data/pending.csv`（欄位：日期、問題、為何查不到、誰問的、狀態）。**不要拿相似詞或「台灣習慣」推一個譯法當成標準答案。**
> 使用者要你先給一個譯法時，可以給，但要明講「這是推論，詞彙表沒有」。

| 使用者會怎麼說 | 查哪裡 | 指令 |
|---|---|---|
| 「X 台灣怎麼翻」「X 的標準譯法」 | glossary.csv | `python scripts/search.py "X"` |
| 「外掛的英文是什麼」（中文找英文） | glossary.csv 中文欄 | `python scripts/search.py "外掛" --domain zh` |
| 「這句話翻成繁中」 | 句中每個詞 | `python scripts/lookup.py "<英文句子>"`，再由模型翻 |
| 「翻這個 .po／.pot」「外掛中文化」 | 檔案 | `python scripts/po.py extract <檔>` → 翻 → `po.py validate <檔>` |
| 「這是中國用語嗎」「設置／默認要改嗎」 | taiwan-terms.csv、TAIWAN_VS_CHINA.md | `python scripts/search.py "設置" --source fanhuaji` |
| 「Loco 一直警告」「佔位符不見」 | 譯好的 .po | `python scripts/po.py validate <檔>` |
| 「標點／空格要怎麼寫」 | `references/STYLE_GUIDE.md` | 直接讀 |

一個英文詞在詞彙表有多個譯法時（例如 spam、sticky、archive），看 `pos` 與 `description` 欄的適用情境選，不要只取第一筆。

## 使用

| 任務 | 步驟 | 完成的證據 |
|---|---|---|
| 查一個詞 | `search.py "<詞>"`；多筆時依 pos／description 選；查不到記 pending.csv | 回答附上命中的那一列（譯法＋來源 WP／FHJ） |
| 翻一句或一段介面文字 | 1. `lookup.py` 列出命中詞 2. 模型照命中譯法與下面的翻譯規則翻 3. 用下節的方法 validate | 每個專有名詞都對得到 lookup 輸出；validate exit 0 |
| 翻 .po/.pot | 1. `po.py extract <檔>` 2. 每條 msgid 先 `lookup.py` 再翻，回寫 msgstr，保留 `%s`、`%1$s`、HTML 標籤與首尾空白 3. `po.py validate <檔>` 4. 修到 0 錯誤，警告逐條判斷 | validate exit 0，報告「錯誤 0」 |
| 中國用語改台灣用語 | `search.py "<詞>" --source fanhuaji`；看 `trust` 欄；對照 `references/TAIWAN_VS_CHINA.md` | 每個替換都對得到一列，並說出依據（實測／官方文件／站內風格） |

### 翻譯規則（含可信度）

| 規則 | 例 | 可信度 |
|---|---|---|
| 用 WP 詞彙表譯法 | sidebar → 資訊欄、block pattern → 區塊版面配置 | 官方文件 |
| 語言名稱稱「文」不稱「語」 | English → 英文 | 官方文件（詞彙表語言名稱列的 description 寫「介面中稱文不稱語」） |
| 品牌、產品名保留英文 | WordPress、Google | 站內風格 |
| 全形標點：，。「」（） | 「設定已儲存。」 | 站內風格 |
| 中英文、數字之間加半形空格 | 請使用 WordPress 外掛 | 站內風格 |
| 原文小寫開頭時，譯文不要以大寫英文起頭 | `an experiment by Automattic` → 由 Automattic 進行的實驗 | 站內風格（避免 Loco「missing the initial lowercase」警告） |
| 中文不加複數標記 | files → 檔案 | 站內風格 |

### 常用詞速查（全部在 glossary.csv 現行列查得到）

| English | 譯法 | English | 譯法 |
|---|---|---|---|
| plugin | 外掛 | featured image | 精選圖片 |
| theme | 佈景主題 | permalink | 永久連結 |
| widget | 小工具 | slug | 代稱 |
| dashboard | 控制台 | excerpt | 內容摘要 |
| sidebar | 資訊欄 | shortcode | 短代碼 |
| header | 頁首 | taxonomy | 分類法 |
| footer | 頁尾 | archive | 彙整 |
| hook | 勾點 | tagline | 網站說明 |
| administrator | 網站管理員 | contributor | 投稿者 |
| activate | 啟用 | deactivate | 停用 |

速查表以外的詞一律用 `search.py` 查。

## 驗證

| 產出 | 驗證器 | 通過標準 |
|---|---|---|
| 譯好的 .po | `python scripts/po.py validate <檔>` | **exit 0**（錯誤 0：無空譯、佔位符一致）。警告（HTML 標籤、首尾空白、結尾標點、首字大小寫、中國用語、用詞不一致）逐條看過，改或說明為何不改 |
| 一句或一段文字 | 把原文與譯文寫成暫存 .po（`msgid "<原文>"`／`msgstr "<譯文>"`），跑 `po.py validate` | 同上 |
| 查詞的回答 | 對回 `search.py` 輸出 | 譯法與命中列一致；查不到的已標「待補」並記進 pending.csv |

`validate` 只報告不修改；有錯一定回 1，可以直接當 CI／腳本關卡。

## 維護

```bash
python scripts/test_tools.py              # 自我測試（離線、標準庫）
python scripts/check_numbers.py           # 本檔數字與資料一致；--stats 印目前筆數
python tools/fetch_glossary.py            # 從 GlotPress 重抓詞彙表（連網），記擷取日
python tools/measure_fanhuaji.py          # 用繁化姬 API 重新實測 taiwan-terms.csv（連網）
python evals/grade.py --questions         # evals 題目；評分見 evals/grade.py 開頭說明
```

- 重抓詞彙表或重測繁化姬後：跑 `check_numbers.py --fix` 更新本檔數字 → 跑 `test_tools.py` → 重跑 evals，結果記 `evals/RESULTS.md`。
- 待補問題在 `data/pending.csv`，處理完把狀態改成 done 並寫明出處。
- 範例見 `EXAMPLES.md`；風格細節見 `references/STYLE_GUIDE.md`。
