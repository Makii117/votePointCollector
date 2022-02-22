import sys
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from fake_useragent import UserAgent


#timeouts to emulate human delay since recaptcha can detect bots
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
    
    
    
    
    
except KeyboardInterrupt:
    print("Keyboard Intterupt, Exiting")
    driver.quit()
    time.sleep(3)
    sys.exit(0)