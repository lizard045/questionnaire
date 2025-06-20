@echo off
chcp 65001 > nul
title NKUST 問卷自動填寫系統

echo.
echo ================================================
echo          NKUST 問卷自動填寫系統
echo ================================================
echo.
echo 🎯 正在啟動問卷自動填寫程式...
echo 📋 請確保已安裝 Python 和相關套件
echo 🔧 如需安裝套件，請先執行 install_requirements.bat
echo.

REM 檢查 Python 是否存在
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: 找不到 Python，請先安裝 Python 3.7 或更新版本
    echo 📥 下載地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 檢查程式檔案是否存在
if not exist "auto_questionnaire.py" (
    echo ❌ 錯誤: 找不到 auto_questionnaire.py 檔案
    echo 請確認檔案位於正確位置
    pause
    exit /b 1
)

REM 檢查設定檔是否存在
if not exist "config.py" (
    echo ❌ 錯誤: 找不到 config.py 設定檔
    echo 請確認設定檔存在並已正確配置學號密碼
    pause
    exit /b 1
)

echo ✅ 環境檢查通過，開始執行程式...
echo.

REM 執行主程式
python auto_questionnaire.py

echo.
echo ================================================
echo 程式執行完畢
echo ================================================
echo.
echo ✅ 問卷填寫任務已完成
echo 📋 請到問卷系統確認填寫狀態
echo.
echo 按任意鍵關閉視窗...
pause > nul 