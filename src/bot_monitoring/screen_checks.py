import time
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from src.drivers.driver_setup import create_driver
from src.utils.constant import MAX_WAIT_TIME_FOR_LOGIN, AGGREGATOR_SERVER, BANK_NAME, BANK_CODE, ALARM_TYPE
from utils_api import api_send_alarm

def is_dashboard_loaded(driver, timeout: int = 60):
    """
    Checks if the dashboard is loaded by looking for a unique <h2> tag text.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[text()='Get more from your money!']")
            )
        )
        print("✅ Dashboard loaded.")
        return True
    except Exception as e:
        print("⛔ Dashboard not loaded in time.")
        return False


MAX_WAIT_TIME = MAX_WAIT_TIME_FOR_LOGIN * 60
CHECK_INTERVAL = 5       # 5 seconds

def start_bot_with_dashboard_check(driver):
    try:
        print("🟡 Waiting for dashboard to load...")

        start_time = time.time()
        # now_time = time.time()
        # diff_time = now_time - start_time
        # print("diff_time", diff_time)
        # print("MAX_WAIT_TIME", MAX_WAIT_TIME)
        while time.time() - start_time < MAX_WAIT_TIME:
            if is_dashboard_loaded(driver, 1):
                print("✅ Dashboard loaded. Bot process started.")
                return True  # Dashboard successfully loaded
            check_invalid_login_and_alert(driver)
            time.sleep(CHECK_INTERVAL)

        print(f"❌ Dashboard not loaded within {MAX_WAIT_TIME_FOR_LOGIN} minutes.")
        return False  # Timed out

    except WebDriverException as e:
        print(f"💥 WebDriver error: {e}")
        return False

    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

def is_session_timeout_url(driver):
    """
    Checks if the current URL indicates a session timeout and sends an alarm if it does.
    """
    expected_url = "https://www.maybank2u.com.my/home/m2u/common/logout?sessionTimeout=true"
    current_url = driver.current_url.strip().lower()

    if current_url == expected_url.lower():
        print("⏳ Session timeout detected.")
        session_timeout_screenshot = driver.get_screenshot_as_base64()
        if session_timeout_screenshot:
            api_send_alarm(AGGREGATOR_SERVER, BANK_NAME, BANK_CODE, ALARM_TYPE.SESSION_TIMEOUT, session_timeout_screenshot)
            print("🚨 Alarm sent for session timeout.")
        return True
    return False

def check_invalid_login_and_alert(driver):
    """
    Checks if the invalid login message is displayed and sends an alarm if it is.
    """
    try:
        error_element = driver.find_element(By.XPATH,  "//span[contains(text(), 'Invalid username/password') or contains(text(), 'Invalid Username')]")
        if error_element:
            print("❌ Invalid login detected.")
            invalid_login_screenshot = driver.get_screenshot_as_base64()
            if invalid_login_screenshot:
                api_send_alarm(AGGREGATOR_SERVER, BANK_NAME, BANK_CODE, ALARM_TYPE.LOGIN_FAILURE, invalid_login_screenshot)
                print("🚨 Alarm sent for invalid login.")
                time.sleep(5)
    except NoSuchElementException:
        # Error message not found
        return False