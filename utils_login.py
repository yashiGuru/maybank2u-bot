import subprocess
import time
import pyautogui
pyautogui.FAILSAFE = False
import os
import sys
import stat
import base64
import shutil
from io import BytesIO
from random import random, randint

application_path = os.path.dirname(sys.executable)
if "python.exe" in sys.executable:
    application_path = "."
print("application path:", application_path)

login_yellow_path   = os.path.join(application_path, 'im_login_yellow.png')
ok_green_path       = os.path.join(application_path, 'im_ok_green.png')
login_green_path    = os.path.join(application_path, 'im_login_green.png')
logout_black_path   = os.path.join(application_path, 'im_logout_black.png')
view_white_path     = os.path.join(application_path, 'im_view_white.png')
account_tool_path   = os.path.join(application_path, 'im_account_tool.png')
captcha_path        = os.path.join(application_path, 'im_captcha.png')
action_wait = 5

def start_chrome_home(url, port):
    print(f"ACTION: Open Chrome and go to home page")
    chrome = subprocess.Popen([
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        f'--remote-debugging-port={port}',
        f'--user-data-dir=C:\\chromeCookie_{port}',
        '--start-maximized', 
        "--disable-features=PrivacySandboxSettings4,PrivacySandboxAdsAPIs,InterestCohortAPI",
        "--disable-extensions",
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
    ])


    time.sleep(5+random())
    pyautogui.hotkey('alt', 'd')
    pyautogui.write(url, interval=0.05)
    pyautogui.press('enter', interval=0.1)

    ret = True
    button5location = None
    st = time.time()    
    tgt_img = login_yellow_path
    while True:
        if time.time() - st > 20:
            ret = False
            break
        try:
            button5location = pyautogui.locateOnScreen(tgt_img, confidence=0.9)
            print("Get Log In Button, so home page is loaded")
            time.sleep(1)
            break
        except:
            time.sleep(random())
            continue
    return ret, chrome, button5location

def do_login(username, password, login_btn_pos):
    ret = False
    print('--- start login')
    enter_username(username, login_btn_pos)
    if evaluate_security():
        enter_password(password)
        ret = True
        print('--- login success')
    else:
        print('--- login failed')
    return ret

def enter_username(username, btn_pos):
    x, y, w, h = btn_pos

    x = randint(x-200, x-90)
    y = randint(y, y+h)
    pyautogui.moveTo(x, y, 1)
    pyautogui.click()
    pyautogui.write(username, interval=0.2)
    pyautogui.press('enter', interval=0.5)

def evaluate_security():
    ret = True
    st = time.time()
    tgt_img = ok_green_path
    while True:
        if time.time() - st > 15:
            ret = False
            break
        try:
            button5location = pyautogui.locateOnScreen(tgt_img, confidence=0.9)
            print("Get Green Ok Button, so prepare to input password")
            time.sleep(random())
            break
        except:
            time.sleep(random())            
            continue
    if ret:        
        pyautogui.press('tab', presses=2, interval=0.5)
        pyautogui.press('enter', presses=1)
        time.sleep(2*random())
    return ret

def enter_password(password):
    pyautogui.write(password, interval=0.2)
    pyautogui.press('enter', interval=0.5)

def is_logined(delay):
    ret = True
    st = time.time()
    tgt_img = account_tool_path
    while True:
        if time.time() - st > 60 * delay:
            ret = False
            break
        try:
            x, y = pyautogui.locateCenterOnScreen(tgt_img, confidence=0.8)
            pyautogui.moveTo(x, y, 1)
            print("Get Account ToolBar, so login Successed")
            break
        except:
            time.sleep(random()*2)
            continue    
    return ret

def refresh_page():
    pyautogui.hotkey('ctrl', 'shift', 'r')
    time.sleep(action_wait)

def exit_chrome(chrome):    
    print("exit chrome")
    if chrome:
        chrome.kill()
        # chrome.terminate()
        # chrome.wait()

    time.sleep(1 + 2*random())

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_cookie(port):
    cookie_dir = f"C:\\chromeCookie_{port}"
    try:
        shutil.rmtree(cookie_dir, onerror=remove_readonly)
    except Exception as e:
        print(f"Failed to delete {cookie_dir}: {e}")

def exit_driver(driver):
    if driver:
        driver.quit()

# def remove_cookie(port=9292):
#     import shutil
#     shutil.rmtree(f"C:\\chromeCookie_{port}")

def check_captcha():
    ret = False
    st = time.time()
    tgt_img = captcha_path
    while True:
        if time.time() - st > 2:
            ret = False
            break
        try:
            x, y = pyautogui.locateCenterOnScreen(tgt_img, confidence=0.8)
            print("Got Captcha.")
            break
        except:
            time.sleep(random()*2)
            continue    
    return ret

def get_screenshot_b64():
    try:
        im = pyautogui.screenshot()
        buff = BytesIO()
        im.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue()).decode("utf-8")
    except:
        img_str = ''
    return img_str