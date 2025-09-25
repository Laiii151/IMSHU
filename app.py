# -*- coding: utf-8 -*-
import os
import sys
import time
import glob
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('SHU_USERNAME')
PASSWORD = os.getenv('SHU_PASSWORD')

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET", "dev-secret")  # for flash()

# === 設定：請把路徑改成你電腦上實際的檔名 ===
# 建議把你的四個爬蟲檔擺一起（或改成絕對路徑）
SCRIPTS = {
    "timetable": "~\Mainreptile\schedule_scraper.py",  # 只抓清單一那支
    "grades":r"C:\IMSHU\Mainreptile\grade.py",          # 歷年成績那支（輸出 grades_courses_fixed.csv / grades_summary_fixed.csv）
    "ranking":r"C:\IMSHU\Mainreptile\ranking_scraper.py",         # 歷年名次那支（輸出 ranking_records.csv）
    "attendance":r"C:\IMSHU\Mainreptile\attendance_scraper.py",      # 出缺勤記錄那支（輸出 attendance_records.csv）
}

# 各腳本跑完後**預期**會產生的檔案（用來找最新一份）
OUTPUTS = {
    "timetable": [f"{USERNAME}_timetable_list1.csv"],
    "grades":    [f"{USERNAME}_grades_courses_fixed.csv", f"{USERNAME}_grades_summary_fixed.csv"],
    "ranking":   [f"{USERNAME}_ranking_records.csv"],
    "attendance":[f"{USERNAME}_attendance_records.csv"],
}

# CSV 顯示時的預設欄位（有就秀；沒有就自動顯示全部）
DEFAULT_COLUMNS = {
    "timetable": ["選別","課程簡碼","課程名稱(教材下載)","開課系級","學分","授課老師","星期節次週別","教室","備註"],
    "grades":    ["學年","選別","科目","上學期_學分","上學期_成績","下學期_學分","下學期_成績"],
    "ranking":   ["學年","學期","學分","平均","名次","人數"],
    "attendance":["學年","學期","課程代碼","課程名稱","教師","缺勤狀態","曠課次數","扣考時數","備註"],
}

# 在 Windows 通常用 "python"，在虛擬環境/其他系統用 sys.executable 比較穩
PYTHON_BIN = sys.executable or "python"


def run_script(kind: str, env_override: Dict[str, Any]) -> int:
    """
    呼叫對應的爬蟲腳本。回傳 process returncode。
    會把 SHU_USERNAME / SHU_PASSWORD / HEADLESS 等環境變數覆寫進去（不落地存檔）。
    """
    script = SCRIPTS.get(kind)
    if not script or not Path(script).exists():
        raise FileNotFoundError(f"找不到爬蟲腳本：{script}（請確認 SCRIPTS 設定與檔名）")

    env = os.environ.copy()
    env.update({k: str(v) for k, v in env_override.items() if v is not None})

    # 讓 selenium 在 server 上能跑
    if "HEADLESS" not in env:
        env["HEADLESS"] = os.getenv("HEADLESS", "True")

    # 執行
    print(f"[RUN] {PYTHON_BIN} {script}")
    proc = subprocess.run([PYTHON_BIN, script], env=env, capture_output=True, text=True)
    # 把標準輸出／錯誤留檔方便除錯
    ts = int(time.time())
    Path("logs").mkdir(exist_ok=True)
    (Path("logs")/f"{kind}_{ts}.out.txt").write_text(proc.stdout or "", encoding="utf-8")
    (Path("logs")/f"{kind}_{ts}.err.txt").write_text(proc.stderr or "", encoding="utf-8")
    print(f"[RET] code={proc.returncode}")
    return proc.returncode


def latest_existing(path_patterns):
    """
    回傳符合任一 pattern 的**最新**檔案路徑（找不到回傳 None）
    """
    candidates = []
    for pat in path_patterns:
        candidates.extend(glob.glob(pat))
    if not candidates:
        return None
    candidates.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)
    return candidates[0]


def load_csv_safely(path: str) -> pd.DataFrame:
    """
    嘗試用 UTF-8-SIG 讀，失敗就用 UTF-8。
    """
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path, encoding="utf-8")


def filter_df(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    針對所有欄位做簡單關鍵字包含過濾（不分大小寫）。
    """
    if not keyword:
        return df
    kw = str(keyword).strip().lower()
    mask = pd.Series([False]*len(df))
    for col in df.columns:
        mask = mask | df[col].astype(str).str.lower().str.contains(kw, na=False)
    return df[mask]


@app.route("/", methods=["GET"])
def index():
    """
    GET請求：單純顯示頁面。
    - 會嘗試載入最新的CSV，如果找不到就顯示一個空表格。
    """
    kind = request.args.get("kind", "timetable")
    keyword = request.args.get("keyword", "")
    outputs = OUTPUTS.get(kind, [])

    df = pd.DataFrame() # 預設建立一個空的 DataFrame
    csv_path = latest_existing(outputs)

    if csv_path: # 只有在找到 CSV 檔案時才讀取
        df = load_csv_safely(csv_path)

    if not df.empty: # 如果 DataFrame 不是空的，才進行篩選
        df = filter_df(df, keyword)
        pref = DEFAULT_COLUMNS.get(kind, [])
        cols = [c for c in pref if c in df.columns]
        view_df = df[cols] if cols else df
    else:
        view_df = df # 維持空的 DataFrame

    return render_template(
        "home.html",
        result_table=view_df.to_html(classes="table table-striped", index=False),
        kind=kind,
        keyword=keyword,
        download_link=os.path.basename(csv_path) if csv_path else None
    )


@app.route("/query", methods=["POST"])
def query():
    kind = request.form.get("kind")  # timetable / grades / ranking / attendance
    keyword = request.form.get("keyword", "").strip()
    do_scrape = request.form.get("do_scrape") == "on"

    # 可選：讓使用者臨時覆寫帳密（不會寫到 .env）
    user = request.form.get("username") or os.getenv("SHU_USERNAME")
    pwd  = request.form.get("password") or os.getenv("SHU_PASSWORD")

    if not kind:
        flash("請選擇要查詢的類型")
        return redirect(url_for("index"))

    if do_scrape:
        if not user or not pwd:
            flash("需要 SHU_USERNAME / SHU_PASSWORD 才能執行爬蟲")
            return redirect(url_for("index"))

        rc = run_script(kind, {"SHU_USERNAME": user, "SHU_PASSWORD": pwd})
        if rc != 0:
            flash("爬蟲執行失敗，請到 logs/ 夾查看 out/err 記錄")
            return redirect(url_for("index"))

    # 決定要讀哪個 CSV
    outputs = OUTPUTS.get(kind, [])
    if not outputs:
        flash("沒有設定輸出的檔名，請檢查 app.py 的 OUTPUTS 設定")
        return redirect(url_for("index"))

    # 歷年成績有兩份 CSV：課程與彙總，優先顯示課程
    csv_path = latest_existing(outputs)
    if not csv_path:
        flash("找不到對應的輸出 CSV，請先執行一次爬蟲或確認檔名")
        return redirect(url_for("index"))

    df = load_csv_safely(csv_path)
    df = filter_df(df, keyword)

    # 只挑常用欄位（有的話），避免表格太寬
    pref = DEFAULT_COLUMNS.get(kind, [])
    cols = [c for c in pref if c in df.columns]
    view_df = df[cols] if cols else df

    # 把目前顯示的 CSV 檔名也帶回前端（給下載）
    return render_template(
        "home.html",
        result_table=view_df.to_html(index=False, classes="table table-striped table-hover"),
        csv_path=csv_path,
        kind=kind,
        keyword=keyword
    )


@app.route("/download")
def download():
    path = request.args.get("path")
    if not path or not Path(path).exists():
        flash("檔案不存在")
        return redirect(url_for("index"))
    # 直接傳檔讓使用者下載
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    # python app.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)






