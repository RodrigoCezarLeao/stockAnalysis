from helpers import *
from stock import Stock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#from _myToken import apiToken
import requests


stocksToAnalyze = ["SAPR4", "SANB3", "KLBN4", "GOAU4", "VALE3", "BBAS3"]

XPATHS = {    
    "googleCurrentPrice": {
        "tag": "YMlKec",
        "i": 10,
    },
    "yahooCurrentPrice": {
        "tag": "e3b14781 ",
        "i": 3,
    },
    "yahooVPA": {
        "tag": "td",
        "i": 115,
    },
    "yahooLPA": {
        "tag": "td",
        "i": 101,
    },    
}

urls = {
    "currentPrice": "https://www.google.com/finance/quote/@stock:BVMF",
    "fundamentInfo": "https://www.dadosdemercado.com.br/bolsa/acoes/@stock",
    "brapi": "https://brapi.dev/api/quote/@stock?token=@token",
    "yahooFinances": "https://br.financas.yahoo.com/quote/@stock.SA/key-statistics?p=@stock.SA"
}

results = []

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = webdriver.Chrome(options=options)

for stockName in stocksToAnalyze:
    stock = Stock()
    stock.code = stockName
    

    print("-----------------------------")
    print(f"{stockName} | Buscando dados...")
        
    driver.get(urls["currentPrice"].replace("@stock", stockName))
    

    print(f"{stockName} | Buscando preço atual...")
    elementHTML = findElementSelenium(driver, By.CLASS_NAME, XPATHS["googleCurrentPrice"], stockName)
    print(f"Valor encontrado = '{elementHTML.text}'")
    stock.currentPrice = tryParseFloat(cleanFloatString(elementHTML.text))
    
    driver.get(urls["yahooFinances"].replace("@stock", stockName))
    
    print(f"{stockName} | Buscando VPA...")
    elementHTML = findElementSelenium(driver, By.TAG_NAME, XPATHS["yahooVPA"], stockName)
    print(f"Valor encontrado = '{elementHTML.text}'")
    stock.vpa = tryParseFloat(cleanFloatString(elementHTML.text))

    print(f"{stockName} | Buscando LPA...")
    elementHTML = findElementSelenium(driver, By.TAG_NAME, XPATHS["yahooLPA"], stockName)
    print(f"Valor encontrado = '{elementHTML.text}'")
    stock.lpa = tryParseFloat(cleanFloatString(elementHTML.text))  

    print(f"{stockName} | Finalizado.")

    stock.calculateGrahamIntrinsicValue()
    
    results.append(stock)
    
    
driver.quit()

print("\n\n\n")
text = ""

sortStocksToBuy(results)
for stock in results:
    text += "-"*30 + "\n"
    text += str(stock)
    
text += "-"*30

print(text)
saveFile(text)