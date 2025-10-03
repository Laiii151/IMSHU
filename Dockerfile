# 1. 使用官方的 Python 3.10 作為基礎映像
FROM python:3.10-slim

# 2. 設定環境變數，避免產生 .pyc 檔案
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV CHROME_BIN /usr/bin/chromium
# 確保所有爬蟲都以 Headless 模式運行
ENV HEADLESS True

# 3. 安裝我們需要的系統套件 (C 編譯器等)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    chromium \
    fontconfig \
    # 清理快取以減小映像檔大小
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# 4. 設定工作目錄
WORKDIR /app

# 5. 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir google-api-python-client

# 6. 複製整個專案的程式碼到工作目錄
COPY . .

# 7. 設定 Gunicorn 的啟動指令
# Render 會自動偵測 PORT 環境變數，我們用 10000 作為預設值
CMD gunicorn --bind 0.0.0.0:5000 app:app


