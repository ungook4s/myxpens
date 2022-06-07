from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
import mylib
import configparser as parser

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

def newExpense(tranDate, fromLoc, toLoc, vehicleId, distance, comment):
    clickXpath("Add Expense", "//span[@data-trans-id='Expense.addExpense']")

    clickXpath("Personal Car Mileage", "//span[text()='Personal Car Mileage']")

    time.sleep(0.3)

    xpath = "//input[@name='transactionDate']"
    sendKeys("Send keys Ctrl+a", xpath, Keys.CONTROL + "a")
    sendKeys("Send keys DEL", xpath, Keys.DELETE)
    sendKeys("Send keys {tranDate}}", xpath, tranDate)

    sendKeys("Send keys {fromLoc}", "//input[@name='fromLocation']", fromLoc)

    sendKeys("Send keys {toLoc}", "//input[@name='toLocation']", toLoc)

    clickXpath("VehicleId Combo", "//div[@data-nuiexp='field-carKey']")

    clickXpath(f"VehicleId {vehicleId}", f"//li/span[text()='{vehicleId}']")

    xpath = "//input[@name='businessDistance']"
    sendKeys("Send keys Ctrl+a", xpath, Keys.CONTROL + "a")
    sendKeys("Send keys DEL", xpath, Keys.DELETE)
    sendKeys("Send keys distance", xpath, distance)
    sendKeys("Send keys comment", "//textarea[@name='comment']", comment)

    clickXpath("Save Expense", "//span[@data-trans-id='expenseEntry.saveExpense']")

    time.sleep(2)

# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
driver.get("http://www.siemens.com/travel")

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

with open('mileage.csv', 'r') as csvfile:
    f = csv.reader(csvfile, delimiter='\t', lineterminator="\r\n")
    lineno = 0;
    for values in f:
        lineno += 1
        comment = ""

        if (len(values) == 0) : continue

        if (len(values) == 1) : 
            if values[0].startswith("#") : continue

        if (len(values) < 5 or len(values) > 6) :
            print(f"Content of csv file is not proper. Line {lineno}: {values}" )
            print("Exmaple row is following" )
            print("05/02/2022	Home	HKMC	Short	100" )
            sys.exit()
        elif (len(values) == 6 ):
            trDate, fromLoc, toLoc, vehicleId, distance, comment = values
        elif (len(values) == 5 ):
            trDate, fromLoc, toLoc, vehicleId, distance = values

        distance = distance.strip()
        comment = comment.strip()

        print(trDate, fromLoc, toLoc, vehicleId, distance, comment)
        newExpense(trDate, fromLoc, toLoc, vehicleId, distance, comment)
        
print("Job is complete")
