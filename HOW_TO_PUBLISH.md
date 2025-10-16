# 如何將專案公開到 GitHub (How to Publish to GitHub)

本文件說明如何將 IMSHU 專案公開發佈到 GitHub，讓其他人可以使用。

## 📋 發佈前檢查清單

在將您的儲存庫設為公開之前，請確認：

### 1. 敏感資訊檢查

- [ ] `.env` 檔案已加入 `.gitignore` 且未被追蹤
- [ ] `client_secrets.json` 未被追蹤
- [ ] `token.json` 未被追蹤
- [ ] `data/` 目錄未被追蹤
- [ ] `logs/` 目錄未被追蹤
- [ ] 沒有硬編碼的密碼或 API 金鑰
- [ ] 所有敏感資訊都使用環境變數

**檢查方法**：

```bash
# 查看被 Git 追蹤的所有檔案
git ls-files

# 檢查是否有敏感檔案
git ls-files | grep -E '\.env$|client_secrets|token\.json|data/|logs/'

# 應該沒有輸出，如果有，請移除追蹤
git rm --cached 檔案名稱
```

### 2. 文件完整性檢查

- [ ] `README.md` 已更新並包含完整說明
- [ ] `SETUP.md` 已建立（首次設定指南）
- [ ] `DEPLOYMENT.md` 已建立（部署指南）
- [ ] `CONTRIBUTING.md` 已建立（貢獻指南）
- [ ] `SECURITY.md` 已建立（安全性指南）
- [ ] `SECURITY_NOTICE.md` 已建立（安全公告）
- [ ] `LICENSE` 已建立（授權條款）
- [ ] `.env.example` 已建立（環境變數範本）

### 3. 程式碼品質檢查

- [ ] 移除除錯用的 `print()` 語句
- [ ] 移除註解掉的程式碼
- [ ] 程式碼格式一致
- [ ] 沒有硬編碼的路徑或設定

### 4. 儲存庫設定

- [ ] `.gitignore` 已正確設定
- [ ] 有意義的 commit 訊息
- [ ] 分支結構清晰（建議使用 `main` 作為主分支）

## 🚀 發佈步驟

### 方法一：GitHub 網頁介面

1. **前往您的儲存庫**
   - 登入 [GitHub](https://github.com/)
   - 開啟您的 IMSHU 儲存庫

2. **變更可見度設定**
   - 點擊「Settings」（設定）
   - 滾動到最下方的「Danger Zone」（危險區域）
   - 點擊「Change repository visibility」（變更儲存庫可見度）
   - 選擇「Make public」（設為公開）
   - 輸入儲存庫名稱確認
   - 點擊「I understand, change repository visibility」

3. **確認發佈**
   - 重新整理儲存庫頁面
   - 確認沒有 🔒 符號（代表已公開）
   - 使用無痕視窗測試是否能正常訪問

### 方法二：從私有儲存庫 Fork

如果您的原始儲存庫包含敏感資訊的歷史記錄：

1. **建立新的公開儲存庫**
   ```bash
   # 在 GitHub 上建立一個新的空白儲存庫（設為公開）
   ```

2. **推送乾淨的程式碼**
   ```bash
   # Clone 您的私有儲存庫
   git clone <私有儲存庫URL>
   cd IMSHU
   
   # 移除舊的遠端
   git remote remove origin
   
   # 新增新的遠端（公開儲存庫）
   git remote add origin <新的公開儲存庫URL>
   
   # 推送到新儲存庫
   git push -u origin main
   ```

## 📝 發佈後的設定

### 1. 設定儲存庫資訊

在 GitHub 儲存庫頁面：

1. 點擊右上角的 ⚙️ 圖示（About 設定）
2. 填寫以下資訊：
   - **Description**（描述）：
     ```
     世新大學校務系統資料查詢工具 - 自動抓取課表、成績、排名、出缺勤資料並上傳至 Google Drive
     ```
   - **Website**（網站）：如果有部署的 demo 網站，填入網址
   - **Topics**（主題標籤）：
     ```
     flask, python, web-scraping, selenium, google-drive-api, education, automation, shu
     ```
3. 勾選「Releases」、「Packages」（如果適用）
4. 點擊「Save changes」

### 2. 設定預設分支

1. 前往「Settings」→「Branches」
2. 確認預設分支為 `main`
3. （選填）設定分支保護規則：
   - 勾選「Require pull request reviews before merging」
   - 勾選「Require status checks to pass before merging」

### 3. 建立發佈版本（Release）

1. 前往儲存庫首頁
2. 點擊右側的「Releases」
3. 點擊「Create a new release」
4. 填寫資訊：
   - **Tag version**: `v1.0.0`
   - **Release title**: `IMSHU v1.0.0 - 初始版本`
   - **Description**:
     ```markdown
     ## 🎉 首次發佈
     
     IMSHU v1.0.0 正式發佈！
     
     ### ✨ 主要功能
     - 課表自動查詢與下載
     - 成績自動查詢與下載
     - 排名自動查詢與下載
     - 出缺勤自動查詢與下載
     - 自動上傳至 Google Drive
     - 支援 Docker 部署
     - 支援 Render.com 部署
     
     ### 📚 文件
     - [快速開始指南](https://github.com/Laiii151/IMSHU#快速開始)
     - [完整設定指南](SETUP.md)
     - [部署指南](DEPLOYMENT.md)
     
     ### ⚠️ 注意事項
     請務必閱讀 [安全性指南](SECURITY.md) 和 [安全公告](SECURITY_NOTICE.md)
     ```
5. 點擊「Publish release」

### 4. 建立 GitHub Pages（選填）

如果想要建立專案文件網站：

1. 前往「Settings」→「Pages」
2. Source 選擇「Deploy from a branch」
3. Branch 選擇 `main` 和 `/docs`（需要先建立 docs 資料夾）
4. 點擊「Save」

### 5. 設定議題範本（Issue Templates）

建立 `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug 回報
about: 回報錯誤以協助我們改進
title: '[BUG] '
labels: bug
assignees: ''
---

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

## 錯誤訊息
```
貼上錯誤訊息
```

## 額外資訊
其他可能有幫助的資訊
```

建立 `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: 功能建議
about: 建議新功能
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## 功能描述
簡短描述建議的新功能

## 動機
為什麼需要這個功能？

## 使用方式
如何使用這個功能？

## 替代方案
有沒有其他解決方法？

## 額外資訊
其他補充說明
```

## 🌟 推廣您的專案

### 1. 撰寫部落格文章

分享：
- 開發動機
- 技術挑戰
- 使用教學
- 心得感想

### 2. 社群媒體分享

- Twitter/X
- Reddit (r/Python, r/learnprogramming)
- PTT
- Dcard
- Facebook 社團

### 3. 新增到專案列表

- [Awesome Python](https://github.com/vinta/awesome-python)
- [Python Weekly](https://www.pythonweekly.com/)
- 其他相關的 awesome lists

### 4. 持續維護

- 回應 Issues
- 審查 Pull Requests
- 定期更新文件
- 修復 bugs
- 新增功能

## 📊 監控專案狀態

### 1. GitHub Insights

前往「Insights」查看：
- 訪客數量
- Clone 數量
- Fork 數量
- Star 數量
- 貢獻者

### 2. 設定通知

1. 前往「Settings」→「Notifications」
2. 設定接收通知的類型：
   - Issues
   - Pull Requests
   - Releases
   - Discussions

### 3. 新增徽章（Badges）

在 README.md 中新增狀態徽章：

```markdown
![GitHub stars](https://img.shields.io/github/stars/Laiii151/IMSHU)
![GitHub forks](https://img.shields.io/github/forks/Laiii151/IMSHU)
![GitHub issues](https://img.shields.io/github/issues/Laiii151/IMSHU)
![GitHub license](https://img.shields.io/github/license/Laiii151/IMSHU)
![Python version](https://img.shields.io/badge/python-3.10+-blue.svg)
```

## ⚠️ 常見錯誤

### 錯誤 1: 敏感資訊已在 Git 歷史中

**解決方法**：
- 清除 Git 歷史（參考 [SECURITY_NOTICE.md](SECURITY_NOTICE.md)）
- 或建立新的乾淨儲存庫

### 錯誤 2: 文件不完整

**解決方法**：
- 確保 README.md 包含完整的使用說明
- 新增 SETUP.md 詳細設定步驟

### 錯誤 3: 授權條款未明確

**解決方法**：
- 新增 LICENSE 檔案（已使用 MIT License）
- 在 README.md 中說明授權條款

## ✅ 發佈檢查表

最後確認：

- [ ] 所有敏感資訊已移除
- [ ] 文件完整且正確
- [ ] README.md 清晰易懂
- [ ] .gitignore 設定正確
- [ ] LICENSE 已新增
- [ ] 儲存庫可見度已設為公開
- [ ] 儲存庫描述已填寫
- [ ] Topics 標籤已設定
- [ ] 首個 Release 已發佈
- [ ] Issue templates 已建立
- [ ] 已在社群媒體分享

## 🎉 恭喜發佈！

您的專案現在已經公開，可以讓全世界的人使用了！

記得：
- 定期更新文件
- 回應使用者問題
- 接受社群貢獻
- 持續改進專案

---

祝您的專案大受歡迎！⭐
