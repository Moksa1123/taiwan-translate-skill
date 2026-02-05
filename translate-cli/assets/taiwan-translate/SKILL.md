---
name: tw-translate
description: 台灣正體中文翻譯工具。使用 WordPress 台灣社群官方詞彙表，翻譯軟體介面、外掛、佈景主題等文字。支援 .po/.pot 檔案翻譯、詞彙查詢、文字翻譯。
user-invocable: true
---

# 台灣正體中文翻譯技能

> 此技能採用雙來源策略，協助將英文及簡體中文翻譯成符合台灣用語習慣的正體中文。

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

| 來源 | 優先順序 | 詞彙數量 | 說明 |
|------|----------|----------|------|
| WP 官方 | 1 (最高) | 2,300+ | WordPress 台灣社群官方詞彙表 |
| 繁化姬 | 2 (備用) | 130+ | 簡體中文轉台灣正體中文規則 |

## 快速導覽

### 相關文件
- `references/STYLE_GUIDE.md` - 翻譯風格指南
- `references/TAIWAN_VS_CHINA.md` - 台灣 vs 中國用語對照
- `data/glossary.csv` - WP 官方詞彙表（2,300+ 詞彙）
- `data/taiwan-terms.csv` - 繁化姬台灣化規則（130+ 詞彙）

### 智能工具
- `scripts/search.py` - BM25 詞彙搜尋引擎
- `scripts/translate.py` - 自動翻譯工具

### 何時使用此技能
- 翻譯 WordPress 外掛/佈景主題
- 翻譯軟體介面文字
- 查詢標準譯法
- 處理 .po/.pot 檔案

---

## 智能搜尋與翻譯

### 搜尋引擎 (search.py)

使用 BM25 算法搜尋詞彙表（支援雙來源）：

```bash
# 搜尋英文詞彙
python scripts/search.py "plugin"

# 搜尋中文詞彙（包含簡體轉換）
python scripts/search.py "外掛" --domain zh

# 限制結果數量
python scripts/search.py "setting" --limit 20

# JSON 輸出
python scripts/search.py "theme" --format json

# 只搜尋特定來源
python scripts/search.py "設置" --source fanhuaji
```

**搜尋範圍：**
| 參數 | 說明 |
|------|------|
| `--domain all` | 搜尋全部欄位（預設）|
| `--domain en` | 只搜尋英文 |
| `--domain zh` | 只搜尋中文 |

**來源篩選：**
| 參數 | 說明 |
|------|------|
| `--source all` | 搜尋全部來源（預設）|
| `--source wp` | 只搜尋 WP 官方 |
| `--source fanhuaji` | 只搜尋繁化姬 |

### 翻譯工具 (translate.py)

自動翻譯（WP 官方優先，繁化姬備用）：

```bash
# 翻譯英文文字
python scripts/translate.py "Please select a theme"

# 翻譯簡體中文為台灣正體
python scripts/translate.py "请选择一个默认设置"

# 翻譯檔案
python scripts/translate.py --file input.txt

# 翻譯 PO 檔案
python scripts/translate.py --po path/to/plugin.po

# JSON 輸出
python scripts/translate.py "Click Settings" --format json
```

輸出會顯示詞彙來源統計（WP官方 / 繁化姬）。

---

## 核心詞彙速查表

### WordPress 專有名詞
| English | 台灣正體中文 |
|---------|-------------|
| plugin | 外掛 |
| theme | 佈景主題 |
| widget | 小工具 |
| block | 區塊 |
| shortcode | 短代碼 |
| dashboard | 控制台 |
| admin bar | 工具列 |
| sidebar | 側邊欄 |
| header | 頁首 |
| footer | 頁尾 |
| post | 文章 |
| page | 頁面 |
| category | 分類 |
| tag | 標籤 |
| taxonomy | 分類法 |
| custom post type | 自訂文章類型 |
| custom field | 自訂欄位 |
| featured image | 精選圖片 |
| permalink | 永久連結 |
| slug | 代稱 |
| excerpt | 內容摘要 |
| media library | 媒體庫 |
| hook | 勾點 |
| action hook | 動作勾點 |
| filter hook | 篩選器勾點 |

### 使用者角色
| English | 台灣正體中文 |
|---------|-------------|
| administrator | 網站管理員 |
| editor | 編輯 |
| author | 作者 |
| contributor | 投稿者 |
| subscriber | 訂閱者 |
| super admin | 超級管理員 |

### 動作動詞
| English | 台灣正體中文 |
|---------|-------------|
| activate | 啟用 |
| deactivate | 停用 |
| install | 安裝 |
| uninstall | 解除安裝 |
| update | 更新 |
| upgrade | 升級 |
| download | 下載 |
| upload | 上傳 |
| import | 匯入 |
| export | 匯出 |
| save | 儲存 |
| delete | 刪除 |
| edit | 編輯 |
| add | 新增 |
| create | 建立 |
| publish | 發佈 |
| preview | 預覽 |
| search | 搜尋 |
| filter | 篩選 |
| submit | 送出 |
| cancel | 取消 |
| confirm | 確認 |
| login | 登入 |
| logout | 登出 |
| register | 註冊 |

### 系統詞彙
| English | 台灣正體中文 |
|---------|-------------|
| file | 檔案 |
| folder | 資料夾 |
| directory | 目錄 |
| path | 路徑 |
| URL | 網址 |
| link | 連結 |
| database | 資料庫 |
| server | 伺服器 |
| cache | 快取 |
| backup | 備份 |
| settings | 設定 |
| options | 選項 |
| default | 預設 |
| custom | 自訂 |
| error | 錯誤 |
| warning | 警告 |

---

## 台灣 vs 中國用語對照

翻譯時**必須使用台灣用語**（來自繁化姬台灣化規則）：

### 基礎用語
| 中國大陸 | 台灣 | English |
|----------|------|---------|
| 文件 | 檔案 | file |
| 程序 | 程式 | program |
| 軟件 | 軟體 | software |
| 硬件 | 硬體 | hardware |
| 數據 | 資料 | data |
| 數據庫 | 資料庫 | database |
| 網絡 | 網路 | network |
| 服務器 | 伺服器 | server |
| 內存 | 記憶體 | memory |
| 接口 | 介面 | interface |
| 窗口 | 視窗 | window |
| 鼠標 | 滑鼠 | mouse |
| 打印 | 列印 | print |
| 登錄 | 登入 | login |
| 賬號 | 帳號 | account |
| 鏈接 | 連結 | link |
| 默認 | 預設 | default |
| 插件 | 外掛 | plugin |

### 開發用語
| 中國大陸 | 台灣 | English |
|----------|------|---------|
| 代碼 | 程式碼 | code |
| 變量 | 變數 | variable |
| 函數 | 函式 | function |
| 數組 | 陣列 | array |
| 字符串 | 字串 | string |
| 對象 | 物件 | object |
| 線程 | 執行緒 | thread |
| 進程 | 程序 | process |
| 調試 | 除錯 | debug |
| 算法 | 演算法 | algorithm |
| 循環 | 迴圈 | loop |
| 遞歸 | 遞迴 | recursion |
| 異步 | 非同步 | async |
| 回調 | 回呼 | callback |
| 緩存 | 快取 | cache |
| 堆棧 | 堆疊 | stack |
| 隊列 | 佇列 | queue |

### UI 用語
| 中國大陸 | 台灣 | English |
|----------|------|---------|
| 菜單 | 選單 | menu |
| 工具欄 | 工具列 | toolbar |
| 狀態條 | 狀態列 | status bar |
| 標籤頁 | 分頁 | tab |
| 配置 | 設定 | configuration |
| 設置 | 設定 | settings |
| 激活 | 啟用 | activate |
| 禁用 | 停用 | disable |
| 導入 | 匯入 | import |
| 導出 | 匯出 | export |
| 粘貼 | 貼上 | paste |
| 剪切 | 剪下 | cut |
| 撤銷 | 復原 | undo |
| 刷新 | 重新整理 | refresh |
| 加載 | 載入 | load |

---

## 翻譯規則

### 1. 語言名稱
稱「文」不稱「語」：
- English → 英文（不是英語）
- Japanese → 日文（不是日語）
- French → 法文（不是法語）

### 2. 品牌名稱
保留英文原名：
- WordPress（不翻譯）
- Google（不翻譯）
- Apple（不翻譯）

### 3. 標點符號
使用全形標點：
- 逗號：，（不是 ,）
- 句號：。（不是 .）
- 引號：「」『』（不是 "" ''）
- 括號：（）（不是 ()）

### 4. 中英混排
中英文之間加半形空格：
- 請使用 WordPress 5.0 以上版本
- 前往 Settings 頁面

### 5. 複數處理
中文不需要複數標記：
- files → 檔案（不是「檔案們」）
- users → 使用者（不是「使用者們」）

---

## 翻譯工作流程

### 翻譯一般文字

1. **搜尋詞彙**
```bash
python scripts/search.py "<關鍵字>"
```

2. **翻譯文字**
```bash
python scripts/translate.py "<英文文字>"
```

### 翻譯 .po/.pot 檔案

1. **執行翻譯**
```bash
python scripts/translate.py --po path/to/plugin.pot
```

2. **檢查輸出**
- 輸出檔案：`plugin-translated.po`
- 手動審核需要調整的翻譯

3. **完成**
- 將翻譯好的 .po 檔案放回原位置

---

## 常見問題

### Q: 找不到某個詞彙的翻譯？

1. 先用搜尋工具查詢：
```bash
python scripts/search.py "<詞彙>" --limit 20
```

2. 如果找不到，參考相似詞彙或台灣用語習慣

### Q: 同一個詞有多種翻譯？

根據詞性和上下文選擇：
- **名詞** vs **動詞**：如 update（名詞：更新 / 動詞：更新）
- **技術用語** vs **一般用語**：如 post（文章 vs 貼文）

### Q: 如何處理專有名詞？

- 軟體/服務名稱：保留英文（WordPress, Google）
- 技術術語：使用詞彙表標準譯法
- 無標準譯法：音譯或意譯並標註原文

---

## 參考資料

詞彙表來源：
- [WordPress 台灣漢文字彙表](https://translate.wordpress.org/locale/zh-tw/default/glossary/)
- [GitHub: WordPress-zh_TW-Glossary](https://github.com/WordPress-Taiwan/WordPress-zh_TW-Glossary)
- [繁化姬 Fanhuaji](https://github.com/Fanhuaji/Sublime-Fanhuaji) - 台灣化轉換規則

---

*Taiwan Traditional Chinese Translation Skill v1.1*
*支援雙來源策略：WP 官方 + 繁化姬*
*詞彙表更新日期：2026/02*
