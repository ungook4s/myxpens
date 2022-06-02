from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import configparser as parser
import mylib

# ----------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------
properties = parser.ConfigParser()
properties.read('./config.ini')
attendeeName = properties['CONFIG']['attendee']

# ----------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------
timeout = 60

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# options.add_experimental_option('prefs', {'intl.accept_languages': 'ko,ko_KR'})
driver = webdriver.Chrome("./chromedriver", chrome_options=options)

clickCss = mylib.clickCss(driver, timeout)
clickXpath = mylib.clickXpath(driver, timeout)
waitXpath = mylib.waitXpath(driver, timeout)
sendKeys = mylib.sendKeys(driver, timeout)
sleep = mylib.sleep(driver, timeout)

def addAttendee():
    clickCss("Attendee (0)", ".attendees-link > .sapcnqr-button__text")
    sleep(1)

    xpath = "//*[@id='attendees-add']"
    waitXpath("Add", xpath)
    sendKeys("Add", xpath, Keys.RETURN)
    sleep(1)

    waitXpath("Attendees", "//span[@data-trans-id='attendees.import']")

    xpath = "(//span[@data-trans-id='attendees.attendees'])[2]"
    waitXpath("Wait for Attendee", xpath)
    clickXpath("Attendee", xpath)

    sleep(0.5)

    sendKeys("Enter Name in First Name", "//input[@name='firstName']", attendeeName)

    clickXpath("Search", "//span [@data-trans-id='common.search']")
    
    clickXpath("Select a first row", "//input[@aria-label='Select row']")

    clickXpath("Add to List", "//span[@data-trans-id='attendees.addToList']")

    clickXpath("x", "(//button[@aria-label='Close'])[3]")

    clickXpath("Save", "//span[@data-trans-id='common.save']")

    sleep(2)

    waitXpath("Wait ...", "//p[@class='sapcnqr-spinner__message']")
    waitXpath("Wait ..", "//li[@class='form-header__list-item']")
    # waitXpath("Wait .", "//*[text()='Allocate']")

# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
# Launch Browser

driver.get("http://www.siemens.com/travel")

clickXpath("Show all available login methods", "//a[@id='btnToggle']")

rowNo = properties['CONFIG']['row_no']
clickXpath("Select first expense", f"//div[@data-id='mytasks-expensereportslist']//li[contains(@class, 'cnqr-tile-{rowNo}')]")

# Find expenses
xpath="//div[text() = 'Business Meals (Staff Only) (taxable)']"
waitXpath("Find all Business Meals", xpath);

elements = driver.find_elements(By.XPATH, xpath)

for i in range(len(elements)):
    elem = elements[i]

    try:
        # Find expend rows with attendee
        # xpath ..// find from its parent node
        elem.find_element(By.XPATH, "..//span[@class='screen-reader-only']") 
        print("Skip the expense. Attendee is already added.")
    except NoSuchElementException:
        print(f"Open expense[{i}]")
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(elem)).click()

        sleep(1)

        waitXpath("Wait till save is done", "//li[@class='form-header__list-item']")
        # waitXpath("Wait .", "//*[text()='Allocate']")

        sleep(1)

        try:
            xpath="//*[text() = 'Attendees (0)']"
            driver.find_element(By.XPATH, xpath)
            addAttendee()
        except NoSuchElementException:
            print("Skip the expense. Attendee is already added.")

        # Go Back to list     # it requires due to stale elements
        driver.execute_script("window.history.go(-1)")
        sleep(1)

        xpath="//div[text() = 'Business Meals (Staff Only) (taxable)']"
        waitXpath("Wait for list is dispalyed", xpath)

        elements = driver.find_elements(By.XPATH, xpath)


print("Job is complete")

# driver.close()
