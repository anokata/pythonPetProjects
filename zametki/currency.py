import requests as req
currency_url = 'http://api.fixer.io/latest?symbols=RUB&base={}'
def request_pair(base):
    res = req.get(currency_url.format(base))
    try:
        res = res.json()
    except:
        return 0
    return res['rates']['RUB']

def get_EUR_RUB():
    return request_pair('EUR')


def get_USD_RUB():
    return request_pair('USD')

if __name__=='__main__':
    print(get_USD_RUB())
    print(get_EUR_RUB())

