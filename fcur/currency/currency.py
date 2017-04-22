import datetime
import requests
import pymorphy2
from .russian_number import russian_number_to_int

morph = pymorphy2.MorphAnalyzer()

def normalize_word(word):
    return morph.parse(word.lower())[0].normal_form

def normalize_words(words):
    return list(map(normalize_word, words))


currency_names = {"USD":"Доллар США", 
        "CAD": "Канадский доллар",
        "NZD": "Новозеландский доллар",
        "SGD": "Сингапурский Доллар",
        "HKD": "Гонконгский доллар",
        "AUD": "Австралийский доллар", 
        "CZK": "Чешская крона", 
        "DKK": "Датская крона",
        "NOK": "Норвежская крона", 
        "SEK": "Шведская крона",
        "IDR": "Индонезийская рупия",
        "INR": "Индийская рупия",
        "PHP": "Филиппинское песо",
        "MXN": "Мексиканское песо",
        "RUB": "Рубль",
        "EUR": "Евро", 
        "CHF": "Швейцарский франк",
        "GBP": "Фунт стерлингов",
        "HUF": "Венгерский форинт",
        "MYR": "Малайзийский ринггит",
        "CNY": "Китайский Юань",
        "ILS": "Израильский Новый Шекель",
        "ZAR": "Южноафриканский рэнд",
        "RON": "Румынский лей",
        "KRW": "Корейский вон",
        "PLN": "Польский злотый",
        "BRL": "Бразильский реал",
        "TRY": "Турецкая лира",
        "BGN": "Болгарский лев",
        "THB": "Тайландский бат",
        "HRK": "Хорватская куна",
        "JPY": "Японская йена",
        }

name_to_code = {name.lower(): code for code, name in currency_names.items()}
name_to_code["доллар"] = "USD"
name_to_code["японский йена"] = "JPY"
name_to_code["йена"] = "JPY"
name_to_code["евро"] = "EUR"
name_to_code["франк"] = "CHF"
name_to_code["фунт"] = "GBP"
name_to_code["форинт"] = "HUF"
name_to_code["ринггит"] = "MYR"
name_to_code["юань"] = "CNY"
name_to_code["шекель"] = "ILS"
name_to_code["рэнд"] = "ZAR"
name_to_code["лей"] = "RON"
name_to_code["вон"] = "KRW"
name_to_code["злотый"] = "PLN"
name_to_code["реал"] = "BRL"
name_to_code["лира"] = "TRY"
name_to_code["лев"] = "BGN"
name_to_code["бат"] = "THB"
name_to_code["куна"] = "HRK"

code_to_name = {code : name.lower() for code, name in currency_names.items()}

main_currency = "RUB"

main_query = "http://api.fixer.io/latest?base=" + main_currency
pair_query = "http://api.fixer.io/latest?symbols={0},{1}&base={0}"

def load_pair_rate(currency_from, currency_to):
    return requests.get(pair_query.format(currency_from,
        currency_to)).json()["rates"][currency_to]

#print(load_pair_rate("RUB", "USD")) # TODO Test

def previous_day(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date = date - datetime.timedelta(days=1)
    return date.strftime("%Y-%m-%d")


# Load table data with values and growth sing, real names in dict
# also return current data as string
def load_currency_table():
    #try
    res = requests.get(main_query)
    data = res.json()

    date = data["date"]
    last_date = previous_day(date)

    history_query = "http://api.fixer.io/{}?base={}".format(last_date, main_currency)
    history_rates = requests.get(history_query).json()["rates"]

    rates = data["rates"]
    table = fill_table(rates, history_rates)

    date_str = datetime.datetime.strptime(date, "%Y-%m-%d").date().strftime("%d %B %Y")

    return table, date_str

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

def is_num_word(word):
    return morph.parse(word)[0].tag.POS == "NUMR"

def get_first_value(words): #TODO number in words
    if words[0].isdigit(): #TODO Float
        value_from = int(words[0])
        return value_from, words[end:]

    end = 0
    number_words = list()
    while is_num_word(words[end]):
        number_words.append(words[end])
        end += 1

    number_words = normalize_words(number_words)
    n = russian_number_to_int(number_words)
    return n, words[end:]

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
    value_from, words = get_first_value(words)
    currency_from, words = get_from_currency(words)
    currency_to = get_currency(words)
    value = calc_currency_from_to(currency_from, currency_to, value_from)
    value = round(value, 4)
    query += "<BR> FROM {} {} TO {} = {}".format(value_from, currency_from,
            currency_to, value)
    print(query)
    #return "", "Не понимаю"
    return ("{}".format(value), 
            "{} {} = {} {}".format(value_from, currency_from, value, currency_to))

