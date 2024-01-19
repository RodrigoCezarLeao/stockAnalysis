from helpers import *
from stock import Stock
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


stocksToAnalyze = ["GOAU4", "VALE3", "BBAS3", "SAPR4", "SANB3", "KLBN4"]

XPATHS = {
    "googleCurrentStockPrice": "fxKbKc",
    "googleDividendYield": "P6K39c",
    "lpa": "/html/body/div[3]/div/div[3]/div[1]/span[2]",
    "vpa": "/html/body/div[3]/div/div[3]/div[2]/span[2]"
}

urls = {
    "currentPrice": "https://www.google.com/finance/quote/@stock:BVMF",
    "fundamentInfo": "https://www.dadosdemercado.com.br/bolsa/acoes/@stock"
}

results = []

navegador = webdriver.Chrome()

for stockName in stocksToAnalyze:
    stock = Stock()
    stock.code = stockName

    navegador.get(urls["fundamentInfo"].replace("@stock", stockName))

    elementHTML = navegador.find_element(By.XPATH, XPATHS["lpa"])
    stock.lpa = tryParseFloat(cleanFloatString(elementHTML.text))

    elementHTML = navegador.find_element(By.XPATH, XPATHS["vpa"])
    stock.vpa = tryParseFloat(cleanFloatString(elementHTML.text))

    navegador.get(urls["currentPrice"].replace("@stock", stockName))

    elementHTML = navegador.find_element(By.CLASS_NAME, XPATHS["googleCurrentStockPrice"])
    stock.currentPrice = tryParseFloat(cleanFloatString(elementHTML.text))

    elementHTML = navegador.find_elements(By.CLASS_NAME, XPATHS["googleDividendYield"])[6]
    stock.dy = tryParseFloat(cleanFloatString(elementHTML.text))

    results.append(stock)
    print(stock)
    
    

print()