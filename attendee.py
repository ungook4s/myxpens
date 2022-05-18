from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import configparser as parser

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

def addAttendee():
    # Attendee (0)
    css = ".attendees-link > .sapcnqr-button__text"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()
    time.sleep(1)

    # Add
    xpath = "//*[@id='attendees-add']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(Keys.RETURN)
    time.sleep(1)

    # Attendees
    xpath = "//span[@data-trans-id='attendees.import']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    xpath = "(//span[@data-trans-id='attendees.attendees'])[2]"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # Enter Name in First Name
    time.sleep(0.5)

    xpath = "//input[@name='firstName']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(attendeeName)

    # Click Search
    xpath = "//span [@data-trans-id='common.search']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    
    # Select a first row
    xpath = "//input[@aria-label='Select row']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # Add to List
    xpath = "//span[@data-trans-id='attendees.addToList']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # click x
    xpath = "(//button[@aria-label='Close'])[3]"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # Save
    xpath = "//span[@data-trans-id='common.save']"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    time.sleep(2)

    # Wait Save is done
    xpath="//p[@class='sapcnqr-spinner__message']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    xpath="//li[@class='form-header__list-item']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    xpath="//*[text()='Allocate']"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def getText(element):
    return driver.execute_script("""
    var parent = arguments[0];
    var child = parent.firstChild;
    var ret = "";
    while(child) {
        if (child.nodeType === Node.TEXT_NODE)
            ret += child.textContent;
        child = child.nextSibling;
    }
    return ret;
    """, element) 
# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
# Launch Browser
driver = webdriver.Chrome("./chromedriver")

driver.get("http://www.siemens.com/travel")

xpath="//a[@id='btnToggle']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

xpath="//a[@class='btn btn-primary right-aligned']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# select first expense
xpath="//li[@class='  cnqr-tile-1']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# Find all Business Meals
xpath="//div[text() = 'Business Meals (Staff Only) (taxable)']"
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

elements = driver.find_elements(By.XPATH, xpath)

for i in range(len(elements)):
    elem = elements[i]

    # elem.find_element(By.XPATH, "//span[@class='screen-reader-only']") # doesn't work
    # children = elem.find_elements(By.XPATH, ".//small[text()='Attendees (1)']") # doesn't work
    # text = getText(children[0])
    # print (text)

    try:
        # xpath ..// find from its parent node
        elem.find_element(By.XPATH, "..//span[@class='screen-reader-only']") 
        print("Skip the expense. Attendee is already added.")
    except NoSuchElementException:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(elem))
        elem.click()

        time.sleep(1)

        xpath="//li[@class='form-header__list-item']"
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        xpath="//*[text()='Allocate']"
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        time.sleep(1)

        try:
            xpath="//*[text() = 'Attendees (0)']"
            driver.find_element(By.XPATH, xpath)
            addAttendee()
        except NoSuchElementException:
            print("Skip the expense. Attendee is already added.")

        # Go Back to list     # it requires due to stale elements
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)

        xpath="//div[text() = 'Business Meals (Staff Only) (taxable)']"
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        elements = driver.find_elements(By.XPATH, xpath)


# driver.close()

# As per the best practices:

#     If your usecase is to validate the presence of any element you need to induce WebDriverWait setting the expected_conditions as presence_of_element_located() which is the expectation for checking that an element is present on the DOM of a page. This does not necessarily mean that the element is visible. So the effective line of code will be:
#     WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()

#     If your usecase is to extract any attribute of any element you need to induce WebDriverWait setting the expected_conditions as visibility_of_element_located(locator) which is an expectation for checking that an element is present on the DOM of a page and visible. Visibility means that the element is not only displayed but also has a height and width that is greater than 0. So in your usecase effectively the line of code will be:
#     email = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "element_css"))).get_attribute("value")

#     If your usecase is to invoke click() on any element you need to induce WebDriverWait setting the expected_conditions as element_to_be_clickable() which is an expectation for for checking an element is visible and enabled such that you can click it. So in your usecase effectively the line of code will be:
#     WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-button"))).click()

