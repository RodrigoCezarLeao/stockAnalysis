from datetime import datetime

def convertStrToDate(dateStr):
    return datetime.strptime(dateStr, '%d/%m/%Y')

def convertStrToTick(dateStr):
    return convertStrToDate(dateStr).timestamp()

def convertDateToStr(date):
    return datetime.strftime(date, '%d/%m/%Y')

def convertDateToTick(date):
    return date.timestamp()

def convertTickToDate(tickInt):
    return datetime.fromtimestamp(tickInt)

def convertTickToStr(tickInt):
    return datetime.strftime(datetime.fromtimestamp(tickInt), '%d/%m/%Y')
