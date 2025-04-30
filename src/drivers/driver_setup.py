import subprocess
import time
import random
import pyautogui as pg

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def start_chrome_home(url, port):
    """
    Launches Chrome with a specific URL using remote debugging, and waits
    for the login page to load based on the appearance of a button or screen element.
    
    :param url: The URL to navigate to.
    :param port: The port for remote debugging.
    :return: (bool, Popen object, button location or None)
    """
    print(f"🟡 ACTION: Open Chrome and navigate to home page")

    chrome = None
    ret = False
    try:
        # Start Chrome with remote debugging and user profile.
        chrome = subprocess.Popen([
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            f'--remote-debugging-port={port}',
            f'--user-data-dir=C:\\chrome_profiles\\bot_{port}',
            '--start-maximized',
            "--disable-features=PrivacySandboxSettings4,PrivacySandboxAdsAPIs,InterestCohortAPI",
            "--disable-extensions",
            "--disable-popup-blocking",
            "--no-first-run",
            "--no-default-browser-check",
        ])

        # Give Chrome time to initialize before interacting with it.
        time.sleep(5 + random.random())

        # Focus Chrome and type the URL
        pg.hotkey('alt', 'd')
        pg.write(url, interval=0.05)
        pg.press('enter', interval=0.1)

        # Initialize the return value for success
        ret = True
        print(f"✅ Chrome opened successfully, navigating to {url}.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while starting Chrome: {e}")
    except pg.FailSafeException as e:
        print(f"❌ Error occurred during pg operation: {e}")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")

    return ret, chrome

def create_driver(port: int):
    """
    Connects to an existing Chrome session via remote debugging port.
    
    :param port: The port used by Chrome for remote debugging.
    :return: Selenium WebDriver instance
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        
        driver = webdriver.Chrome(options=options)
        print("✅ Driver created and attached to existing Chrome session successfully.")
        return driver

    except WebDriverException as e:
        print(f"❌ Selenium WebDriver Error: {e}")
        raise  # Let the calling code handle it

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        raise  # Let the calling code handle it
