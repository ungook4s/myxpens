from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import configparser as parser

# ----------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------
properties = parser.ConfigParser()
properties.read('./config.ini')
city = properties['CONFIG']['city']
bizPurpose = properties['CONFIG']['purpose']

# ----------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------
timeout = 60

# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
# Launch Browser
driver = webdriver.Chrome("./chromedriver")

driver.get("http://www.siemens.com/travel")

xpath="//a[@id='btnToggle']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# xpath="//div[@class='login-method-text']"
# WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

xpath="//a[@class='btn btn-primary right-aligned']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# select first expense
xpath="//li[@class='  cnqr-tile-1']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# Find error nodes
xpath="//button[@aria-label='Show Errors']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

elements = driver.find_elements(By.XPATH, xpath)

while (len(elements) > 0):
    elem = elements[0]
    print(elem)

    # navigate its parent nodes from error icon, then find clickable node in children
    xpath="../../..//div[@data-nuiexp='expenseType-name']"
    elem.find_element(By.XPATH, xpath).click() 

    xpath="//li[@class='form-header__list-item']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    xpath="//*[text()='Allocate']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    time.sleep(1)

    # City of Purchase
    xpath="//input[@data-nuiexp='field-locName']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    time.sleep(1) # it requires, otherwise it went wrong...

    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(Keys.CONTROL + "a")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(Keys.DELETE)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(city)

    time.sleep(1)

    xpath=f"//li/span[text()='{city}']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # wait till input is complete
    xpath=f"//input[@value='{city}']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    time.sleep(2)

    # Business Purpose
    xpath="//input[@data-nuiexp='field-description']"
    try:
        elem = driver.find_element(By.XPATH, xpath) 
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        time.sleep(1) # it requires, otherwise it went wrong...

        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(Keys.DELETE)
        elem.send_keys(bizPurpose)
    except NoSuchElementException:
        print("Skip. No Business Purpose")

    # Save Expense
    xpath = "//span[@data-trans-id='expenseEntry.saveExpense']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    time.sleep(1)

    xpath="//button[@aria-label='Show Errors']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    elements = driver.find_elements(By.XPATH, xpath)
