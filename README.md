# IMSHU - 世新大學校務系統資料查詢工具

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ⚠️ 重要安全提醒

> **在開始使用之前，請務必閱讀 [安全公告](SECURITY_NOTICE.md)**
> 
> 本專案包含敏感資訊設定。請：
> - ✅ 使用您自己的憑證和密碼
> - ✅ 絕不將 `.env`、`client_secrets.json`、`token.json` 上傳到公開位置
> - ✅ 定期更換密碼和金鑰
> - ✅ 閱讀 [安全性指南](SECURITY.md) 了解更多資訊

## 📖 專案簡介

IMSHU 是一個針對世新大學校務系統設計的資料查詢工具，可以幫助學生自動抓取並整理以下資料：

- 📅 **課表查詢** (Timetable)
- 📊 **成績查詢** (Grades)
- 🏆 **排名查詢** (Ranking)
- 📝 **出缺勤查詢** (Attendance)

查詢完成後，資料會自動上傳到您的 Google Drive，方便隨時查閱與備份。

## ✨ 主要功能

- ✅ 自動登入世新大學校務系統
- ✅ 抓取課表、成績、排名、出缺勤等資料
- ✅ 自動轉換為 CSV 格式並整理
- ✅ 自動上傳至 Google Drive（支援覆蓋同名舊檔）
- ✅ 提供網頁介面進行查詢與下載
- ✅ 支援 Docker 部署
- ✅ 支援 Render.com 雲端部署

## 🚀 快速開始

> 📘 **首次使用？** 請參考詳細的 [設定指南 (SETUP.md)](SETUP.md)

### 前置需求

- Python 3.10 或以上版本
- Google Cloud Platform 帳號（用於 Google Drive API）
- 世新大學學號與密碼

### 本地安裝

1. **克隆專案**

```bash
git clone https://github.com/Laiii151/IMSHU.git
cd IMSHU
```

2. **安裝依賴**

```bash
pip install -r requirements.txt
```

3. **設定環境變數**

建立 `.env` 檔案並設定以下變數：

```env
# 世新大學帳號密碼
SHU_USERNAME=你的學號
SHU_PASSWORD=你的密碼

# Flask 設定
APP_SECRET=your-secret-key-here
PORT=5000

# Selenium 設定（本地開發可設為 False）
HEADLESS=True

# Google Drive 資料夾 ID（選填，留空則上傳到根目錄）
GDRIVE_FOLDER_ID=

# 逾時設定（秒）
TIMEOUT_TIMETABLE=240
TIMEOUT_GRADES=300
TIMEOUT_RANKING=300
TIMEOUT_ATTENDANCE=300
```

4. **設定 Google Drive API**

請參考 [Google Drive API 設定指南](#google-drive-api-設定) 章節。

5. **執行應用程式**

```bash
python app.py
```

開啟瀏覽器訪問 `http://localhost:5000`

## 🔑 Google Drive API 設定

### 步驟 1: 建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 專案名稱可以設定為 "IMSHU" 或任何您喜歡的名稱

### 步驟 2: 啟用 Google Drive API

1. 在側邊欄選擇「API 和服務」→「資料庫」
2. 搜尋「Google Drive API」
3. 點擊「啟用」

### 步驟 3: 建立 OAuth 2.0 憑證

1. 在「API 和服務」中選擇「憑證」
2. 點擊「建立憑證」→「OAuth 用戶端 ID」
3. 應用程式類型選擇「桌面應用程式」
4. 名稱可設定為 "IMSHU Desktop Client"
5. 點擊「建立」

### 步驟 4: 下載憑證檔案

1. 在憑證列表中找到剛建立的 OAuth 2.0 用戶端 ID
2. 點擊下載圖示（⬇️）
3. 將下載的 JSON 檔案重新命名為 `client_secrets.json`
4. 將檔案放在專案根目錄

### 步驟 5: 首次授權

第一次執行應用程式時，系統會自動開啟瀏覽器進行 OAuth 授權：

1. 選擇您的 Google 帳號
2. 點擊「允許」授予 Google Drive 存取權限
3. 授權成功後會自動產生 `token.json` 檔案

⚠️ **重要提醒**：`token.json` 和 `client_secrets.json` 包含敏感資訊，請勿上傳至 GitHub 或公開分享。

## 🐳 Docker 部署

### 使用 Docker 建置並執行

```bash
# 建置 Docker 映像
docker build -t imshu .

# 執行容器
docker run -d \
  -p 5000:5000 \
  -e SHU_USERNAME=你的學號 \
  -e SHU_PASSWORD=你的密碼 \
  -e APP_SECRET=your-secret-key \
  -e HEADLESS=True \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --name imshu \
  imshu
```

### 查看容器日誌

```bash
docker logs -f imshu
```

## ☁️ Render.com 部署

### 步驟 1: 準備 Render 帳號

1. 前往 [Render.com](https://render.com/) 註冊帳號
2. 連結您的 GitHub 帳號

### 步驟 2: 建立 Web Service

1. 點擊「New +」→「Web Service」
2. 選擇此 GitHub 儲存庫
3. 設定如下：
   - **Name**: `imshu`（或任何您喜歡的名稱）
   - **Environment**: `Docker`
   - **Region**: 選擇離您最近的區域
   - **Branch**: `main`

### 步驟 3: 設定環境變數

在 Render 面板中新增以下環境變數：

- `SHU_USERNAME`: 您的學號
- `SHU_PASSWORD`: 您的密碼
- `APP_SECRET`: 隨機字串（用於 Flask session）
- `HEADLESS`: `True`
- `GDRIVE_FOLDER_ID`: （選填）您的 Google Drive 資料夾 ID

### 步驟 4: 部署

點擊「Create Web Service」，Render 會自動部署您的應用程式。

⚠️ **注意**：由於 Render 的免費方案限制，容器可能會在一段時間後休眠。

## 📂 專案結構

```
IMSHU/
├── app.py                    # Flask 主程式
├── requirements.txt          # Python 依賴套件
├── Dockerfile               # Docker 設定檔
├── build.sh                 # 建置腳本
├── README.md               # 專案說明文件（本文件）
├── SETUP.md                # 首次設定指南 ⭐
├── DEPLOYMENT.md           # 部署指南
├── CONTRIBUTING.md         # 貢獻指南
├── SECURITY.md             # 安全性指南
├── SECURITY_NOTICE.md      # 安全公告
├── LICENSE                 # MIT 授權條款
├── .env.example           # 環境變數範本
├── .env                   # 環境變數（請勿上傳，已在 .gitignore）
├── .gitignore            # Git 忽略檔案清單
├── client_secrets.json   # Google OAuth 憑證（請勿上傳）
├── token.json           # Google OAuth Token（自動產生，請勿上傳）
├── Mainreptile/            # 爬蟲腳本資料夾
│   ├── schedule_scraper.py    # 課表爬蟲
│   ├── grade.py               # 成績爬蟲
│   ├── ranking_scraper.py     # 排名爬蟲
│   └── attendance_scraper.py  # 出缺勤爬蟲
├── templates/              # HTML 模板
│   └── home.html             # 首頁模板
├── data/                   # 使用者資料目錄（自動產生）
└── logs/                   # 日誌目錄（自動產生）
```

## 🔒 安全性與隱私

### 敏感檔案保護

以下檔案包含敏感資訊，已在 `.gitignore` 中排除：

- `.env` - 環境變數（帳號密碼）
- `client_secrets.json` - Google OAuth 憑證
- `token.json` - Google OAuth Token
- `data/` - 使用者資料
- `logs/` - 系統日誌

### 資料安全建議

1. ✅ 使用強密碼並定期更換
2. ✅ 不要將敏感檔案上傳至公開儲存庫
3. ✅ 定期檢查 Google Drive 的存取權限
4. ✅ 在公開網路環境使用時，考慮使用 VPN
5. ✅ 部署至雲端時，使用環境變數管理敏感資訊

## 🛠️ 開發指南

### 執行測試

```bash
# 測試單一爬蟲腳本
python Mainreptile/schedule_scraper.py
```

### 除錯模式

在本地開發時，可以在 `.env` 中設定 `HEADLESS=False`，這樣可以看到瀏覽器操作過程。

### 查看日誌

所有執行日誌都會儲存在 `data/{學號}/logs/` 目錄下：

- `{type}_{timestamp}.out.txt` - 標準輸出
- `{type}_{timestamp}.err.txt` - 錯誤輸出

## ❓ 常見問題

### Q1: 為什麼顯示「學號或密碼錯誤」？

- 請確認 `.env` 檔案中的 `SHU_USERNAME` 和 `SHU_PASSWORD` 是否正確
- 檢查您的帳號是否能正常登入校務系統網站

### Q2: 為什麼 Google Drive 上傳失敗？

- 檢查 `client_secrets.json` 是否存在且正確
- 刪除 `token.json` 後重新授權
- 確認 Google Drive API 已啟用

### Q3: Docker 容器無法啟動？

- 檢查環境變數是否都已設定
- 查看容器日誌：`docker logs imshu`
- 確認 Chrome/Chromium 已正確安裝在容器中

### Q4: 爬蟲執行逾時怎麼辦？

- 可以在 `.env` 中增加逾時時間，例如：`TIMEOUT_GRADES=600`
- 檢查網路連線是否穩定
- 確認校務系統是否正常運作

## 📝 更新日誌

### v1.0.0 (2024-10-16)

- ✨ 初始版本發布
- ✅ 支援課表、成績、排名、出缺勤查詢
- ✅ 整合 Google Drive 自動上傳
- ✅ 提供 Docker 與 Render 部署方案

## 🤝 貢獻指南

歡迎提交 Issue 或 Pull Request！

1. Fork 此專案
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權條款

本專案採用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。

## ⚠️ 免責聲明

本工具僅供個人學習與合法使用，請遵守世新大學相關規定。使用者應自行承擔使用本工具所產生的任何風險與責任。

## 📧 聯絡方式

如有任何問題或建議，歡迎透過以下方式聯絡：

- 提交 [GitHub Issue](https://github.com/Laiii151/IMSHU/issues)
- Email: （請在此填入您的聯絡 Email）

---

⭐ 如果這個專案對您有幫助，請給個星星支持！