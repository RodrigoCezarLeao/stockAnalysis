import math

class Stock():
    code = ""
    currentPrice = 0
    dy = 0
    lpa = 0
    vpa = 0

    def __str__(self):
        currentPriceStr = f"R${self.currentPrice:6.2f}"
        dyStr = f"DY: {self.dy:5.2f}%"
        lpaStr = f"LPA: {self.lpa:5.2f}"
        vpaStr = f"VPA: {self.vpa:5.2f}"

        grahamStr = f"Intrinsic Value: R${self.grahamIntrinsicValue():5.2f}"

        return f"{self.code} | {currentPriceStr} | {dyStr} | {lpaStr} | {vpaStr}\n{grahamStr}\n"
    
    def grahamIntrinsicValue(self):
        return math.sqrt(22.5 * self.lpa * self.vpa)