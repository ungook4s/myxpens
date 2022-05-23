# from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def waitXpath(driver, timeout):
    def myWaitXpath(label, target):
        print(label)
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, target)))
    return myWaitXpath

def sendKeys(driver, timeout):
    def mySendKeys(label, target, value):
        print(label)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, target))).send_keys(value)
    return mySendKeys

def clickCss(driver, timeout):
    def myClickCss(label, target):
        print(label)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, target))).click()
    return myClickCss

def clickXpath(driver, timeout):
    def myClickXpath(label, target):
        print(label)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, target))).click()
    return myClickXpath

def sleep(driver, timeout):
    def mySleep(value):
        print(f"sleep for {value}")
        time.sleep(value)
    return mySleep