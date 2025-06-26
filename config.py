# 配置檔案
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 登入資訊
STUDENT_ID = "C111110118"  # 您的學號
PASSWORD   = "C111110118"      # 您的密碼

# 網站設定
LOGIN_URL = "https://ceq.nkust.edu.tw/Home"

# 瀏覽器設定
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'True').lower() == 'true'  # 預設啟用 headless
WAIT_TIME = int(os.getenv('WAIT_TIME', '2'))  # 縮短等待時間從3秒到2秒

# 🚀 優化模式設定
ULTRA_SPEED_MODE = True  # 啟用超高速模式
DISABLE_IMAGES = True    # 禁用圖片載入
DISABLE_CSS = False      # 保留CSS確保元素可見
FAST_LOGIN_MODE = True   # 啟用快速登入模式
DIRECT_NAVIGATION = True # 啟用直接導航模式

# 隨機作答設定
RANDOM_ANSWER_PROBABILITY = 0.8  # 80% 機率選擇隨機答案
DEFAULT_RATING = 4  # 預設評分 (1-5分)

# 可能的評分答案
RATING_OPTIONS = [3, 4, 5]  # 偏向正面評價
TEXT_ANSWERS = [
    "好",  # 最短正面回應
    "課程內容豐富，受益良多",
    "教學方式生動有趣",
    ""  # 空白回答
]

# 🚀 超高速模式專用設定
ULTRA_SPEED_CONFIG = {
    'implicit_wait': 2,        # 隱式等待時間 (從10秒降到2秒)
    'page_load_timeout': 15,   # 頁面載入超時 (從30秒降到15秒)
    'script_timeout': 10,      # 腳本執行超時 (從30秒降到10秒)
    'login_wait': 2,           # 登入等待時間 (從5秒降到2秒)
    'navigation_wait': 1,      # 導航等待時間 (從3秒降到1秒)
    'submit_wait': 1,          # 提交等待時間 (從3秒降到1秒)
    'question_delay': 0.1      # 問題間延遲 (從0.3秒降到0.1秒)
} 