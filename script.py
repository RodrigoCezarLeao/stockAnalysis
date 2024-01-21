from helpers import *
from stock import Stock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#from _myToken import apiToken
import requests


stocksToAnalyze = ["SAPR4", "SANB3", "KLBN4", "GOAU4", "VALE3", "BBAS3", "WEGE3", "EGIE3"]

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
    "SI_currentPrice": {
        "tag": "//*[@id='cards-ticker']/div[1]/div[2]/div/span",
        "i": 0
    },
    "SI_balance12M": {
        "tag": "//*[@id='cards-ticker']/div[2]/div[2]/div/span",
        "i": 0
    },
    "SI_dy": {
        "tag": "//*[@id='cards-ticker']/div[5]/div[2]/span",
        "i": 0
    },
    "SI_vpa": {
        "tag": "//*[@id='table-indicators']/div[17]/div[1]/span",
        "i": 0
    },
    "SI_lpa": {
        "tag": "//*[@id='table-indicators']/div[18]/div[1]/span",
        "i": 0
    },
    "SI_dividends": {
        "tag": "//*[@id='table-dividends-history']",
        "i": 0
    },
}

urls = {
    "currentPrice": "https://www.google.com/finance/quote/@stock:BVMF",
    "fundamentInfo": "https://www.dadosdemercado.com.br/bolsa/acoes/@stock",
    "brapi": "https://brapi.dev/api/quote/@stock?token=@token",
    "yahooFinances": "https://br.financas.yahoo.com/quote/@stock.SA/key-statistics?p=@stock.SA",
    "statusInvest": "https://investidor10.com.br/acoes/@stock/",
}

results = []

options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--disable-cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = webdriver.Chrome(options=options)

for stockName in stocksToAnalyze:
    stock = Stock()
    stock.code = stockName
    

    print("-----------------------------")
    print(f"{stockName} | Buscando dados (Investidor 10)...")
        
    driver.get(urls["statusInvest"].replace("@stock", stockName))
    

    #[x for x in driver.find_elements(By.XPATH, XPATHS["SI_dividends"]["tag"])[0].text.split("\n") if "2023" in x.split(' ')[2]]
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