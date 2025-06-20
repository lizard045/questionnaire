@echo off
chcp 65001 >nul
echo ================================
echo 🔧 安裝問卷自動填寫程式依賴項目
echo ================================
echo.

echo 📦 正在安裝 Python 套件...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ 安裝完成！
    echo.
    echo 📋 請按照以下步驟設定：
    echo 1. 編輯 config.py 檔案
    echo 2. 設定您的學號和密碼
    echo 3. 執行 python run.py 開始使用
    echo.
) else (
    echo.
    echo ❌ 安裝失敗，請檢查 Python 環境
    echo.
)

pause 