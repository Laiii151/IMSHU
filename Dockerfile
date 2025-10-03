# 1) 基底映像
FROM python:3.10-slim

# 2) 基本環境
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3) 安裝系統依賴（一次完成）
#   - chromium / chromium-driver：Selenium 用
#   - 一些常見的 headless 依賴避免 Chrome 啟動時崩潰
RUN apt-get update && apt-get install -y --no-install-recommends \
      chromium \
      chromium-driver \
      fonts-noto-cjk \
      ca-certificates \
      libglib2.0-0 \
      libnss3 \
      libx11-6 \
      libxcomposite1 \
      libxrandr2 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxi6 \
      libxrender1 \
      libxss1 \
      libxtst6 \
      libgbm1 \
      libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 4) 工作目錄
WORKDIR /app

# 5) 安裝 Python 依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 6) 複製程式碼
COPY . .

# 7) 預設環境變數（仍建議在 Render 面板再設一次）
ENV HEADLESS=True \
    CHROME_BIN=/usr/bin/chromium \
    PORT=5000 \
    PYTHONIOENCODING=utf-8

# 8) 啟動（Render 會提供 $PORT）
CMD ["sh", "-c", "gunicorn -w 2 -k gthread -t 180 -b 0.0.0.0:${PORT} app:app"]
