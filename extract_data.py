from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetimeHelper import *
import pandas as pd
import math

ticker = "SANB3"


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--disable-cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = webdriver.Chrome(options=options)
"""
# Histórico de dividendos (Investidor10)
URL = "https://investidor10.com.br/acoes/@ticker/"
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

"""

df = pd.read_csv(f'reports/dividends_history_{ticker}_report.csv', sep=";")
df.columns = ["Tipo", "Data Com", "Data Ex", "Valor", "Data Com Preço", "Data Ex Preço"]
    
df = df.reset_index()
df = df.drop(["index"], axis=1)
    
if not "Data Com Preço" in df:
    df["Data Com Preço"] = ""

if not "Data Ex Preço" in df:
    df["Data Ex Preço"] = ""

# Histórico de preço (Yahoo Finanças)
try:
    for index, row in df.iterrows():
        if "Data Com Preço" in row and "float" in str(type(row["Data Com Preço"])):
            URL = "https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=@ticker&dtini=@date&dtfim=@date"
            
            for col in ["Data Com", "Data Ex"]:
                if convertStrToDate(row[col]) > datetime.now():
                    continue

                if convertStrToDate(row[col]) < datetime(2000,1,1):
                    continue

                driver.get(URL.replace("@ticker", ticker).replace("@date", row[col]))

                tableElem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='idConteudo']/div/div[9]/table")))
                tableContent = tableElem.text.split("\n")[1:]
                tableContentDividend = [x.split(" ") for x in tableContent]

                lineRow = [x for x in tableContentDividend if x[0] == row[col]]

                if len(lineRow) == 0:
                    lineRow = [x for x in tableContentDividend if x[0][3:] == row[col][3:] ]

                if len(lineRow) == 0:
                    lineRow = tableContentDividend[0]

                

                #lineRow = next(filter(lambda x: x[0] == row[col], tableContentDividend))
                dayEndPrice = lineRow[0][3]
                row[col + " Preço"] = dayEndPrice
                

            df.loc[row.name] = row
            print()
except:    
    df.to_csv(f"reports/dividends_history_{ticker}_report.csv", index=False, sep=";")

df.to_csv(f"reports/dividends_history_{ticker}_report.csv", index=False, sep=";")