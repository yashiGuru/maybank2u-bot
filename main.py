import time
import sys

from utils import attach_driver_go_page, run_transactions
from utils_login import get_screenshot_b64, exit_driver, exit_chrome, remove_cookie
from utils_api import api_send_alarm

from src.drivers.driver_setup import create_driver, start_chrome_home
from src.bot_monitoring.screen_checks import start_bot_with_dashboard_check
from src.utils.constant import BANK_URL, PORT, AGGREGATOR_SERVER, ACTION_WAIT, LIMIT_PAGES, BANK_NAME, BANK_CODE, USERNAME, ACCOUNT_NAME, ALARM_TYPE

def main():
    # 1) Launch Chrome via PyAutoGUI + subprocess
    ret, chrome = start_chrome_home(BANK_URL, PORT)
    if not (ret and chrome):
        print("❌ Failed to launch Chrome. Exiting.")
        sys.exit(1)

    # 2) Attach Selenium to the running Chrome session
    try:
        driver = create_driver(PORT)
        print("✅ Selenium driver attached successfully.")
    except Exception as e:
        print(f"❌ Could not attach Selenium driver: {e}")
        sys.exit(1)

    # 3) Wait for dashboard to load
    login_page_screenshot = driver.get_screenshot_as_base64()
    if login_page_screenshot:
        api_send_alarm(AGGREGATOR_SERVER, BANK_NAME, BANK_CODE, ALARM_TYPE.LOGIN_PAGE, login_page_screenshot)

    is_login = start_bot_with_dashboard_check(driver)
    if not is_login:
        login_not_filled_screenshot = get_screenshot_b64()
        if login_not_filled_screenshot:
            api_send_alarm(AGGREGATOR_SERVER, BANK_NAME, BANK_CODE, ALARM_TYPE.LOGIN_NOT_FILLED, login_not_filled_screenshot)
        print("❌ Dashboard never appeared. Exiting due to login failure.")
        print("Closing driver...")
        exit_driver(driver)

        print("Killing Chrome process...")
        exit_chrome(chrome)

        print("Removing cookies...")
        remove_cookie(PORT)
        sys.exit("Bot exited due to login failure.")

    login_success_screenshot = driver.get_screenshot_as_base64()
    if login_success_screenshot:
        api_send_alarm(AGGREGATOR_SERVER, BANK_NAME, BANK_CODE, ALARM_TYPE.LOGIN_SUCCESS, login_success_screenshot)

    # 4) Proceed with your transaction logic
    print("🚀 Login succeeded, starting transaction run...")
    try:
        attach_driver_go_page(ACCOUNT_NAME, PORT)
        run_transactions(
            driver,
            AGGREGATOR_SERVER,
            BANK_NAME, 
            BANK_CODE, 
            ACCOUNT_NAME, 
            USERNAME, 
            ACTION_WAIT,
            LIMIT_PAGES,
            PORT,
            chrome
        )
    except Exception as e:
        print(f"❌ Error during run_transactions: {e}")
        sys.exit(1)

    # 5) Clean exit (if run_transactions returns normally)
    print("✅ All done. Exiting cleanly.")
    driver.quit()
    chrome.kill()

if __name__ == "__main__":
    main()
