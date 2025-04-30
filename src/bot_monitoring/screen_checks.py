import time
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from src.drivers.driver_setup import create_driver

from src.utils.constant import MAX_WAIT_TIME_FOR_LOGIN

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
            time.sleep(CHECK_INTERVAL)

        print(f"❌ Dashboard not loaded within {MAX_WAIT_TIME_FOR_LOGIN} minutes.")
        return False  # Timed out

    except WebDriverException as e:
        print(f"💥 WebDriver error: {e}")
        return False

    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

def is_session_timeout_url(url: str) -> bool:
    """
    Checks if the provided URL is the Maybank2u session timeout logout URL.
    """
    expected_url = "https://www.maybank2u.com.my/home/m2u/common/logout?sessionTimeout=true"
    return url.strip().lower() == expected_url.lower()