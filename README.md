# 🎓 世新大學自動化學籍資料爬蟲系統

此專案是一個整合式的 **Flask + Selenium 自動化系統**，可登入世新大學學生教務系統，並自動擷取下列個人資料：

- 📅 **個人課表**（SC0106）  
- 🧮 **歷年成績**（SD0101）  
- 🏆 **歷年名次**（SD0104）  
- 🚫 **缺勤記錄**（SC0108）

同時整合 **Google Drive API**，可將產出的資料自動上傳至指定雲端資料夾。

---

## 🧩 專案結構

```
.
├── app.py                      # Flask 主程式（整合後台與子爬蟲）
├── attendance_scraper.py       # 缺勤記錄爬蟲 (SC0108)
├── grade.py                    # 歷年成績爬蟲 (SD0101)
├── ranking_scraper.py          # 歷年名次爬蟲 (SD0104)
├── schedule_scraper.py         # 個人課表爬蟲 (SC0106)
├── requirements.txt            # 套件需求
├── client_secrets.json         # Google API 憑證 (需自行放置)
├── .env                        # 私密設定檔 (帳密、環境參數)
└── data/
    ├── logs/                   # 各模組的執行日誌
    ├── timetable_list1.csv     # 課表結果
    ├── grades_courses_fixed.csv
    ├── grades_summary_fixed.csv
    ├── ranking_records.csv
    └── attendance_records.csv
```

---

## ⚙️ 安裝環境

### 1️⃣ 安裝依賴
```bash
pip install -r requirements.txt
```

**主要套件：**
- selenium
- webdriver-manager
- flask
- pandas
- google-api-python-client
- google-auth-oauthlib
- python-dotenv

---

### 2️⃣ 設定 `.env` 檔案

```env
SHU_USERNAME=你的學號
SHU_PASSWORD=你的密碼
GDRIVE_FOLDER_ID=你的雲端資料夾ID (可選)
APP_SECRET=自訂flask密鑰
HEADLESS=True
```

---

### 3️⃣ 取得 Google Drive API 憑證

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)。  
2. 建立 OAuth 2.0 憑證。  
3. 下載為 `client_secrets.json` 放入專案根目錄。  
4. 第一次執行時會開啟瀏覽器要求授權，產生 `token.json`。

---

## 🚀 執行方式

### ✅ 直接執行 Flask 主程式
```bash
python app.py
```

---

### ✅ 單獨執行爬蟲腳本

```bash
python schedule_scraper.py
python grade.py
python ranking_scraper.py
python attendance_scraper.py
```

---

## 🧠 模組說明

### 🗓️ 課表爬蟲 (SC0106)
- 自動登入 → 點擊「課務作業」→「SC0106-學生課表查詢」
- 擷取《個人課表清單一》
- 匯出：`timetable_list1.csv / json / xlsx`

### 🧾 成績爬蟲 (SD0101)
- 登入 → 「成績作業」→「SD0101-歷年成績查詢」
- 處理跨學期課程
- 匯出：`grades_courses_fixed.csv / grades_summary_fixed.csv`

### 🏅 名次爬蟲 (SD0104)
- 登入 → 「成績作業」→「SD0104-歷年(學期)名次查詢」
- 修正名次格式防止 Excel 誤判
- 匯出：`ranking_records.csv`

### 🚷 缺勤記錄爬蟲 (SC0108)
- 登入 → 「課務作業」→「SC0108-出缺勤記錄查詢」
- 匯出：`attendance_records.csv`

---

## ☁️ Google Drive 自動上傳

- `authenticate()`：OAuth2 驗證  
- `find_or_create_folder()`：建立或查找學號資料夾  
- `upload_replace()`：自動覆蓋舊檔案

---

## 🧾 錯誤診斷

- 登入錯誤：自動截圖與 HTML 備份  
- 導覽錯誤：輸出除錯檔  
- 執行結果：紀錄於 `data/logs/*.out.txt`、`*.err.txt`  

---

## 🖥️ Headless 模式部署

```env
HEADLESS=True
CHROME_BIN=/usr/bin/google-chrome
```

伺服器建議安裝：
```bash
apt-get install -y chromium-driver google-chrome-stable
```

---

## 🧾 License

僅供學術與個人用途，不得用於商業目的。  
作者：黃珮婷（世新大學專題製作）  
技術：Flask + Selenium + Google Drive API
