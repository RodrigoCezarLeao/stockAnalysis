from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests

URL = "https://vale.com/pt/dividendos-dividas-e-debentures"



options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--disable-cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = webdriver.Chrome(options=options)

driver.get(URL)

tableElem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lnfo']/table/tbody")))

x = tableElem.text.split("\n")
y = [x[i : i+11] for i in range(len(x)//12)]

df = pd.DataFrame([x.split(" ") for x in tableElem[0].text.split("\n")] )
df.columns = ["Tipo", "Data Com", "Data Ex", "Valor"]



for page in range(len(navBar[0].text.split("\n")) - 1) :
    nextPageElem.click()
    tableElem = driver.find_elements(By.XPATH, "//*[@id='table-dividends-history']")
    
    print()