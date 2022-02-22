import sys
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from fake_useragent import UserAgent


#timeouts to emulate human delay because of bot detection
#chromedriver for chrome version 98


#initialize chromedriver and give it a useragent
path = r'./chromedriver'
ua = UserAgent()
userAgent = ua.random

options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument('--ignore-certificate-errors')
options.add_argument(f'user-agent={userAgent}')
options.add_argument("--window-size=1100,1000")
#options.add_argument('--incognito')
#options.add_argument('--headless')

#load buster captcha solver extension into the driver
#TODO: 
#     Get packaged extension for the driver so it comes with the app
options.add_argument("--load-extension=C:\\Users\\BIOSs\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\mpbjkejclgfgadiemmefgebjfooflfhl\\1.3.1_0")


driver = webdriver.Chrome(executable_path = path,chrome_options=options)

url="https://www.warmane.com/account/login"

username = ""
password = ""

try:
    driver.get(url)
    time.sleep(1)
    unameElement=driver.find_element_by_id("userID")
    passwordElement=driver.find_element_by_id("userPW")
    time.sleep(1)
    unameElement.click
    time.sleep(2)
    unameElement.send_keys(username)
    time.sleep(2)
    passwordElement.click()
    time.sleep(2)
    passwordElement.send_keys(password)
    time.sleep(2)
    #load captcha iframe
    driver.switch_to_frame(driver.find_element_by_xpath("/html/body/div[3]/div[5]/div/div[2]/div[1]/form/table/tbody/tr[7]/td/div/div/div/iframe"))
    #click captcha
    time.sleep(2)
    captchaClick=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]')
    time.sleep(1)
    captchaClick.click()
    time.sleep(random.randrange(3,6))
    #handle new iframe popup
    driver.switch_to_default_content()
    driver.switch_to_frame(driver.find_element_by_xpath("/html/body/div[5]/div[4]/iframe"))
    time.sleep(5)
    busterButton = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]')
    busterButton.click()
    time.sleep(10)
    #leave captcha iframe
    driver.switch_to_default_content()
    loginButton = driver.find_element_by_xpath('//*[@id="frmLogin"]/div/button')
    loginButton.click()
      
    
except KeyboardInterrupt:
    print("Keyboard Intterupt, Exiting")
    driver.quit()
    time.sleep(3)
    sys.exit(0)