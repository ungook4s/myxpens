from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
import mylib
import configparser as parser
import pyautogui 
from threading import Thread
import subprocess

# ----------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------
# mileage.csv
# seperator: tab
# Date          from    to      vehicle distance    comment
# 05/02/2022	Home	HKMC	Short	100
properties = parser.ConfigParser()
properties.read('./config.ini')

# ----------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome("./chromedriver", chrome_options=options)

timeout = 60

clickCss = mylib.clickCss(driver, timeout)
clickXpath = mylib.clickXpath(driver, timeout)
waitXpath = mylib.waitXpath(driver, timeout)
sendKeys = mylib.sendKeys(driver, timeout)
sleep = mylib.sleep(driver, timeout)

def enterpw_certifcate():
    sleep(2)

    subprocess.check_call([r"softkey.exe"])

    result =  [char for char in softkeypw]
    result.append('enter')

    print(result)

    pyautogui.press(result)

    # Thread(target = enterpw_certifcate).start()

def accept_certifcate():
    print("accept_certifcate")
    sleep(3)
    pyautogui.press('enter')
    print("accept_certifcate end")
    #Presses 10 times
    # for i in range(0,10):
    #     pyautogui.press('enter')

    enterpw_certifcate()

driver.get("http://www.siemens.com/travel")

waitXpath("wait", "//div[@class='login-method-title']")

# Email
try:        
    email = properties['CONFIG']['email']
    passwd = properties['CONFIG']['passwd']
except KeyError:
    email = ""

# Softkey
try:        
    softkeypw = properties['CONFIG']['softkeypw']
except KeyError:
    softkeypw = ""


if (len(email) > 0):
    clickXpath("Email", "//div[@class='login-method-icon icon-mail_login']")
    waitXpath("wait", "//div[@class='login-method-collapsible in collapse show']")

    sendKeys("email", "//input[@id='username']", email)
    sendKeys("password", "//input[@id='password']", passwd)

    clickXpath("Login", "//*[@id='btnLoginEmail']")
    clickXpath("Mobile Authentication", "//div[@class='login-method-icon icon-pingid']")
elif (len(softkeypw) > 0) :
    clickXpath("Show all available login methods", "//a[@id='btnToggle']")

    thread = Thread(target = accept_certifcate)
    thread.start()

    clickXpath("Softkey", "//div[@class='login-method-icon icon-soft-PKI']")
    # WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='login-method-icon icon-soft-PKI']"))).click()

sleep(2)

print("login complete")  

clickXpath("Confirm", "//a[@class='btn btn-primary right-aligned']")

rowNo = properties['CONFIG']['row_no']
clickXpath("Select first expense", f"//div[@data-id='mytasks-expensereportslist']//li[contains(@class, 'cnqr-tile-{rowNo}')]")

waitXpath("Wait page is loaded", "//span[@data-trans-id='Expense.addExpense']")

print("done")  
