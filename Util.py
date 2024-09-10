import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import Config

def init_driver():
    options = webdriver.ChromeOptions()
    if Config.auto_login == True:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

    return webdriver.Chrome(options=options)

def login(driver):
    driver.implicitly_wait(Config.implicitly_wait_time)
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.implicitly_wait(1)

    driver.execute_script("document.getElementsByName('id')[0].value=\'" + Config.user_id + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + Config.user_pw + "\'")

    if Config.auto_login == True:
        driver.find_element(by=By.XPATH, value='//*[@id="log.login"]').click()
    else:
        time.sleep(Config.manual_login_wait_time)
