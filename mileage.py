from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time


# ----------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------
# mileage.csv
# seperator: tab
# Date          from    to      vehicle distance    comment
# 05/02/2022	Home	HKMC	Short	100

# ----------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------
timeout = 60

def newExpense(tranDate, fromLoc, toLoc, vehicleId, distance, comment):
    xpath = "//span[@data-trans-id='Expense.addExpense']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    xpath = "//span[text()='Personal Car Mileage']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    time.sleep(0.3)

    xpath = "//input[@name='transactionDate']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(Keys.CONTROL + "a")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(Keys.DELETE)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(tranDate)

    xpath = "//input[@name='fromLocation']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(fromLoc)

    xpath = "//input[@name='toLocation']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(toLoc)

    xpath = "//div[@data-nuiexp='field-carKey']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    xpath = f"//li/span[text()='{vehicleId}']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    xpath = "//input[@name='businessDistance']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(Keys.CONTROL + "a")
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(Keys.DELETE)
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(distance)

    xpath = "//textarea[@name='comment']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(comment)

    xpath = "//span[@data-trans-id='expenseEntry.saveExpense']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    time.sleep(2)

    # # Wait Save is done
    # xpath="//*[text()='Allocate']"
    # WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
# Launch Browser
driver = webdriver.Chrome("./chromedriver")

driver.get("http://www.siemens.com/travel")

# select first expense
xpath="//li[@class='  cnqr-tile-1']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

with open('mileage.csv', 'r') as csvfile:
    f = csv.reader(csvfile, delimiter='\t', lineterminator="\r\n")
    for values in f:
        trDate, fromLoc, toLoc, vehicleId, distance, comment = values

        distance = distance.strip()
        comment = comment.strip()
        # if (len(values) > 5):
        #     comment = values[5]
        print(trDate, fromLoc, toLoc, vehicleId, distance, comment)

        newExpense(trDate, fromLoc, toLoc, vehicleId, distance, comment)

