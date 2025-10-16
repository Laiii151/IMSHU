# 安全性指南 (Security Guide)

本文件說明 IMSHU 專案的安全性考量與最佳實踐。

## 🔒 重要安全提醒

### ⚠️ 敏感檔案保護

以下檔案包含敏感資訊，**絕對不可**上傳到公開儲存庫：

1. **`.env`** - 包含帳號密碼
2. **`client_secrets.json`** - Google OAuth 憑證
3. **`token.json`** - Google OAuth 存取 Token
4. **`data/`** - 使用者個人資料
5. **`logs/`** - 可能包含敏感資訊的日誌

這些檔案已在 `.gitignore` 中排除，但請務必確認。

### 檢查是否已意外上傳敏感檔案

```bash
# 檢查 Git 追蹤的檔案
git ls-files

# 如果發現敏感檔案已被追蹤
git rm --cached 檔案名稱
git commit -m "Remove sensitive file"
git push
```

⚠️ **重要**：如果敏感資訊已經被推送到 GitHub：
1. 立即更改所有密碼
2. 撤銷 Google OAuth 憑證並重新建立
3. 考慮使用 `git filter-branch` 或 BFG Repo-Cleaner 清除歷史記錄

## 🔐 密碼與金鑰管理

### 強密碼建議

- 長度至少 12 個字元
- 包含大小寫字母、數字和特殊符號
- 不要使用生日、姓名等個人資訊
- 定期更換（建議每 3-6 個月）

### APP_SECRET 金鑰生成

在 Python 中生成隨機金鑰：

```python
import secrets
print(secrets.token_hex(32))
```

或使用 OpenSSL：

```bash
openssl rand -hex 32
```

### 環境變數最佳實踐

1. **本地開發**
   - 使用 `.env` 檔案
   - 不要提交 `.env` 到 Git

2. **生產環境**
   - 使用平台的環境變數功能
   - Render: Environment Variables
   - Heroku: Config Vars
   - Docker: `-e` 參數或 Docker Secrets

3. **團隊協作**
   - 使用 `.env.example` 作為範本
   - 在文件中說明需要哪些環境變數
   - 不要在聊天工具中傳送密碼

## 🌐 網路安全

### HTTPS 加密

- ✅ 生產環境必須使用 HTTPS
- ✅ 大部分雲端平台自動提供 SSL/TLS
- ❌ 不要在 HTTP 環境下輸入敏感資訊

### CORS (跨來源資源共享)

如果需要限制存取來源，在 `app.py` 中加入：

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://yourdomain.com"])
```

### Rate Limiting

為了防止濫用，建議加入請求限制：

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 🛡️ Google Drive API 安全

### OAuth 2.0 最佳實踐

1. **權限最小化**
   - 目前使用 `drive.file` 範圍（只能存取程式建立的檔案）
   - 不要使用 `drive` 範圍（會存取所有檔案）

2. **憑證保護**
   ```bash
   # 設定檔案權限（Linux/macOS）
   chmod 600 client_secrets.json
   chmod 600 token.json
   ```

3. **定期審查**
   - 前往 [Google Account Security](https://myaccount.google.com/permissions)
   - 檢查並撤銷不需要的應用程式存取權限

### Service Account（進階）

對於伺服器環境，建議使用 Service Account：

1. 在 Google Cloud Console 建立 Service Account
2. 下載金鑰檔案（JSON）
3. 使用 Service Account 認證：

```python
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'service-account-key.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)
```

## 🔍 程式碼安全

### 輸入驗證

```python
# 驗證學號格式
import re

def validate_student_id(student_id):
    # 假設學號為 9 位數字
    if not re.match(r'^\d{9}$', student_id):
        raise ValueError("Invalid student ID format")
    return student_id
```

### SQL Injection 防護

本專案不直接使用 SQL，但如果未來需要資料庫：

```python
# ✅ 正確：使用參數化查詢
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ❌ 錯誤：字串拼接
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### XSS 防護

Flask 的 Jinja2 模板引擎預設會自動轉義 HTML，但要注意：

```html
<!-- ✅ 安全：自動轉義 -->
{{ user_input }}

<!-- ❌ 危險：不轉義 -->
{{ user_input | safe }}
```

### 日誌安全

不要在日誌中記錄敏感資訊：

```python
# ❌ 錯誤
logger.info(f"Login attempt: {username} {password}")

# ✅ 正確
logger.info(f"Login attempt: {username}")
```

## 🚨 錯誤處理

### 不要洩露詳細錯誤訊息

```python
# ❌ 錯誤：洩露內部資訊
@app.errorhandler(500)
def server_error(e):
    return str(e), 500

# ✅ 正確：回傳一般性訊息
@app.errorhandler(500)
def server_error(e):
    logger.error(f"Internal error: {e}")
    return "Internal Server Error", 500
```

### 設定適當的錯誤頁面

```python
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
```

## 🔄 定期安全維護

### 1. 更新依賴套件

```bash
# 檢查過期套件
pip list --outdated

# 更新套件
pip install --upgrade package_name

# 更新 requirements.txt
pip freeze > requirements.txt
```

### 2. 檢查安全漏洞

使用 `safety` 檢查已知漏洞：

```bash
pip install safety
safety check
```

使用 `bandit` 檢查程式碼安全問題：

```bash
pip install bandit
bandit -r .
```

### 3. 定期審查日誌

```bash
# 檢查異常登入嘗試
grep -i "failed\|error" logs/*.log

# 檢查資源使用情況
grep -i "timeout\|memory" logs/*.log
```

### 4. 備份重要資料

```bash
# 定期備份資料
tar -czf backup-$(date +%Y%m%d).tar.gz data/ logs/

# 或使用 rsync 同步到遠端
rsync -avz data/ user@backup-server:/backup/imshu/
```

## 👥 多使用者環境

如果計劃讓多人使用：

### 1. 實作使用者認證

```python
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

### 2. 資料隔離

```python
# 確保每個使用者只能存取自己的資料
user_data_dir = DATA_ROOT / current_user.username
if not user_data_dir.exists():
    user_data_dir.mkdir(parents=True)
```

### 3. Session 安全

```python
from datetime import timedelta

app.config.update(
    SESSION_COOKIE_SECURE=True,  # 只在 HTTPS 下傳送
    SESSION_COOKIE_HTTPONLY=True,  # 防止 JavaScript 存取
    SESSION_COOKIE_SAMESITE='Lax',  # CSRF 防護
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)  # Session 過期時間
)
```

## 📋 安全檢查清單

部署前請確認：

- [ ] `.env` 已加入 `.gitignore`
- [ ] `client_secrets.json` 已加入 `.gitignore`
- [ ] `token.json` 已加入 `.gitignore`
- [ ] 使用強密碼
- [ ] APP_SECRET 使用隨機金鑰
- [ ] 生產環境使用 HTTPS
- [ ] 設定適當的環境變數
- [ ] 日誌不包含敏感資訊
- [ ] 錯誤訊息不洩露內部資訊
- [ ] 依賴套件為最新版本
- [ ] 已執行安全掃描工具
- [ ] 設定適當的檔案權限
- [ ] 定期備份重要資料

## 🆘 安全事件回應

如果發現安全問題：

1. **立即行動**
   - 更改所有相關密碼
   - 撤銷可能洩露的 API 金鑰
   - 停止受影響的服務

2. **評估影響**
   - 哪些資料可能被存取
   - 有多少使用者受影響
   - 問題持續多久

3. **修復問題**
   - 更新程式碼
   - 加強安全措施
   - 重新部署

4. **通知相關人員**
   - 如果有其他使用者，通知他們
   - 在 GitHub 上發布安全公告（如果適用）

5. **記錄與學習**
   - 記錄事件經過
   - 分析根本原因
   - 更新安全政策

## 📞 回報安全漏洞

如果您發現安全漏洞，請：

1. **不要**公開揭露
2. 透過 Email 聯繫維護者（私下通知）
3. 提供詳細資訊：
   - 漏洞描述
   - 重現步驟
   - 潛在影響
   - 建議修復方式（如果有）

我們會盡快回應並修復問題。

---

安全是持續的過程，不是一次性的任務。請定期審查並更新安全措施！🔒
