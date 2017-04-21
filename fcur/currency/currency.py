import datetime
import requests
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def normalize_word(word):
    return morph.parse(word.lower())[0].normal_form

def normalize_words(words):
    return list(map(normalize_word, words))


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
        "AUD": "", }

name_to_code = {name.lower(): code for code, name in currency_names.items()}
name_to_code["доллар"] = "USD"
name_to_code["японский йена"] = "JPY"
code_to_name = {code : name.lower() for code, name in currency_names.items()}

main_currency = "RUB"

main_query = "http://api.fixer.io/latest?base=" + main_currency
pair_query = "http://api.fixer.io/latest?symbols={0},{1}&base={0}"

def load_pair_rate(currency_from, currency_to):
    return requests.get(pair_query.format(currency_from,
        currency_to)).json()["rates"][currency_to]

#print(load_pair_rate("RUB", "USD")) # TODO Test

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

delimeters = ["to", "в", "in", "перевести"]

#get_first_value TODO number in words

def calc_currency_from_to(currency_from, currency_to, amount):
    return amount * load_pair_rate(currency_from, currency_to)

def get_currency(words):
    if words[0].upper() in code_to_name:
        return words[0].upper()

    currency = " ".join(words).lower()
    if currency not in name_to_code:
        return None # TODO Exception
    return name_to_code[currency]


def get_from_currency(words):
    currency = list()
    end = 0

    for word in words:
        if word in delimeters:
            break
        currency.append(word)
        end += 1

    currency = get_currency(currency)
    return (currency, words[end + 1:])

def calculate_query(query):
    words = normalize_words(query.split(" "))
    if words[0].isdigit(): #TODO Float
        value_from = int(words[0])
        currency_from, words = get_from_currency(words[1:])
        currency_to = get_currency(words)
        value = calc_currency_from_to(currency_from, currency_to, value_from)
        value = round(value, 4)
        query += "<BR> FROM {} {} TO {} = {}".format(value_from, currency_from,
                currency_to, value)
        print(query)
    else:
        return "Не понимаю"
    return ("{}".format(value), 
            "{} {} = {} {}".format(value_from, currency_from, value, currency_to))
