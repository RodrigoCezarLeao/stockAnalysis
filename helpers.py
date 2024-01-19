from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def tryParseFloat(string):
    try:
        return float(string)
    except Exception:
        return 0
    
def cleanFloatString(string):
    return string.replace(",", ".").replace("R$", "").replace(" ", "").replace("%", "")


def findElementSelenium(driver, type, selector, stockName):
    cont = 0
    while(cont < 10):
        try:
            result = driver.find_elements(type, selector["tag"])[selector["i"]]
            driver.delete_all_cookies()
            return result
        except:
            print(f"{stockName} | Elemento ainda não carregado na tela... tentativa ({cont+1}/10)")
            sleep(10)
            cont += 1
            

def sortStocksToBuy(stockList):
    return stockList.sort(key=lambda x: x.grahamIntrinsicPercent, reverse=True)


def saveFile(txt):
    fp = open("report.txt", "w")
    fp.write(txt)
    fp.close()