# Chrome driver
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import filedialog

def checkDriverAndBinary():
    try:
        currDir = os.getcwd()
        os.chdir(currDir)
        with open(os.path.join(currDir, "Tmp/fileDriverAndBinary.txt"), "r") as f:
            dirs = f.readlines()
        if len(dirs) == 0:
            root = tk.Tk()
            root.withdraw()
            chromeDriver = filedialog.askopenfilename(title="Mở file driver chromedriver.exe (file download)")
            chromeBinary = filedialog.askopenfilename(title="Mở file chrome.exe (Nằm ở C:\Program Files\Google\Chrome\Application\chrome.exe).")
            with open(os.path.join(currDir, "Tmp/fileDriverAndBinary.txt"), "w") as wf:
                wf.write(f"{chromeDriver}\n{chromeBinary}")
            return chromeDriver, chromeDriver
        else:
            chromeDriver = dirs[0].strip()
            chromeBinary = dirs[1].strip()
        return chromeDriver, chromeBinary
    except FileNotFoundError as err:
        print(f"{err}")
        return 0, 0

def initBrowser():
    chromeDriver, chromeBinary = checkDriverAndBinary()
    if chromeDriver and chromeBinary:
        try:
            currDir = os.getcwd()
            os.chdir(currDir)
            
            # Config options
            options = Options()
            # options.add_argument("--headless=new")

            options.page_load_strategy = 'normal'

            options.add_argument('--no-sandbox')
            ###########################################################################
            # Changed dated 2023-06-29 
            # Add more options
            # Adding argument to disable the AutomationControlled flag 
            options.add_argument("--disable-blink-features=AutomationControlled") 
            # Exclude the collection of enable-automation switches 
            options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
            
            # Turn-off userAutomationExtension 
            options.add_experimental_option("useAutomationExtension", False) 
            ###########################################################################
            options.add_argument('--disable-dev-shm-usage')

            userPath = os.path.join(currDir, "userdata")
            
            # Add path of userdata
            options.add_argument(f"--user-data-dir={userPath}")
            #provide the profile name with which we want to open browser
            options.add_argument(r"--profile-directory=Profile 1")
            
            options.binary_location = chromeBinary
 
            service = Service(executable_path=chromeDriver)
            # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            browser = webdriver.Chrome(service=service, options=options)
            ###########################################################################
            # Changed dated 2023-06-29 
            # Changing the property of the navigator value for webdriver to undefined 
            browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
            
            ###########################################################################
            return browser
        except Exception as err:
            print(f'{err}')
            return 0
    else:
        print("Initiate failed.")
        return 0

def browseWebsite(browser):
    try:
        browser.get('https://www.creativefabrica.com/login/')
        return browser
    except Exception as err:
        print(f'{err}')
        browser.quit()
        return 0

def logIn(browser, user, password):
    try:
        time.sleep(5)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='email']")))
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password']")))
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit']")))
        for _ in range(0, 5):
            browser.find_element(By.TAG_NAME, "html").send_keys(Keys.DOWN)
        i_email = browser.find_element(By.XPATH, "//input[@type='email']")
        i_email.send_keys(user)
        time.sleep(1)
        i_pass = browser.find_element(By.XPATH, "//input[@type='password']")
        i_pass.send_keys(password)
        time.sleep(1)        
        b_submit = browser.find_element(By.XPATH, "//button[@type='submit']")
        b_submit.send_keys(Keys.ENTER)
        try:
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located(
                    (By.LINK_TEXT, "Add Graphic")))
        except Exception:
            _ = input('On OTP page. Type OTP code press submit. Then press enter from terminal.')
        return browser
    except Exception as err:
        print(f'{err}')
        browser.quit()
        return 0
    
def goToAddGraphic(browser):
    try:
        time.sleep(2)
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Add Graphic")))
        for _ in range(0, 5):
            browser.find_element(By.TAG_NAME, "html").send_keys(Keys.DOWN)
        l_addGrapic = browser.find_element(By.LINK_TEXT, "Add Graphic")
        l_addGrapic.click()
        time.sleep(4)
        # press the cancel pop buttons
        try:
            b_cancle = browser.find_element(
                By.XPATH, "//button[@id='onesignal-slidedown-cancel-button']"
                )
            b_cancle.send_keys(Keys.ENTER)
        except Exception as err:
            print(f'{err}')
        return browser
    except Exception as err:
        print(f'{err}')
        browser.quit()
        return 0

def checkWhichLandingPage(browser):
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Add Graphic")))
        return "addgraphic", browser
    except Exception:
        return "login", browser

def logInSession(user, password):
    user = user
    password = password
    browser = initBrowser()
    if not browser:
        return 0
    browser = browseWebsite(browser)
    if not browser:
        return 0
    page, browser = checkWhichLandingPage(browser)
    if page == "login":
        browser = logIn(browser, user, password)
        if not browser:
            return 0
        browser = goToAddGraphic(browser)
        if not browser:
            return 0
    elif page == "addgraphic":
        browser = goToAddGraphic(browser)
        if not browser:
            return 0
    else:
        print("Not on both pages!!!")
        return 0
    return browser