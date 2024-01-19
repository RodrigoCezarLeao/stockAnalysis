import math

class Stock():
    code = ""
    currentPrice = 0
    dy = 0
    lpa = 0
    vpa = 0
    grahamIntrinsicValue = 0
    grahamIntrinsicPercent = 0

    def __str__(self):
        currentPriceStr = f"R${self.currentPrice:6.2f}"
        dyStr = f"DY: {self.dy:5.2f}%"
        lpaStr = f"LPA: {self.lpa:5.2f}"
        vpaStr = f"VPA: {self.vpa:5.2f}"

        grahamStr = f"IV: R${self.grahamIntrinsicValue:5.2f} ({'+' if self.grahamIntrinsicPercent > 0 else ''}{self.grahamIntrinsicPercent * 100:5.2f}%)"

        return f"{self.code} | {currentPriceStr} | {dyStr} | {lpaStr} | {vpaStr}\n{grahamStr}\n"
    
    def calculateGrahamIntrinsicValue(self):
        self.grahamIntrinsicValue = math.sqrt(22.5 * self.lpa * self.vpa)
        self.calculateGrahamIntrinsicPercent()
    
    def calculateGrahamIntrinsicPercent(self):
        self.grahamIntrinsicPercent = (self.grahamIntrinsicValue/self.currentPrice) - 1