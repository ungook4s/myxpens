from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import configparser as parser
import mylib

# ----------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------
properties = parser.ConfigParser()
properties.read('./config.ini')
city = properties['CONFIG']['city']
bizPurpose = properties['CONFIG']['purpose']

# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
timeout = 60
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome("./chromedriver", chrome_options=options)


clickCss = mylib.clickCss(driver, timeout)
clickXpath = mylib.clickXpath(driver, timeout)
waitXpath = mylib.waitXpath(driver, timeout)
sendKeys = mylib.sendKeys(driver, timeout)
sleep = mylib.sleep(driver, timeout)

# Login
waitXpath("wait", "//div[@class='login-method-title']")

email = properties['CONFIG']['email']
passwd = properties['CONFIG']['passwd']
if (len(email) > 0):
    clickXpath("Email", "//div[@class='login-method-icon icon-mail_login']")
    waitXpath("wait", "//div[@class='login-method-collapsible in collapse show']")

    sendKeys("email", "//input[@id='username']", email)
    sendKeys("password", "//input[@id='password']", passwd)

    clickXpath("Login", "//*[@id='btnLoginEmail']")
    clickXpath("Mobile Authentication", "//div[@class='login-method-icon icon-pingid']")

rowNo = properties['CONFIG']['row_no']
clickXpath("Select first expense", f"//div[@data-id='mytasks-expensereportslist']//li[contains(@class, 'cnqr-tile-{rowNo}')]")

waitXpath("Wait page is loaded", "//span[@data-trans-id='Expense.addExpense']")

# Find expense with Error
xpath="//button[@aria-label='Show Errors']"
elements = driver.find_elements(By.XPATH, xpath)

while (len(elements) > 0):
    elem = elements[0]
    print(elem)

    # navigate its parent nodes from error icon, then find clickable node in children
    xpath="../../..//div[@data-nuiexp='expenseType-name']"
    elem.find_element(By.XPATH, xpath).click() 

    waitXpath("Wait ...", "//p[@class='sapcnqr-spinner__message']")
    waitXpath("Wait ..", "//li[@class='form-header__list-item']")

    sleep(1)

    xpath="//input[@data-nuiexp='field-locName']"
    waitXpath("City of Purchase", xpath)
    sleep(1) # it requires, otherwise it went wrong...

    sendKeys("Send keys Ctrl+a", xpath, Keys.CONTROL + "a")
    sendKeys("Send keys DEL", xpath, Keys.DELETE)
    sendKeys("Send keys city", xpath, city)

    sleep(1)

    clickXpath("Click city in Combo", f"//li/span[text()='{city}']")

    sleep(1)

    waitXpath("Wait till input is complete", f"//input[@value='{city}']")

    sleep(2)

    # Business Purpose
    xpath="//input[@data-nuiexp='field-description']"
    try:
        elem = driver.find_element(By.XPATH, xpath) 
        waitXpath("Wait", xpath)

        sleep(1) # it requires, otherwise it went wrong...

        sendKeys("Send keys Business Purpose", xpath, Keys.CONTROL + "a")
        sendKeys("Send keys Business Purpose", xpath, Keys.DELETE)
        sendKeys("Send keys Business Purpose", xpath, bizPurpose)
    except NoSuchElementException:
        print("Skip. No Business Purpose")

    clickXpath("Save Expense", "//span[@data-trans-id='expenseEntry.saveExpense']")

    sleep(0.5)

    waitXpath("Wait ...", "//p[@class='sapcnqr-spinner__message sapcnqr-spinner__message--large']")

    sleep(1)

    waitXpath("Wait list page is loaded", "//span[@data-trans-id='Expense.addExpense']")

    # Find expense with Error
    xpath="//button[@aria-label='Show Errors']"
    elements = driver.find_elements(By.XPATH, xpath)

print("Job is complete")
