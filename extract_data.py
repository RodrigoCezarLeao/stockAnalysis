from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep

#URL = "https://vale.com/pt/dividendos-dividas-e-debentures"
URL = "https://investidor10.com.br/acoes/@ticker/"
ticker = "SANB3"


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--disable-cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = webdriver.Chrome(options=options)

driver.get(URL.replace("@ticker", ticker))

tableElem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-dividends-history']")))
auxData = tableElem.text.split("\n")
df = pd.DataFrame([x.split(" ") for x in auxData])
df.columns = ["Tipo", "Data Com", "Data Ex", "Valor"]

try:
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='table-dividends-history_next']"))).click()
except:
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='table-dividends-history_next']"))).click()

navBar = driver.find_elements(By.XPATH, "//*[@id='table-dividends-history_paginate']/span")

for page in range(len(navBar[0].text.split("\n")) - 1) :
    tableElem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-dividends-history']")))
    auxData = tableElem.text.split("\n")
    df2 = pd.DataFrame([x.split(" ") for x in auxData])
    df2.columns = ["Tipo", "Data Com", "Data Ex", "Valor"]

    df = pd.concat([df, df2])

    driver.find_element(By.XPATH, "//*[@id='table-dividends-history_next']").click()

df.to_csv(f"dividends_history_{ticker}_report.csv", index=False, sep=";")