# IMSHU 部署指南 (Deployment Guide)

本文件提供 IMSHU 專案的詳細部署說明，包含本地開發、Docker 容器化，以及雲端平台部署。

## 📋 目錄

- [本地開發環境](#本地開發環境)
- [Docker 部署](#docker-部署)
- [Render.com 部署](#rendercom-部署)
- [Heroku 部署](#heroku-部署)
- [其他雲端平台](#其他雲端平台)
- [生產環境建議](#生產環境建議)
- [常見問題排除](#常見問題排除)

## 🖥️ 本地開發環境

### Windows 系統

1. **安裝 Python**
   - 下載並安裝 [Python 3.10+](https://www.python.org/downloads/)
   - 安裝時勾選「Add Python to PATH」

2. **安裝 Git**
   - 下載並安裝 [Git for Windows](https://git-scm.com/download/win)

3. **Clone 專案**
```bash
git clone https://github.com/Laiii151/IMSHU.git
cd IMSHU
```

4. **建立虛擬環境**
```bash
python -m venv venv
venv\Scripts\activate
```

5. **安裝依賴**
```bash
pip install -r requirements.txt
```

6. **設定環境變數**
```bash
copy .env.example .env
# 使用記事本編輯 .env 檔案
notepad .env
```

7. **執行應用程式**
```bash
python app.py
```

### macOS 系統

1. **安裝 Homebrew**（如果尚未安裝）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **安裝 Python 和 Git**
```bash
brew install python@3.10 git
```

3. **Clone 專案**
```bash
git clone https://github.com/Laiii151/IMSHU.git
cd IMSHU
```

4. **建立虛擬環境**
```bash
python3 -m venv venv
source venv/bin/activate
```

5. **安裝依賴**
```bash
pip install -r requirements.txt
```

6. **設定環境變數**
```bash
cp .env.example .env
# 使用任何文字編輯器編輯 .env
nano .env  # 或使用 vim, code 等
```

7. **執行應用程式**
```bash
python app.py
```

### Linux 系統 (Ubuntu/Debian)

1. **更新套件列表**
```bash
sudo apt update
```

2. **安裝必要套件**
```bash
sudo apt install -y python3.10 python3.10-venv python3-pip git
```

3. **安裝 Chrome/Chromium**
```bash
sudo apt install -y chromium-browser chromium-chromedriver
```

4. **Clone 專案**
```bash
git clone https://github.com/Laiii151/IMSHU.git
cd IMSHU
```

5. **建立虛擬環境**
```bash
python3 -m venv venv
source venv/bin/activate
```

6. **安裝依賴**
```bash
pip install -r requirements.txt
```

7. **設定環境變數**
```bash
cp .env.example .env
nano .env  # 編輯環境變數
```

8. **執行應用程式**
```bash
python app.py
```

## 🐳 Docker 部署

### 建置與執行

1. **確認已安裝 Docker**
```bash
docker --version
```

2. **建置映像**
```bash
docker build -t imshu:latest .
```

3. **執行容器**
```bash
docker run -d \
  --name imshu \
  -p 5000:5000 \
  -e SHU_USERNAME=your_student_id \
  -e SHU_PASSWORD=your_password \
  -e APP_SECRET=your-secret-key \
  -e HEADLESS=True \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  imshu:latest
```

4. **查看日誌**
```bash
docker logs -f imshu
```

5. **停止容器**
```bash
docker stop imshu
```

6. **移除容器**
```bash
docker rm imshu
```

### Docker Compose

建立 `docker-compose.yml` 檔案：

```yaml
version: '3.8'

services:
  imshu:
    build: .
    container_name: imshu
    ports:
      - "5000:5000"
    environment:
      - SHU_USERNAME=${SHU_USERNAME}
      - SHU_PASSWORD=${SHU_PASSWORD}
      - APP_SECRET=${APP_SECRET}
      - HEADLESS=True
      - GDRIVE_FOLDER_ID=${GDRIVE_FOLDER_ID}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

執行：

```bash
# 啟動服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

## ☁️ Render.com 部署

### 準備工作

1. **註冊 Render 帳號**
   - 前往 [Render.com](https://render.com/)
   - 使用 GitHub 帳號註冊

2. **連結 GitHub 儲存庫**
   - 將您的 Fork 儲存庫推送到 GitHub
   - 在 Render 中授權存取 GitHub

### 部署步驟

1. **建立 Web Service**
   - 登入 Render Dashboard
   - 點擊「New +」→「Web Service」
   - 選擇 IMSHU 儲存庫

2. **設定服務**
   - **Name**: `imshu`
   - **Environment**: `Docker`
   - **Region**: 選擇最近的區域（如 Singapore）
   - **Branch**: `main`
   - **Plan**: Free（或選擇付費方案）

3. **設定環境變數**

   在「Environment」頁籤中新增：

   | Key | Value | 說明 |
   |-----|-------|------|
   | `SHU_USERNAME` | 您的學號 | 必填 |
   | `SHU_PASSWORD` | 您的密碼 | 必填 |
   | `APP_SECRET` | 隨機字串 | 必填 |
   | `HEADLESS` | `True` | 必填 |
   | `GDRIVE_FOLDER_ID` | 資料夾 ID | 選填 |
   | `PORT` | `5000` | 建議填寫 |

4. **部署**
   - 點擊「Create Web Service」
   - 等待自動建置和部署（約 5-10 分鐘）

5. **訪問應用程式**
   - 部署完成後，會提供一個網址（例如：`https://imshu.onrender.com`）
   - 點擊該網址即可訪問應用程式

### Render 注意事項

⚠️ **免費方案限制**：
- 服務閒置 15 分鐘後會自動休眠
- 休眠後首次訪問需要等待約 30 秒喚醒
- 每月有 750 小時免費執行時間

💡 **建議**：
- 使用付費方案以獲得更好的效能
- 定期訪問以保持服務活躍
- 使用 UptimeRobot 等服務定期 ping 您的應用程式

## 🚀 Heroku 部署

### 準備檔案

1. **建立 `Procfile`**

```
web: gunicorn -w 2 -k gthread -t 180 -b 0.0.0.0:$PORT app:app
```

2. **建立 `runtime.txt`**

```
python-3.10.12
```

3. **更新 `requirements.txt`**（確認包含）

```
gunicorn==22.0.0
```

### 部署步驟

1. **安裝 Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# 下載並安裝 Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
```

2. **登入 Heroku**
```bash
heroku login
```

3. **建立應用程式**
```bash
heroku create imshu-app-name
```

4. **設定 Buildpacks**
```bash
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-chromedriver
```

5. **設定環境變數**
```bash
heroku config:set SHU_USERNAME=your_student_id
heroku config:set SHU_PASSWORD=your_password
heroku config:set APP_SECRET=your-secret-key
heroku config:set HEADLESS=True
```

6. **部署**
```bash
git push heroku main
```

7. **開啟應用程式**
```bash
heroku open
```

8. **查看日誌**
```bash
heroku logs --tail
```

## 🌐 其他雲端平台

### Railway

1. 前往 [Railway.app](https://railway.app/)
2. 使用 GitHub 登入
3. 「New Project」→「Deploy from GitHub repo」
4. 選擇 IMSHU 儲存庫
5. 新增環境變數
6. 自動部署

### Fly.io

```bash
# 安裝 flyctl
curl -L https://fly.io/install.sh | sh

# 登入
flyctl auth login

# 初始化
flyctl launch

# 設定環境變數
flyctl secrets set SHU_USERNAME=your_id
flyctl secrets set SHU_PASSWORD=your_pwd
flyctl secrets set APP_SECRET=secret

# 部署
flyctl deploy
```

### Google Cloud Run

```bash
# 建置映像
gcloud builds submit --tag gcr.io/PROJECT-ID/imshu

# 部署
gcloud run deploy imshu \
  --image gcr.io/PROJECT-ID/imshu \
  --platform managed \
  --region asia-east1 \
  --set-env-vars SHU_USERNAME=your_id,SHU_PASSWORD=your_pwd
```

## 🔒 生產環境建議

### 安全性

1. **環境變數管理**
   - ✅ 使用平台的環境變數功能
   - ❌ 不要將敏感資訊寫入程式碼
   - ✅ 定期更換密碼和金鑰

2. **HTTPS**
   - ✅ 使用 HTTPS 加密傳輸
   - ✅ 大部分雲端平台會自動提供

3. **存取控制**
   - ✅ 設定 IP 白名單（如果平台支援）
   - ✅ 使用防火牆規則

### 效能優化

1. **資源配置**
   - CPU: 至少 1 vCPU
   - RAM: 至少 512MB（建議 1GB）
   - 儲存空間: 至少 1GB

2. **快取策略**
   - 使用 Redis 快取查詢結果
   - 設定適當的 session 過期時間

3. **監控與日誌**
   - 設定錯誤追蹤（如 Sentry）
   - 定期檢查日誌檔案
   - 設定效能監控（如 New Relic）

## ❓ 常見問題排除

### 問題 1: 部署後無法訪問

**可能原因**：
- PORT 環境變數設定錯誤
- 防火牆規則問題

**解決方法**：
```bash
# 檢查 PORT 設定
echo $PORT

# 確認應用程式監聽正確的 port
# 在 app.py 中應該使用 os.getenv("PORT", "5000")
```

### 問題 2: Selenium 無法啟動

**可能原因**：
- Chrome/Chromium 未安裝
- HEADLESS 設定錯誤

**解決方法**：
```bash
# 確認 HEADLESS=True
# 檢查 Chrome 是否已安裝
chromium --version
```

### 問題 3: Google Drive 上傳失敗

**可能原因**：
- OAuth 憑證未設定
- token.json 過期

**解決方法**：
- 在雲端環境中，需要使用 Service Account
- 或者在本地完成認證後，將 token.json 上傳

### 問題 4: 記憶體不足

**可能原因**：
- 免費方案資源限制
- Chrome 佔用太多記憶體

**解決方法**：
```python
# 在 Chrome options 中加入
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
```

### 問題 5: 請求逾時

**可能原因**：
- 網路延遲
- 校務系統回應慢

**解決方法**：
```bash
# 增加逾時時間
TIMEOUT_GRADES=600
```

## 📞 技術支援

如果遇到無法解決的問題：

1. 查看 [GitHub Issues](https://github.com/Laiii151/IMSHU/issues)
2. 搜尋相關錯誤訊息
3. 建立新 Issue 並提供：
   - 錯誤訊息
   - 環境資訊
   - 重現步驟

---

祝您部署順利！🎉
