import sys
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import Proxy, ProxyType
import chromedriver_autoinstaller

#timeouts to emulate human delay because of bot detection
#chromedriver for chrome version 98 - Automatically updates

#TODO
#   Add better automation flagging evasion, currently the script works for 1 account every 24 hours, still gotta make it more dynamic for it to support multiple accounts

#TODO:
#   Use implicit waits to avoid errors caused by internet connection or slow page loading
#   Add captcha loaded check in case of bad user agent


class PointCollector:
    options=None
    driver=None
    ua = None
    path = r'./chromedriver'
    captchaElement = None
    creds = []
    username = None
    password = None
    noOfAccounts= None
    
    url="https://www.warmane.com/account/login"
    
    def __init__(self):
        #check chromedriver version and auto update
        chromedriver_autoinstaller.install()
        
        self.driverStart()
        self.driver.get(self.url)
        counter=0
        self.checkIfCaptchaLoaded()
        
        self.getNoOfAccounts()
        
        while counter<self.noOfAccounts:
            time.sleep(2)
            self.enterLoginInfo(counter)
            self.solveCaptcha()
            self.logIn()
            self.collectPoints()
            counter+=1  
            
    def driverStart(self):
        self.optionsSetup()
        self.proxySetup()
        self.driver = webdriver.Chrome(executable_path = self.path,options=self.options)
        
    
    def optionsSetup(self):
        print("Setting up options")
        ua = UserAgent()
        userAgent = ua.random
        self.options=webdriver.ChromeOptions()
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument(f'user-agent={userAgent}')
        self.options.add_argument("--window-size=1100,1000")
        #options.add_argument('--incognito')
        #options.add_argument('--headless')
        #load buster captcha solver extension into the driver
        self.options.add_extension("./Buster.crx")
        
        
    def proxySetup(self):
        #Proxy configuration in case of IP flagging 
        #TODO
        #   Add proxy rotation and validation
        #options.add_argument('--proxy-server=104.149.3.3:8080')
        return 0
    
    def checkIfCaptchaLoaded(self):
        print("Checking if captcha is loaded")
        time.sleep(5)
        try:
            self.driver.switch_to_default_content()
            self.driver.switch_to_frame(self.driver.find_element_by_xpath("/html/body/div[3]/div[5]/div/div[2]/div[1]/form/table/tbody/tr[7]/td/div/div/div/iframe"))
            captcha = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]')
            self.captchaElement = captcha
            paragraphElement = self.driver.find_element_by_xpath('/html/body/div/div[3]/p[1]')
            if paragraphElement.text=='Please upgrade to a ':
                self.driver.close()
                time.sleep(15)
                self.driverStart()
                self.checkIfCaptchaLoaded()
                
            else:
                pass
        except NoSuchElementException:
            #TODO: Make this part prettier and not janky
            pass
    
    
    def solveCaptcha(self):    
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("/html/body/div[3]/div[5]/div/div[2]/div[1]/form/table/tbody/tr[7]/td/div/div/div/iframe"))    
        #click captcha
        self.captchaElement.click()
        time.sleep(random.randrange(3,6))
        #handle new iframe popup
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame(self.driver.find_element_by_xpath("/html/body/div[5]/div[4]/iframe"))
        time.sleep(5)
        busterButton = self.driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]')
        busterButton.click()
        time.sleep(1)
        busterButton.click()
        time.sleep(10)
        
        
    def getCredentials(self):
        #get login info from the file 
        print("Getting credentials")
        with open('login.txt') as credentials:
            #skip first two lines in the login text file
            lines = credentials.readlines()[2:]
            for line in lines:    
                self.creds+=line.split(",")
        
        print("Done")
        credentials.close()      
             
             
    def getNoOfAccounts(self):
        print("Getting no of accounts")
        self.getCredentials()
        print(str(len(self.creds)/2)+" Accounts found")
        print(self.creds)
        if len(self.creds)==2:
           self.noOfAccounts=1
        else:
            self.noOfAccounts=len(self.creds)/2
    
    
    #using counter in case of multiple accounts
    def enterLoginInfo(self,counter):
        self.driver.switch_to_default_content()
        username = self.creds[counter].lstrip().rstrip()
        password = self.creds[counter+1].lstrip().rstrip()  
        unameElement=self.driver.find_element_by_id("userID")
        passwordElement=self.driver.find_element_by_id("userPW")
        time.sleep(1)
        unameElement.click
        time.sleep(2)
        unameElement.send_keys(username)
        time.sleep(2)
        passwordElement.click()
        time.sleep(2)
        passwordElement.send_keys(password)
        time.sleep(2)
              
               
    def logIn(self):
        self.driver.switch_to_default_content()
        time.sleep(1)
        loginButton = self.driver.find_element_by_xpath('//*[@id="frmLogin"]/div/button')
        loginButton.click()
        time.sleep(10)


    def collectPoints(self):
        collectLink = self.driver.find_element_by_xpath('/html/body/div[3]/div[5]/div/div[2]/div[1]/table/tbody/tr[4]/td/span[2]/a')
        collectLink.click()
        time.sleep(5)
        self.driver.quit()
    
        
        
try:
    collect=PointCollector()    
      
except KeyboardInterrupt:
    print("Keyboard Intterupt, Exiting")
    PointCollector.driver.quit()
    time.sleep(3)
    sys.exit(0)