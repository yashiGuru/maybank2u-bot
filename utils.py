from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from random import random, randint
import re
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os
import logging
import utils_click

os.environ['WDM_LOG'] = str(logging.NOTSET)
os.environ['WDM_PROGRESS_BAR'] = str(0)

import utils_api

def attach_driver_go_page(account_name, port):
    # account_name = "CCA SME FIRST"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(options=options)
    print('attached chrome driver')
    time.sleep(5+random())

    # account_card_item = driver.find_element(By.CSS_SELECTOR, "span[class*='Card---accountName---']")
    driver.find_element(By.XPATH, f"//span[text()='{account_name}']").click()
    time.sleep(5+2*random())
    return driver

def go_next_page(driver):
    print("ACTION: Clicking Next")
    driver.execute_script("window.scrollTo(0, 768 + parseInt(256*Math.random() - 128))")
    time.sleep(1 + random())
    driver.find_element(By.CSS_SELECTOR, "a[class*='SavingAccountContainer---next_arrow']").click()
    time.sleep(3 + 2*random())

def check_session_modal(driver):
    ret = True
    try:
        modal = driver.find_element(By.CSS_SELECTOR, "div[class*='SessionModal---container---']")
        btn = modal.find_element(By.CSS_SELECTOR, "button.btn-success")
        time.sleep(2*random())
        btn.click()
    except:
        ret = False
    return ret

def check_logout_page(driver):
    ret = True
    try:
        modal = driver.find_element(By.CSS_SELECTOR, "div[class*='ZeroActivities---prompt---']")
    except:
        ret = False    
    return ret

def check_login_page(driver):
    ret = True
    try:
        modal = driver.find_element(By.CSS_SELECTOR, "div[class*='LoginUsername---loginWrapper---']")
    except:
        ret = False    
    return ret

def refresh_transactions(driver, account_name):
    print(f"ACTION: Refreshing Transactions")
    # time.sleep(2 + random()*2)
    # driver.find_element(By.XPATH, "//button[@id='transactionType']").click()
    # time.sleep(2 + random()*2)
    # driver.find_element(By.LINK_TEXT, "All Transaction History").click()

    ret = True
    try:
        driver.find_element(By.CSS_SELECTOR, "div[class*='Navigation---selected---']").click()
        time.sleep(5 + random()*2)
    except:
        ret = False
    
    try:
        driver.find_element(By.XPATH, f"//span[text()='{account_name}']").click()
        time.sleep(5 + random()*2)        
    except:
        ret = False

    return ret

def get_current_balance(driver):
    print(f"ACTION: Get Current Balance")
    balance_soup = BeautifulSoup(driver.page_source, features="html.parser")
    available_balance_element = balance_soup.select_one('p[class*="AvailableBalanceCard---balance"]')
    current_balance_element = balance_soup.select_one('div[class*="AccountDetailsCard---row"]').find("div")

    available_balance = available_balance_element.get_text(strip=True).replace("RM", "").replace(",", "")
    current_balance = current_balance_element.get_text(strip=True).strip().replace("RM", "").replace(",", "")
    print("available_balance", available_balance)        
    print("current_balance", current_balance)        
    return available_balance, current_balance

def parse_transaction(driver):
    print(f"ACTION: Parse transaction table")
    def remove_excess_whitespace(x):
        x = x.replace("\t", " ")
        x = x.replace("'", "")
        x = re.sub(' +', ' ', x)
        return x

    soup = BeautifulSoup(driver.page_source, features="lxml")
    table_data = []
    table_data_html = []
    try:
        table_data_html = soup.find_all("table")[0].find_all("tr")[1:]
        for element in table_data_html:
            sub_data = []
            for sub_element in element:
                try:
                    element_text = sub_element.get_text().strip()
                    if "negativeAmount" in str(sub_element):
                        element_text = "-" + element_text
                    if "SavingAccountContainer---amounts" in str(sub_element):
                        element_text = element_text.replace("RM", "")

                    sub_data.append(element_text)
                except:
                    continue
            
            dt = datetime.strptime(sub_data[0], '%d %b %Y').strftime("%Y-%m-%d")
            detail = remove_excess_whitespace(sub_data[1])
            amount = float(sub_data[3].replace(",", ""))
            sub_data = [dt, detail, amount]
            table_data.append(sub_data)        
    except:
        print(f"Erorr while get table data")
        table_data = None
        pass

    return table_data

def click_check_recaptcha_resume(driver):
    try:
        # Switch to the reCAPTCHA iframe
        recaptcha_iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
        driver.switch_thttpo.frame(recaptcha_iframe)

        # Locate the checkbox and click it
        recaptcha_checkbox = driver.find_element(By.ID, "recaptcha-anchor")
        recaptcha_checkbox.click()

        # Switch back to the main content
        driver.switch_to.default_content()
    except:
        pass

def check_captcha_modal(driver):
    modal = None
    try:
        modal = driver.find_element(By.CSS_SELECTOR, "div[class*='HeartBeatModal---wrapperCaptch---']")
    except:
        modal = None
    
    return modal

def check_captcha_and_alarm(driver, aggregator_server, bank_name, bank_code):
    ret = False
    modal =  check_captcha_modal(driver)
    if modal is not None:

        # with open('page_source.html', 'w', encoding='utf-8') as file:
        #     file.write(driver.page_source)

        print(f"ACTION: Found Captcha Modal, so exit the bot")
        img_b64 = driver.get_screenshot_as_base64()
        if img_b64:
            utils_api.api_send_alarm(aggregator_server, bank_name, bank_code, 'captcha', img_b64)
        ret = True

        # click_check_recaptcha_resume(driver)

    return ret

'''
-1: not find
0:  find and there is no update
>0: find there is update
'''
def match_transaction(data, init_data):
    def make_sequence(ddd):
        sequence = []
        for d in ddd:
            bal = float(str(d[2]))
            trace = "{}:{}:{}".format(d[0], d[1], bal)
            sequence.append(trace)
        return sequence
    
    data_seq = make_sequence(data)
    init_seq = make_sequence(init_data)
    position = -1
    for i in range(len(data_seq)):
        if data_seq[i:i + len(init_seq)] == init_seq:
            position = i
            break
    return position

def calc_amount(data):
    total_amount = 0
    for d in data:
        total_amount += float(d[2])
    return total_amount

def logout(driver):
    print(f"ACTION: Log Out")
    driver.find_element(By.CSS_SELECTOR, "div[class*='SideBar---logout_icon_wrapper']").click()
    time.sleep(1 + random()*2)

# Main Process
def run_transactions(driver, aggregator_server, bank_name, bank_code, account_name, username, action_wait=20, limit_pages=10):
    start_data = []
    start_data = utils_api.api_get_init_transactions(aggregator_server, bank_name, bank_code)
    if len(start_data) == 0:            
        clicked_row_index, balance = utils_click.get_init_data(driver)
        if clicked_row_index is None:
            return
        new_data = parse_transaction(driver)
    
        if int(clicked_row_index) + 5 <= len(new_data):
            start_data = new_data[clicked_row_index:clicked_row_index+5]
            real_index = 0
        else:
            start_data = new_data[-5:]
            # real_index = int(clicked_row_index) - 5
            real_index = 5 - (len(new_data) - int(clicked_row_index))
        
        init_data = []
        balance = balance.replace(",", "")
        balance = float(balance)
        for i, r in enumerate(start_data):
            dt, description, amount = r
            is_publish = 1
            if i < real_index:
                balance += float(amount)
                is_publish = 0
            init_data.append([dt, description, amount, is_publish])

        ret = utils_api.api_set_init_transactions(aggregator_server, bank_name, bank_code, username, init_data, balance)
        refresh_transactions(driver, account_name)
    
    table_data = []
    pages = 0
    BAL = 0
    st = time.time()
    while True:
            # if time.time() - st > 15 * 60:
            #     print(f"ACTION: Log In time is exceed 15 mins, so logout")
            #     logout()
            #     break
        try:
            if check_captcha_and_alarm(driver, aggregator_server, bank_name, bank_code):
                time.sleep(3 + random())
                break
                # break # uncomment in Version 1

            if pages >= limit_pages:
                print(f"there is no match data till {limit_pages} pages")
                break             

            if check_logout_page(driver) or check_login_page(driver):
                print(f"ACTION: Site is logged out, so exit the bot")
                img_b64 = driver.get_screenshot_as_base64()
                if img_b64:
                    utils_api.api_send_alarm(aggregator_server, bank_name, bank_code, 'logout', img_b64)                
                break
            
            # unconmment in version 1
            # if check_captcha_modal(driver):
            #     print(f"ACTION: Found Captcha Modal, so exit the bot")
            #     img_b64 = driver.get_screenshot_as_base64()
            #     utils_api.api_send_alarm(aggregator_server, bank_name, bank_code, 'captcha', img_b64)
            #     time.sleep(5 + random())
            #     continue

            new_data = parse_transaction(driver)
            if new_data is None: # Get Error while parsing table
                refresh_transactions(driver, account_name)
                table_data = []
                pages = 0
                time.sleep(random() * 2)
                continue

            table_data += new_data
            offset = match_transaction(table_data, start_data)
            
            if offset > 0: # match found, there is updated transaction               
                data = table_data[:offset]
                total = calc_amount(data)
                available_balance, current_balance = get_current_balance(driver)
                if total > 0 and float(available_balance) == BAL:
                    pass
                else:                
                    ret = utils_api.api_send_transactions(aggregator_server, bank_name, bank_code, username, data, available_balance, current_balance)
                    if not ret:
                        print("Server Side not works, so bot will be killed...")
                        break
                    
                    start_data = table_data[:5]                
                    BAL = float(available_balance)
                
                action_sec = randint(10, int(action_wait))
                print("Sent data, so waiting", action_sec, " seconds...")
                sec = 0
                while sec < action_sec:
                    if check_captcha_and_alarm(driver, aggregator_server, bank_name, bank_code):
                        break
                    time.sleep(1)
                    sec += 1
                if sec >= action_sec:
                    refresh_transactions(driver, account_name)
                    table_data = []
                    pages = 0

            elif offset == 0: # match found, but there is no updated transaction
                action_sec = randint(10, int(action_wait))
                print("NO updated the transactions, so waiting", action_sec, " seconds...")
                sec = 0
                while sec < action_sec:
                    if check_captcha_and_alarm(driver, aggregator_server, bank_name, bank_code):
                        break
                    time.sleep(1)
                    sec += 1
                if sec >= action_sec:
                    refresh_transactions(driver, account_name)
                    table_data = []
                    pages = 0

            else: # offset < 0, match not found.
                go_next_page(driver)
                pages += 1

        except Exception as error:
            print("Error occured: ", error)
            img_b64 = driver.get_screenshot_as_base64()
            if img_b64:
                utils_api.api_send_alarm(aggregator_server, bank_name, bank_code, 'error', img_b64)

            refresh_transactions(driver, account_name)
            table_data = []
            pages = 0
            time.sleep(2)

def send_login_alert(driver, aggregator_server, bank_name, bank_code, username):
    ret = False
    try:
        img_b64 = driver.get_screenshot_as_base64()
        if img_b64:
            utils_api.api_send_alarm(aggregator_server, bank_name, bank_code, username, 'alert', img_b64)            
        ret = True
        time.sleep(1 + random()*2)
    except:
        ret = False            