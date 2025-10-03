# 1. 使用官方的 Python 3.10 作為基礎映像
FROM python:3.10-slim

# 2. 設定環境變數，避免產生 .pyc 檔案
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1

# 3. 安裝我們需要的系統套件 (C 編譯器等)
RUN apt-get update && \
    apt-get install -y build-essential python3-dev && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-noto-cjk \
        curl ca-certificates jq gosu gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver fonts-noto-cjk \
 && rm -rf /var/lib/apt/lists/*

# 4. 設定工作目錄
WORKDIR /app

# 5. 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製整個專案的程式碼到工作目錄
COPY . .
ENV HEADLESS=True \
    CHROME_BIN=/usr/bin/chromium \
    PORT=5000 \
    PYTHONIOENCODING=utf-8

# Render 會把 $PORT 傳進來，這裡用 gunicorn 綁定 0.0.0.0:$PORT
CMD ["sh", "-c", "gunicorn -w 2 -k gthread -t 180 -b 0.0.0.0:${PORT} app:app"]
# 7. 設定 Gunicorn 的啟動指令
# Render 會自動偵測 PORT 環境變數，我們用 10000 作為預設值


#CMD gunicorn --bind 0.0.0.0:5000 app:app 
