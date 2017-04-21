import datetime
import requests

currency_names = {"USD":"Доллар США", 
        "RUB": "Рубль",
        "EUR": "Евро", 
        "CAD": "Канадский доллар",
        "CHF": "Швейцарский франк",
        "CZK": "Чешская крона", 
        "DKK": "Датская крона",
        "GBP": "Фунт стерлингов",
        "NOK": "Норвежская крона", 
        "SEK": "",
        "HUF": "",
        "NZD": "",
        "MYR": "",
        "PHP": "",
        "CNY": "",
        "ILS": "",
        "ZAR": "",
        "RON": "",
        "IDR": "",
        "SGD": "",
        "KRW": "",
        "PLN": "",
        "BRL": "",
        "TRY": "",
        "BGN": "",
        "MXN": "",
        "THB": "",
        "HRK": "",
        "HKD": "",
        "INR": "",
        "JPY": "Японская Йена",
        "AUD": "",
        "CAD": "",}

main_currency = "RUB"

main_query = "http://api.fixer.io/latest?base=" + main_currency

# Load table data with values and growth sing, real names in dict
# also return current data as string
def load_currency_table():
    #try
    res = requests.get(main_query)
    data = res.json()

    date = data["date"]
    last_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    last_date = last_date - datetime.timedelta(days=1)
    last_date = last_date.strftime("%Y-%m-%d")

    history_query = "http://api.fixer.io/{}?base={}".format(last_date, main_currency)
    history_rates = requests.get(history_query).json()["rates"]

    rates = data["rates"]
    table = fill_table(rates, history_rates)

    return table, date

# Fills table with values and names and growth sign relative to previous value
def fill_table(rates, history_rates):
    table = dict()
    for name, value in rates.items():
        growth_symbol = get_growth_symbol(value - history_rates[name])
        table[name] = {
                "display_name": currency_names[name],
                "name": name,
                "value": value,
                "growth": growth_symbol,
                }
    return table

def get_growth_symbol(difference):
        if difference > 0:
            return "+"
        elif difference < 0:
            return "-"
        else:
            return "0"

