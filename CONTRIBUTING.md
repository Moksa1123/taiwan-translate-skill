# 貢獻指南

感謝你有興趣為 Taiwan Translate Skill 做出貢獻！

## 如何貢獻

### 回報問題

1. 先搜尋 [Issues](https://github.com/Moksa1123/taiwan-translate-skill/issues) 確認問題尚未被回報
2. 使用 Issue 模板描述問題
3. 提供重現步驟和環境資訊

### 提交 Pull Request

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 開發環境設定

```bash
# Clone 專案
git clone https://github.com/Moksa1123/taiwan-translate-skill.git
cd taiwan-translate-skill/translate-cli

# 安裝依賴
npm install

# 編譯
npm run build

# 本地測試
node dist/index.js init
```

## 程式碼規範

- 使用 TypeScript
- 遵循 ESLint 規則
- 提交訊息使用繁體中文或英文皆可
- 變數命名使用 camelCase

## 詞彙表貢獻

### 新增 WP 官方詞彙

編輯 `translate-cli/assets/taiwan-translate/data/glossary.csv`：

```csv
en,zh-tw,pos,description
new-term,新詞彙,noun,說明
```

### 新增繁化姬規則

編輯 `translate-cli/assets/taiwan-translate/data/taiwan-terms.csv`：

```csv
cn,tw,category,note
简体词,正體詞,dev,說明
```

## 測試

在提交 PR 前，請確保：

1. `npm run build` 編譯成功
2. `node dist/index.js list` 正常顯示
3. 新增的詞彙可被搜尋到

## 授權

貢獻的程式碼將採用與專案相同的 MIT 授權。

---

有任何問題歡迎開 Issue 討論！
