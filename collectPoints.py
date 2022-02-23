import sys
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import Proxy, ProxyType



#timeouts to emulate human delay because of bot detection
#chromedriver for chrome version 98

#TODO
#   24hr sleep time, but since this script is inteded to be ran as a cronjob, dont know about that
#   Add better automation flagging evasion, currently the script works for 1 account every 24 hours, still gotta make it more dynamic for it to support multiple accounts
#   Add chrome version check and chromedriver automatic updates

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
options.add_extension("./Buster.crx")

#Proxy configuration in case of IP flagging 
#TODO
#   Add proxy rotation and validation
#options.add_argument('--proxy-server=104.149.3.3:8080')

driver = webdriver.Chrome(executable_path = path,options=options)

url="https://www.warmane.com/account/login"

#TODO:
#   Use implicit waits to avoid errors caused by internet connection or slow page loading
#   Convert entire script to class for prettier code and more capabilites
#   Add captcha loaded check in case of bad user agent

try:
    #get login info from the file (in case of multiple accounts)
    with open('login.txt') as credentials:
        #skip first two lines in the login text file
        lines = credentials.readlines()[2:]
    for line in lines:    
        creds = line.split(",")  
        username = creds[0]
        password = creds[1].lstrip()  
        time.sleep(1)
        driver.get(url)
        time.sleep(2)
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
        time.sleep(1)
        loginButton = driver.find_element_by_xpath('//*[@id="frmLogin"]/div/button')
        loginButton.click()
        time.sleep(10)
        collectLink = driver.find_element_by_xpath('/html/body/div[3]/div[5]/div/div[2]/div[1]/table/tbody/tr[4]/td/span[2]/a')
        collectLink.click()
        time.sleep(5)
        driver.quit()
    credentials.close()      
    
except KeyboardInterrupt:
    print("Keyboard Intterupt, Exiting")
    driver.quit()
    time.sleep(3)
    sys.exit(0)