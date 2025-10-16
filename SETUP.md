# 首次設定指南 (First-Time Setup Guide)

本指南將協助您完成 IMSHU 的首次設定。請依照順序完成所有步驟。

## ⚠️ 重要安全提醒

如果您是從 GitHub clone 此專案，以下檔案可能已經在舊版本中被追蹤：

- `.env`
- `client_secrets.json`
- `token.json`

**這些檔案包含敏感資訊！** 請務必：

1. ✅ 這些檔案已從 Git 追蹤中移除
2. ✅ 使用您自己的憑證和設定
3. ✅ 絕不分享這些檔案給他人
4. ✅ 如果曾經推送這些檔案到公開儲存庫，請立即更換所有密碼和金鑰

## 📋 設定步驟

### 步驟 1: 準備環境

1. **確認 Python 版本**

```bash
python --version
# 或
python3 --version

# 應該顯示 Python 3.10 或更高版本
```

2. **克隆專案**（如果尚未完成）

```bash
git clone https://github.com/Laiii151/IMSHU.git
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

4. **安裝依賴套件**

```bash
pip install -r requirements.txt
```

### 步驟 2: 建立環境變數檔案

1. **複製範本檔案**

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. **編輯 .env 檔案**

使用文字編輯器開啟 `.env` 檔案，並填入您的資訊：

```env
# 您的世新大學學號和密碼
SHU_USERNAME=你的學號
SHU_PASSWORD=你的密碼

# Flask 密鑰（請生成一個隨機字串）
APP_SECRET=your-random-secret-key-here

# 其他設定（通常使用預設值即可）
PORT=5000
HEADLESS=True
```

💡 **生成隨機密鑰**：

```bash
# 使用 Python
python -c "import secrets; print(secrets.token_hex(32))"

# 或使用 OpenSSL
openssl rand -hex 32
```

### 步驟 3: 設定 Google Drive API

#### 3.1 建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 登入您的 Google 帳號
3. 點擊左上角的專案下拉選單
4. 點擊「新增專案」
5. 輸入專案名稱（例如：`IMSHU`）
6. 點擊「建立」

#### 3.2 啟用 Google Drive API

1. 在 Google Cloud Console 中，選擇您剛建立的專案
2. 點擊左側選單的「API 和服務」→「程式庫」
3. 搜尋「Google Drive API」
4. 點擊「Google Drive API」
5. 點擊「啟用」按鈕

#### 3.3 建立 OAuth 2.0 憑證

1. 在左側選單點擊「API 和服務」→「憑證」
2. 點擊「建立憑證」→「OAuth 用戶端 ID」
3. 如果出現「設定同意畫面」的提示：
   - 點擊「設定同意畫面」
   - 使用者類型選擇「外部」
   - 點擊「建立」
   - 填寫必要資訊：
     - 應用程式名稱：`IMSHU`
     - 使用者支援電子郵件：您的 Email
     - 開發人員聯絡資訊：您的 Email
   - 點擊「儲存並繼續」
   - 在「範圍」頁面，點擊「儲存並繼續」
   - 在「測試使用者」頁面，點擊「新增使用者」，加入您的 Email
   - 點擊「儲存並繼續」
4. 回到「憑證」頁面，再次點擊「建立憑證」→「OAuth 用戶端 ID」
5. 應用程式類型選擇「**桌面應用程式**」
6. 名稱輸入「IMSHU Desktop Client」
7. 點擊「建立」

#### 3.4 下載憑證檔案

1. 在憑證列表中，找到剛建立的 OAuth 2.0 用戶端 ID
2. 點擊右側的下載圖示（⬇️）
3. 會下載一個 JSON 檔案（檔名類似 `client_secret_xxx.json`）
4. 將這個檔案重新命名為 `client_secrets.json`
5. 將 `client_secrets.json` 複製到 IMSHU 專案的根目錄

⚠️ **重要**：`client_secrets.json` 包含敏感資訊，請勿分享或上傳到公開位置！

#### 3.5 （選填）建立 Google Drive 目標資料夾

1. 開啟 [Google Drive](https://drive.google.com/)
2. 建立一個新資料夾（例如：`IMSHU_Data`）
3. 開啟該資料夾
4. 從瀏覽器網址列複製資料夾 ID
   - 網址格式：`https://drive.google.com/drive/folders/資料夾ID`
   - 複製最後一段（資料夾ID）
5. 將資料夾 ID 填入 `.env` 檔案：
   ```env
   GDRIVE_FOLDER_ID=你的資料夾ID
   ```

### 步驟 4: 首次執行與授權

1. **啟動應用程式**

```bash
python app.py
```

您應該會看到類似以下的輸出：

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

2. **開啟瀏覽器**

在瀏覽器中開啟 `http://localhost:5000`

3. **首次 Google Drive 授權**

第一次執行查詢時，系統會：
- 自動開啟瀏覽器視窗
- 要求您登入 Google 帳號
- 顯示授權請求頁面

請按照以下步驟授權：

1. 選擇您的 Google 帳號
2. 可能會出現「Google 尚未驗證這個應用程式」的警告
   - 點擊「進階」
   - 點擊「前往 IMSHU（不安全）」
3. 檢閱要求的權限
4. 點擊「允許」
5. 授權成功後，瀏覽器會顯示「已授權，可以關閉此視窗」

授權完成後，系統會在專案目錄下產生 `token.json` 檔案（此檔案包含存取 Token，請勿分享！）

### 步驟 5: 測試功能

1. **測試課表查詢**
   - 在網頁介面選擇「課表查詢」
   - 輸入學號和密碼（如果尚未在 .env 中設定）
   - 點擊「查詢」
   - 等待查詢完成

2. **確認上傳成功**
   - 開啟 Google Drive
   - 檢查是否有新的檔案或資料夾產生
   - 確認檔案內容正確

3. **測試其他功能**
   - 成績查詢
   - 排名查詢
   - 出缺勤查詢

## ✅ 設定完成檢查清單

請確認以下項目都已完成：

- [ ] Python 3.10+ 已安裝
- [ ] 依賴套件已安裝（`pip install -r requirements.txt`）
- [ ] `.env` 檔案已建立並填入正確資訊
- [ ] Google Cloud 專案已建立
- [ ] Google Drive API 已啟用
- [ ] OAuth 2.0 憑證已建立
- [ ] `client_secrets.json` 已下載並放置在專案根目錄
- [ ] 首次授權已完成
- [ ] `token.json` 已自動產生
- [ ] 測試查詢功能正常運作
- [ ] Google Drive 上傳功能正常運作

## 🔧 常見設定問題

### 問題 1: ImportError: No module named 'xxx'

**原因**：依賴套件未正確安裝

**解決方法**：
```bash
pip install -r requirements.txt
```

### 問題 2: FileNotFoundError: client_secrets.json

**原因**：OAuth 憑證檔案不存在或路徑錯誤

**解決方法**：
- 確認 `client_secrets.json` 在專案根目錄
- 檢查檔名是否正確（不是 `client_secret_xxx.json`）

### 問題 3: 授權視窗沒有自動開啟

**原因**：防火牆或瀏覽器設定問題

**解決方法**：
- 手動複製終端機顯示的網址到瀏覽器
- 檢查防火牆設定

### 問題 4: 授權後仍然失敗

**原因**：測試使用者未加入或應用程式未發布

**解決方法**：
- 回到 Google Cloud Console
- 「API 和服務」→「OAuth 同意畫面」
- 確認您的 Email 已加入測試使用者清單

### 問題 5: 找不到 Chrome/Chromium

**原因**：Selenium 需要瀏覽器驅動

**解決方法**：

Windows:
```bash
# 安裝 Chrome 瀏覽器
# 從 https://www.google.com/chrome/ 下載安裝
```

macOS:
```bash
brew install --cask google-chrome
```

Linux (Ubuntu/Debian):
```bash
sudo apt install chromium-browser chromium-chromedriver
```

### 問題 6: 學號或密碼錯誤

**原因**：.env 中的帳號密碼設定錯誤

**解決方法**：
- 確認 SHU_USERNAME 和 SHU_PASSWORD 正確
- 注意不要有多餘的空格或引號
- 先在校務系統網站測試帳號密碼是否正確

## 📚 下一步

設定完成後，您可以：

1. 閱讀 [README.md](README.md) 了解更多功能
2. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 學習如何部署到雲端
3. 參考 [SECURITY.md](SECURITY.md) 了解安全性最佳實踐
4. 查閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何貢獻程式碼

## 💬 需要協助？

如果遇到問題：

1. 查看 [常見問題](README.md#常見問題) 章節
2. 搜尋現有的 [GitHub Issues](https://github.com/Laiii151/IMSHU/issues)
3. 建立新的 Issue 描述您的問題

---

祝您設定順利！🎉
