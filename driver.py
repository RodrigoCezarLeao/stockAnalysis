from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetimeHelper import *
from helpers import *
import pandas as pd
import math

class Driver():
    driver = ""
    df = pd.DataFrame()
    visible = True
    ticker = ""
    
    def __init__(self, visible=True, ticker=""):
        self.visible = visible
        self.ticker = ticker
        

    def initializeBrowser(self):
        options = webdriver.ChromeOptions()
        
        options.add_argument("--disable-cache")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        if not self.visible:
            options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)

    def browserGoTo(self, operation, args = {}):
        if operation == "GET_INDICATORS":
            URL = "https://investidor10.com.br/acoes/@ticker/"
            self.driver.get(URL.replace("@ticker", self.ticker))
        if operation == "EXTRACT_HISTORIC_PRICE_DATA":
            URL = "https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=@ticker&dtini=@date&dtfim=@date"
            self.driver.get(URL.replace("@ticker", self.ticker).replace("@date", args["date"]))

    def loadAlreadySavedData(self, ticker):
        try:
            df = pd.read_csv(f'reports/dividends_history_{ticker}_report.csv', sep=";")
            columns=["Tipo", "Data Com", "Data Com Preço", "% DCP", "Data Ex", "Data Ex Preço", "% DEP", "Valor Bruto", "Valor Real"]
            for col in columns:
                if col not in df:
                    df[col] = ""

            df = df.reset_index()
            df = df.drop(["index"], axis=1)

            self.df = df
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Tipo", "Data Com", "Data Com Preço", "% DCP", "Data Ex", "Data Ex Preço", "% DEP", "Valor Bruto", "Valor Real"])
            self.df = df
        
    def dividendsNeedToBeUpdated(self, ticker):
        # Get online info
        URL = "https://investidor10.com.br/acoes/@ticker/"
        self.driver.get(URL.replace("@ticker", ticker))
        tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-dividends-history']/tbody/tr[1]")))
        auxData = tableElem.text.split(" ")


        if (len(self.df) > 0) and (self.df.iloc[0]["Tipo"] == auxData[0]) and (self.df.iloc[0]["Data Com"] == auxData[1]) and (self.df.iloc[0]["Data Ex"] == auxData[2]) and (self.df.iloc[0]["Valor Bruto"] == auxData[3]):
            return False
        else:
            return True
        
    def updateDividends(self, ticker):
        URL = "https://investidor10.com.br/acoes/@ticker/"
        self.driver.get(URL.replace("@ticker", ticker))

        tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-dividends-history']")))
        auxData = tableElem.text.replace("Rend. Tributado", "Rend.Tributado").split("\n")
        df = pd.DataFrame([x.split(" ") for x in auxData])
        df.columns = ["Tipo", "Data Com", "Data Ex", "Valor Bruto"]

        # Convert value col to numeric
        df["Valor Bruto"] = pd.to_numeric(df["Valor Bruto"].apply(convert))

        # Fill real value col
        df["Valor Real"] = pd.concat([df[df["Tipo"] != "Dividendos"]["Valor Bruto"] * 0.85, df[df["Tipo"] == "Dividendos"]["Valor Bruto"]])        
        

        try:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='table-dividends-history_next']"))).click()
        except:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='table-dividends-history_next']"))).click()

        navBar = self.driver.find_elements(By.XPATH, "//*[@id='table-dividends-history_paginate']/span")

        for page in range(int(navBar[0].text.split("\n")[-1]) - 1) :
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-dividends-history']")))
            auxData = tableElem.text.replace("Rend. Tributado", "Rend.Tributado").split("\n")
            df2 = pd.DataFrame([x.split(" ") for x in auxData])
            df2.columns = ["Tipo", "Data Com", "Data Ex", "Valor Bruto"]

            # Convert value col to numeric
            df2["Valor Bruto"] = pd.to_numeric(df2["Valor Bruto"].apply(convert))

            # Fill real value col
            df2["Valor Real"] = pd.concat([df2[df2["Tipo"] != "Dividendos"]["Valor Bruto"] * 0.85, df2[df2["Tipo"] == "Dividendos"]["Valor Bruto"]])

            df = pd.concat([df, df2])

            self.driver.find_element(By.XPATH, "//*[@id='table-dividends-history_next']").click()


        df = df.reset_index()
        df = df.drop(["index"], axis=1)
        df["Valor Bruto"] = df["Valor Bruto"].apply(roundFloat)
        df["Valor Real"] = df["Valor Real"].apply(roundFloat)
        self.df = df
    
    def updateDividendsDatePrice(self, ticker):
        try:
            if "Data Com Preço" not in self.df:
                self.df["Data Com Preço"] = ""
            if "Data Ex Preço" not in self.df:
                self.df["Data Ex Preço"] = ""
            if "% DCP" not in self.df:
                self.df["% DCP"] = ""
            if "% DEP" not in self.df:
                self.df["% DEP"] = ""
            

            for index, row in self.df.iterrows():
                if row["Data Com Preço"] == "" or "float" in str(type(row["Data Com Preço"])):                    
                    URL = "https://www.ibovx.com.br/historico-papeis-bovespa.aspx?papel=@ticker&dtini=@date&dtfim=@date"
                    
                    for col in ["Data Com", "Data Ex"]:
                        print(f"Buscando cotação de {ticker} na data {row[col]}...")

                        if convertStrToDate(row[col]) > datetime.now():
                            continue

                        if convertStrToDate(row[col]) < datetime(2000,1,1):
                            continue

                        # Checar se essa cotação já foi buscada antes
                        if len(self.df[self.df[col] == row[col]]) > 0 and self.df[self.df[col] == row[col]][col + " Preço"].iloc[0] != "":
                            dayEndPrice = self.df[self.df[col] == row[col]][col + " Preço"].iloc[0]
                        else:
                            self.driver.get(URL.replace("@ticker", ticker).replace("@date", row[col]))

                            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='idConteudo']/div/div[9]/table")))
                            tableContent = tableElem.text.split("\n")[1:]
                            tableContentDividend = [x.split(" ") for x in tableContent]

                            lineRow = [x for x in tableContentDividend if x[0] == row[col]]

                            if len(lineRow) == 0:
                                lineRow = [x for x in tableContentDividend if x[0][3:] == row[col][3:] ]

                            if len(lineRow) == 0:
                                lineRow = tableContentDividend[0]

                            #dayEndPrice = lineRow[0][3]
                            dayEndPrice = float(lineRow[0][3].replace(",", "."))


                        row[col + " Preço"] = dayEndPrice

                        aux = col.split(" ")[1][0]
                        auxLabel = f"% D{aux}P"

                        row[auxLabel] = roundFloat((row['Valor Real'] / dayEndPrice) * 100)
                        

                    self.df.loc[row.name] = row
                    
            self.df.to_csv(f"reports/dividends_history_{ticker}_report.csv", index=False, sep=";")
        except:    
            self.df.to_csv(f"reports/dividends_history_{ticker}_report.csv", index=False, sep=";")
        
    def getIndicators(self, indicatorsList = []):
        self.browserGoTo("GET_INDICATORS")
        result = {}

        if "VPA" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators']/div[17]/div[1]/span")))
            result["VPA"] = tryParseFloat(tableElem.text)

        if "LPA" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators']/div[18]/div[1]/span")))
            result["LPA"] = tryParseFloat(tableElem.text)

        if "MARKET_VALUE" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators-company']/div[1]/span[2]/div[1]")))
            result["MARKET_VALUE"] = tryParseFloat(tableElem.text)

        if "STOCK_AMOUNT" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators-company']/div[4]/span[2]/div[1]")))
            result["STOCK_AMOUNT"] = tryParseFloat(tableElem.text)

        if "FREE_FLOAT" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators-company']/div[11]/span[2]")))
            result["FREE_FLOAT"] = tryParseFloat(tableElem.text)

        if "TAG_ALONG" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators-company']/div[12]/span[2]")))
            result["TAG_ALONG"] = tryParseFloat(tableElem.text)

        if "DAILY_LIQUIDITY_AVG" in indicatorsList:
            tableElem = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='table-indicators-company']/div[13]/span[2]/div[1]")))
            result["DAILY_LIQUIDITY_AVG"] = tryParseFloat(tableElem.text)

        


        return result

