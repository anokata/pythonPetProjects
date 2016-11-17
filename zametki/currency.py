import requests as req

def getUSD_RUB():
    currency_url = 'http://api.fixer.io/latest?symbols=RUB&base=USD'
    res = req.get(currency_url).json()
    return res['rates']['RUB']

#print(getUSD_RUB())

