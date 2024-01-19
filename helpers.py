def tryParseFloat(string):
    try:
        return float(string)
    except Exception:
        return 0
    
def cleanFloatString(string):
    return string.replace(",", ".").replace("R$", "").replace(" ", "").replace("%", "")