# ⚠️ 重要安全公告 (Security Notice)

## 關於敏感檔案的歷史提交

如果您在 **2024年10月16日之前** 從此儲存庫克隆或 fork，請注意：

在該日期之前，以下敏感檔案可能已被錯誤地提交到 Git 歷史記錄中：

- `.env` - 包含帳號密碼
- `client_secrets.json` - Google OAuth 憑證
- `token.json` - Google OAuth 存取 Token

## 📌 已採取的行動

✅ 這些檔案已從 Git 追蹤中移除（2024-10-16）
✅ 已更新 `.gitignore` 防止未來再次提交
✅ 所有文件都已更新以包含安全性最佳實踐

## ⚠️ 如果您受到影響

如果您在此日期之前克隆了此儲存庫，或您的 fork 中包含這些敏感檔案，請立即採取以下行動：

### 1. 立即更換所有敏感資訊

```bash
# 1. 更改您的世新大學密碼
# 2. 撤銷 Google OAuth 憑證
# 3. 建立新的 OAuth 憑證
```

### 2. 撤銷 Google OAuth 憑證

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 選擇您的專案
3. 前往「API 和服務」→「憑證」
4. 刪除舊的 OAuth 2.0 用戶端 ID
5. 建立新的憑證（參考 [SETUP.md](SETUP.md)）

### 3. 清除 Git 歷史記錄（選填）

如果您想從 Git 歷史記錄中完全移除這些檔案：

```bash
# 使用 git filter-branch（較慢但內建）
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env client_secrets.json token.json" \
  --prune-empty --tag-name-filter cat -- --all

# 或使用 BFG Repo-Cleaner（推薦，更快）
# 1. 下載 BFG: https://rtyley.github.io/bfg-repo-cleaner/
# 2. 執行：
java -jar bfg.jar --delete-files "{.env,client_secrets.json,token.json}"

# 強制推送（警告：這會改寫歷史記錄）
git push origin --force --all
git push origin --force --tags
```

⚠️ **警告**：清除 Git 歷史記錄會影響所有協作者。如果有其他人 fork 或克隆了您的儲存庫，他們也需要重新 clone。

### 4. 對於 Fork 的儲存庫

如果您 fork 了這個專案：

1. 刪除您的 fork
2. 重新 fork 最新版本
3. 重新設定您的環境（使用新的憑證）

## 🔒 未來的安全措施

為了防止類似問題再次發生：

1. ✅ 所有敏感檔案已加入 `.gitignore`
2. ✅ 提供 `.env.example` 作為範本
3. ✅ 新增完整的安全性文件 ([SECURITY.md](SECURITY.md))
4. ✅ 新增詳細的設定指南 ([SETUP.md](SETUP.md))
5. ✅ README 中包含完整的安全警告

## 📋 檢查清單

如果您是新使用者或受影響的使用者：

- [ ] 已閱讀此安全公告
- [ ] 已更改世新大學密碼（如果受影響）
- [ ] 已撤銷並重建 Google OAuth 憑證（如果受影響）
- [ ] 已使用新的憑證設定環境
- [ ] 已確認 `.env`、`client_secrets.json`、`token.json` 不在 Git 追蹤中
- [ ] 已清除個人 fork 的 Git 歷史記錄（如果需要）

## 🙏 致歉

我們對這個疏忽深感抱歉。資訊安全是我們的首要任務，我們已採取措施確保這種情況不再發生。

## 📞 需要協助？

如果您對此安全問題有任何疑問或需要協助：

1. 建立 [GitHub Issue](https://github.com/Laiii151/IMSHU/issues)（不要在 Issue 中包含任何敏感資訊）
2. 或透過 Email 私下聯繫維護者

---

**最後更新日期**: 2024-10-16
