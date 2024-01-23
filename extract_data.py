from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetimeHelper import *
from driver import *
import pandas as pd

ticker = "BBAS3"

driver = Driver()

driver.loadAlreadySavedData(ticker)

driver.initializeBrowser()
if driver.dividendsNeedToBeUpdated(ticker):
    driver.updateDividends(ticker)

    
driver.updateDividendsDatePrice(ticker)