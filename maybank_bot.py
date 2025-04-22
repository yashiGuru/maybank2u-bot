import utils_login
import utils_api
import utils
import os
import sys
import json
import time


application_path = utils_login.application_path

def init_setting():
    setting_file = "settings.json"
    settings = json.load(open(f"{application_path}/{setting_file}"))
    return settings

if __name__ == "__main__":
    settings = init_setting()
    url = settings['url']
    bank_name = settings['bank_name']
    bank_code = settings['bank_code']
    username = settings['username']
    password = settings['password']
    account_name = settings['account_name']
    aggregator_server = settings['aggregator_server']
    action_wait = settings['action_wait']
    limit_pages = settings['limit_pages']
    port = settings['port']

    login_count = 0

    utils_api.api_send_site_info(aggregator_server, bank_name, bank_code, username, password)

    while(1):       
        ret, chrome, login_btn_pos = utils_login.start_chrome_home(url, port) # uncomment Version 1
        if ret and utils_login.do_login(username, password, login_btn_pos) and utils_login.is_logined(1): # use always
            print(":login successed ----------------------")
            driver = utils.attach_driver_go_page(account_name, port)
            print(":1 attached chrome driver ----------------------")

            utils.run_transactions(driver, aggregator_server, bank_name, bank_code, account_name, username, action_wait, limit_pages, port, chrome)
            print(":2 attached chrome driver ----------------------")

            utils_login.exit_driver(driver)
            utils_login.exit_chrome(chrome)    
            time.sleep(2)
            utils_login.remove_cookie(port)        
            # utils_login.remove_cookie()  # uncomment in Version 2
            # break                          # uncomment in Version 1
        else:
            print("login failed ----------------------")
            img_b64 = utils_login.get_screenshot_b64()
            if img_b64:
                ret = utils_api.api_send_alarm(aggregator_server, bank_name, bank_code, 'login', img_b64)
            # utils_login.exit_driver(driver)
            utils_login.exit_chrome(chrome)
            utils_login.remove_cookie(port)
        
        print("---------------------------------------------------------")