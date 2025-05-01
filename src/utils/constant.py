import os
import sys
import json

# Determine if running as a PyInstaller .exe
if getattr(sys, 'frozen', False):
    # Running in a bundle
    BASE_DIR = sys._MEIPASS
    SETTINGS_PATH = os.path.join(os.path.dirname(sys.executable), 'settings.json')
else:
    # Running in normal Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SETTINGS_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'settings.json'))

def get_settings():
    with open(SETTINGS_PATH, 'r') as f:
        return json.load(f)

settings = get_settings()
# Assign variables
AGGREGATOR_SERVER = settings['aggregator_server']
PORT = settings['port']
DEBUG = settings['debug']
ACTION_WAIT = settings['action_wait']
LIMIT_PAGES = settings['limit_pages']
MAX_WAIT_TIME_FOR_LOGIN = 10  # 10 minutes

BANK_URL = settings['url']

BANK_NAME = settings['bank_name']
BANK_CODE = settings['bank_code']
USERNAME = settings['username']
PASSWORD = settings['password']
ACCOUNT_NAME = settings['account_name']

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGOUT_BLACK_IMG   = os.path.join(ASSETS_DIR, "im_logout_black.png")
ACCOUNT_TOOL_IMG   = os.path.join(ASSETS_DIR, "im_account_tool.png")
CAPTCHA_IMG        = os.path.join(ASSETS_DIR, "im_captcha.png")

class ALARM_TYPE:
    LOGIN_FAILURE = "login"
    LOGIN_PAGE = "login_page"
    LOGIN_NOT_FILLED = "login_not_filled"
    LOGIN_SUCCESS = "login_success"
    LOGOUT = 'logout'
    CAPTCHA = 'captcha'
    CAPTCHA_SOLVED = "captcha_solved"
    CAPTCHA_FAILED = "captcha_failed"
    CAPTCHA_NOT_FILLED = "captcha_not_filled"
    SESSION_TIMEOUT = "session_timeout"