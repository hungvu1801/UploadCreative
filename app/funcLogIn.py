# Chrome driver
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initBrowser():
    try:
        currDir = os.getcwd()
        os.chdir(currDir)
        
        # Config options
        options = Options()
        # options.add_argument("--headless=new")

        options.page_load_strategy = 'normal'

        # options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            os.mkdir("userdata")
            userPath = os.path.join(currDir, "userdata")
            # Add path of userdata
            options.add_argument(f"--user-data-dir={userPath}")
            options.add_argument(r"--profile-directory=Profile 1")
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception:
            pass
        userPath = os.path.join(currDir, "userdata")
        
        # Add path of userdata
        options.add_argument(f"--user-data-dir={userPath}")
        #provide the profile name with which we want to open browser
        options.add_argument(r"--profile-directory=Profile 1")

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return browser
    except Exception as err:
        print(f'{err}')
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