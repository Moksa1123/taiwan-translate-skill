# {{TITLE}}

> {{DESCRIPTION}}

## 何時使用此技能

- 翻譯 WordPress 外掛/佈景主題
- 翻譯軟體介面文字
- 查詢標準譯法
- 處理 .po/.pot 檔案

## 智能搜尋與翻譯

### 搜尋引擎 (search.py)

使用 BM25 算法搜尋詞彙表：

```bash
# 搜尋英文詞彙
python scripts/search.py "plugin"

# 搜尋中文詞彙
python scripts/search.py "外掛" --domain zh

# JSON 輸出
python scripts/search.py "theme" --format json
```

### 詞彙查詢 (lookup.py)

> 理念：詞彙表僅供參考，**不做整句自動代換**。整句翻譯由模型完成，再用 `po.py validate` 把關。

```bash
# 列出一句話命中的詞彙（供翻譯參考）
python scripts/lookup.py "Please select a theme"
```

### PO 工具 (po.py)

```bash
# 抽出未翻譯項目（交給模型翻譯）
python scripts/po.py extract path/to/plugin.pot

# 翻譯把關（佔位符/首字/中國用語/空格…）
python scripts/po.py validate path/to/plugin.po
```

## 核心詞彙速查表

### WordPress 專有名詞

| English | 台灣正體中文 |
|---------|-------------|
| plugin | 外掛 |
| theme | 佈景主題 |
| widget | 小工具 |
| block | 區塊 |
| dashboard | 控制台 |
| post | 文章 |
| page | 頁面 |
| category | 分類 |
| tag | 標籤 |
| media library | 媒體庫 |

### 動作動詞

| English | 台灣正體中文 |
|---------|-------------|
| activate | 啟用 |
| deactivate | 停用 |
| save | 儲存 |
| delete | 刪除 |
| edit | 編輯 |
| upload | 上傳 |
| download | 下載 |
| import | 匯入 |
| export | 匯出 |
| login | 登入 |
| logout | 登出 |

### 系統詞彙

| English | 台灣正體中文 |
|---------|-------------|
| file | 檔案 |
| folder | 資料夾 |
| settings | 設定 |
| options | 選項 |
| database | 資料庫 |
| server | 伺服器 |
| cache | 快取 |
| error | 錯誤 |
| warning | 警告 |

## 台灣 vs 中國用語對照

翻譯時**必須使用台灣用語**：

| 台灣 | 中國大陸 | English |
|------|----------|---------|
| 檔案 | 文件 | file |
| 程式 | 程序 | program |
| 軟體 | 软件 | software |
| 資料 | 数据 | data |
| 伺服器 | 服务器 | server |
| 外掛 | 插件 | plugin |
| 佈景主題 | 主题 | theme |

## 翻譯規則

1. **語言名稱**：稱「文」不稱「語」（英文、日文、法文）
2. **品牌名稱**：保留英文（WordPress, Google, Apple）
3. **標點符號**：使用全形標點（，。、；：「」）
4. **中英混排**：中英文之間加半形空格
5. **首字大小寫**：原文小寫開頭時，譯文勿以大寫英文起頭，改以中文字或符號開頭（避免 Loco「missing the initial lowercase」誤報）

## 詞彙表來源

- [WordPress 台灣漢文字彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/)
- [GitHub: WordPress-zh_TW-Glossary](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)

---

*Taiwan Traditional Chinese Translation Skill*
