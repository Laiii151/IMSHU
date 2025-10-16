# 貢獻指南 (Contributing Guide)

感謝您對 IMSHU 專案的興趣！我們歡迎各種形式的貢獻，包括但不限於：

- 🐛 回報錯誤 (Bug Reports)
- 💡 功能建議 (Feature Requests)
- 📝 文件改進 (Documentation)
- 🔧 程式碼貢獻 (Code Contributions)

## 📋 目錄

- [行為準則](#行為準則)
- [如何回報問題](#如何回報問題)
- [如何提出功能建議](#如何提出功能建議)
- [開發流程](#開發流程)
- [程式碼規範](#程式碼規範)
- [提交 Pull Request](#提交-pull-request)

## 🤝 行為準則

參與本專案的所有人都應該：

- 尊重他人的意見和觀點
- 接受建設性的批評
- 專注於對社群最有利的事情
- 對其他社群成員表示同理心

## 🐛 如何回報問題

如果您發現了 bug，請透過以下步驟回報：

1. **搜尋現有 Issues**：先確認是否已有人回報相同問題
2. **建立新 Issue**：如果沒有重複的問題，請建立新 Issue
3. **提供詳細資訊**：
   - 問題描述（越詳細越好）
   - 重現步驟
   - 預期行為
   - 實際行為
   - 環境資訊（作業系統、Python 版本、瀏覽器版本等）
   - 相關的錯誤訊息或截圖
   - 如果可能，提供日誌檔案（記得移除敏感資訊）

### Issue 範本

```markdown
## 問題描述
簡短描述遇到的問題

## 重現步驟
1. 執行...
2. 點擊...
3. 看到錯誤...

## 預期行為
應該要...

## 實際行為
實際上...

## 環境資訊
- OS: [e.g. Windows 11, macOS 14, Ubuntu 22.04]
- Python: [e.g. 3.10.5]
- Browser: [e.g. Chrome 120]
- IMSHU Version: [e.g. v1.0.0]

## 錯誤訊息
```
貼上錯誤訊息（記得移除敏感資訊）
```

## 額外資訊
其他可能有幫助的資訊
```

## 💡 如何提出功能建議

我們歡迎新功能建議！請透過以下步驟提出：

1. **搜尋現有 Issues**：確認是否已有類似建議
2. **建立新 Issue**：使用「Feature Request」標籤
3. **描述功能**：
   - 功能的目的和動機
   - 如何使用這個功能
   - 可能的實作方式（如果有想法）
   - 替代方案（如果有的話）

## 🛠️ 開發流程

### 設定開發環境

1. **Fork 專案**

```bash
# 在 GitHub 上點擊 Fork 按鈕
```

2. **Clone 到本地**

```bash
git clone https://github.com/你的使用者名稱/IMSHU.git
cd IMSHU
```

3. **建立虛擬環境**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. **安裝依賴**

```bash
pip install -r requirements.txt
```

5. **設定開發用 .env**

```bash
cp .env.example .env
# 編輯 .env 填入您的測試帳號
```

6. **建立功能分支**

```bash
git checkout -b feature/your-feature-name
```

### 開發建議

- 在修改程式碼前，先確保能正常執行現有功能
- 對於重大變更，建議先開 Issue 討論
- 保持每個 commit 的變更範圍小而專注
- 撰寫清晰的 commit 訊息

## 📐 程式碼規範

### Python 程式碼風格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 規範
- 使用 4 個空格縮排（不使用 Tab）
- 每行最多 120 字元
- 函式和類別需要有 docstring

### 命名慣例

- 變數和函式：`snake_case`
- 類別：`PascalCase`
- 常數：`UPPER_CASE`

### 註解規範

```python
def example_function(param1, param2):
    """
    簡短描述函式功能。
    
    Args:
        param1 (type): 參數說明
        param2 (type): 參數說明
    
    Returns:
        type: 回傳值說明
    
    Raises:
        Exception: 異常說明
    """
    pass
```

### 程式碼品質檢查

建議使用以下工具檢查程式碼品質：

```bash
# 安裝檢查工具
pip install flake8 black

# 執行檢查
flake8 .

# 自動格式化
black .
```

## 🎯 測試

### 手動測試

在提交 PR 前，請確保：

- [ ] 所有現有功能仍然正常運作
- [ ] 新功能按預期工作
- [ ] 在不同環境下測試（如果可能）
- [ ] 檢查日誌檔案是否有異常

### 測試檢查清單

- [ ] 課表查詢功能
- [ ] 成績查詢功能
- [ ] 排名查詢功能
- [ ] 出缺勤查詢功能
- [ ] Google Drive 上傳功能
- [ ] 錯誤處理機制
- [ ] 使用者介面顯示正常

## 📤 提交 Pull Request

### PR 準備

1. **確保程式碼品質**
   - 遵循程式碼規範
   - 移除除錯用的 print 語句
   - 更新相關文件

2. **撰寫清晰的 PR 描述**
   - 說明變更的目的
   - 列出主要變更項目
   - 提供測試方法（如果需要）
   - 附上相關的 Issue 編號

3. **小而專注的變更**
   - 每個 PR 專注於一個功能或修復
   - 避免在一個 PR 中混合多個不相關的變更

### PR 範本

```markdown
## 變更說明
簡短描述這個 PR 的目的

## 變更類型
- [ ] Bug 修復
- [ ] 新功能
- [ ] 文件更新
- [ ] 效能改善
- [ ] 程式碼重構

## 主要變更
- 變更項目 1
- 變更項目 2
- 變更項目 3

## 測試方式
1. 步驟 1
2. 步驟 2
3. 預期結果

## 相關 Issues
Closes #issue_number

## 檢查清單
- [ ] 程式碼遵循專案的程式碼規範
- [ ] 已測試所有變更
- [ ] 已更新相關文件
- [ ] 沒有產生新的警告
- [ ] 已移除除錯用程式碼
```

### PR 審查流程

1. 維護者會審查您的 PR
2. 可能會要求進行一些修改
3. 根據回饋進行調整
4. PR 被接受後會合併到主分支

## 📝 文件貢獻

文件改進也是很重要的貢獻！您可以：

- 修正拼寫或語法錯誤
- 改善現有文件的清晰度
- 新增遺漏的資訊
- 提供更多範例

## 🙏 感謝

感謝所有對 IMSHU 做出貢獻的人！您的參與讓這個專案變得更好。

## 💬 問題討論

如果有任何疑問，歡迎：

- 在 Issue 中提問
- 在 PR 中討論
- 透過 Email 聯繫維護者

---

再次感謝您的貢獻！🎉
