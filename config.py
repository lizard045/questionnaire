# 配置檔案
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 登入資訊
STUDENT_ID = ""  # 您的學號
PASSWORD = ""      # 您的密碼

# 網站設定
LOGIN_URL = "https://ceq.nkust.edu.tw/Home"

# 瀏覽器設定
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'
WAIT_TIME = int(os.getenv('WAIT_TIME', '3'))

# 隨機作答設定
RANDOM_ANSWER_PROBABILITY = 0.8  # 80% 機率選擇隨機答案
DEFAULT_RATING = 4  # 預設評分 (1-5分)

# 可能的評分答案
RATING_OPTIONS = [3, 4, 5]  # 偏向正面評價
TEXT_ANSWERS = [
    "課程內容豐富，受益良多",
    "老師教學認真，講解清楚",
    "課程安排適當，學習效果良好",
    "教學方式生動有趣",
    "課程對學習很有幫助",
    "整體而言是很好的課程",
    ""  # 空白回答
] 