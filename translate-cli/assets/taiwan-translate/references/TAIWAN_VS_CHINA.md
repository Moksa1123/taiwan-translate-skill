# 台灣 vs 中國用語對照

翻譯時用台灣用語。每列的「依據」說明這個對照從哪裡來：

- **實測**：送進繁化姬台灣化轉換器（api.zhconvert.org，converter=Taiwan），輸出就是右欄。
- **官方文件**：WordPress 台灣社群詞彙表（GlotPress）把該英文詞譯成右欄。
- **站內風格**：本 skill 自己的用詞慣例，繁化姬不會這樣轉，WP 詞彙表也沒有這組對照。

完整清單與實測日期在 `data/taiwan-terms.csv`（`trust`、`measured_on` 欄），WP 譯法以 `python scripts/search.py <英文>` 為準。
這裡沒有的詞：照 SKILL.md 的鐵則先查，查不到記進 `data/pending.csv`，不要自己推。

## 基礎用語

| 中國大陸 | 台灣 | English | 依據 |
|---|---|---|---|
| 文件 | 檔案 | file | 官方文件 |
| 程序 | 程式 | program | 站內風格 |
| 軟件 | 軟體 | software | 實測 |
| 硬件 | 硬體 | hardware | 實測 |
| 數據 | 資料 | data | 官方文件 |
| 數據庫 | 資料庫 | database | 實測 |
| 網絡 | 網路 | network | 實測 |
| 服務器 | 伺服器 | server | 實測 |
| 內存 | 記憶體 | memory | 實測 |
| 接口 | 介面 | interface | 實測 |
| 窗口 | 視窗 | window | 官方文件 |
| 鼠標 | 滑鼠 | mouse | 實測 |
| 打印 | 列印 | print | 實測 |
| 登錄 | 登入 | login | 官方文件 |
| 賬號 | 帳號 | account | 實測 |
| 鏈接 | 連結 | link | 實測 |
| 默認 | 預設 | default | 官方文件 |
| 插件 | 外掛 | plugin | 官方文件 |

## 開發用語

| 中國大陸 | 台灣 | English | 依據 |
|---|---|---|---|
| 代碼 | 程式碼 | code | 官方文件 |
| 變量 | 變數 | variable | 實測 |
| 函數 | 函式 | function | 官方文件 |
| 數組 | 陣列 | array | 官方文件 |
| 字符串 | 字串 | string | 實測 |
| 對象 | 物件 | object | 官方文件 |
| 線程 | 執行緒 | thread | 實測 |
| 進程 | 程序 | process | 站內風格 |
| 調試 | 除錯 | debug | 實測 |
| 算法 | 演算法 | algorithm | 官方文件 |
| 循環 | 迴圈 | loop | 官方文件 |
| 遞歸 | 遞迴 | recursion | 實測 |
| 異步 | 非同步 | async | 實測 |
| 回調 | 回呼 | callback | 官方文件 |
| 緩存 | 快取 | cache | 實測 |
| 堆棧 | 堆疊 | stack | 站內風格 |
| 隊列 | 佇列 | queue | 站內風格 |

## UI 用語

| 中國大陸 | 台灣 | English | 依據 |
|---|---|---|---|
| 菜單 | 選單 | menu | 官方文件 |
| 工具欄 | 工具列 | toolbar | 站內風格 |
| 狀態條 | 狀態列 | status bar | 站內風格 |
| 標籤頁 | 分頁 | tab | 官方文件 |
| 配置 | 設定 | configuration | 站內風格 |
| 設置 | 設定 | settings | 站內風格 |
| 激活 | 啟用 | activate | 實測 |
| 禁用 | 停用 | disable | 官方文件 |
| 導入 | 匯入 | import | 官方文件 |
| 導出 | 匯出 | export | 官方文件 |
| 粘貼 | 貼上 | paste | 站內風格 |
| 剪切 | 剪下 | cut | 站內風格 |
| 撤銷 | 復原 | undo | 官方文件 |
| 刷新 | 重新整理 | refresh | 官方文件 |
| 加載 | 載入 | load | 站內風格 |
