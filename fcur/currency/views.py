from .app import app
from flask import render_template
import requests
import datetime

#TODO try except
#logic
currency = ["USD", "RUB", "EUR", 
        "CAD", "CHF", "CZK", 
        "DKK", "GBP", "NOK", 
        "SEK", "JPY", "AUD", "CAD"]

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
res = requests.get(main_query)
data = res.json()
date = data["date"]

last_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
last_date = last_date - datetime.timedelta(days=1)
last_date = last_date.strftime("%Y-%m-%d")

history_query = "http://api.fixer.io/{}?base={}".format(last_date, main_currency)
history_rates = requests.get(history_query).json()["rates"]

rates = data["rates"]
table = dict()
for name, value in rates.items():
    growth = value - history_rates[name]
    if growth > 0:
        growth_symbol = "+"
    elif growth < 0:
        growth_symbol = "-"
    else:
        growth_symbol = "0"

    table[name] = {
            "display_name": currency_names[name],
            "name": name,
            "value": value,
            "growth": growth_symbol,
            }
#endlogic

@app.route("/")
def root():
    ans = "n"
    return render_template("page.html", 
            ans=ans, 
            date=date, 
            rates=table)

