import datetime
import itertools
import requests
import pymorphy2
from .russian_number import russian_number_to_int
from .currency_data import *
from .util import *

morph = pymorphy2.MorphAnalyzer()

main_query = "http://api.fixer.io/latest?base=" + main_currency
pair_query = "http://api.fixer.io/latest?symbols={0},{1}&base={0}"
history_query = "http://api.fixer.io/{}?base={}"

class ParseError(Exception):
    pass

# Loads table data with values and growth sing, real names in dict
# also return current data as string
def load_currency_table():
    res = requests.get(main_query)
    data = res.json()

    date = data["date"]
    last_date = previous_day(date)

    history_link = history_query.format(last_date, main_currency)
    history_rates = requests.get(history_link).json()["rates"]

    table = fill_table(data["rates"], history_rates)

    date_str = datetime.datetime.strptime(date, "%Y-%m-%d").date().strftime("%d %B %Y")

    return table, date_str

# Parses query string to number and currency pair
# and transfer from one to another
def calculate_query(query):
    try:
        words = normalize_words(query.split(" "))
        value_from, words = get_first_value(words)
        currency_from, words = get_from_currency(words)
        currency_to = get_currency(words)
        value = calc_currency_from_to(currency_from, currency_to, value_from)
        value = round(value, 4)
        query += "<BR> FROM {} {} TO {} = {}".format(value_from, currency_from,
                currency_to, value)
        print(query)
        return ("{}".format(value), 
                "{} {} = {} {}".format(value_from, currency_from, value, currency_to))
    except Exception as e:
        return "err", "Query error: " + str(e)

# Fills table with values and names and growth sign relative to previous value
def fill_table(rates, history_rates):
    table = dict()
    for name, value in rates.items():
        growth_symbol = get_growth_symbol(value - history_rates[name])
        table[name] = {
                "display_name": currency_names[name],
                "name": name,
                "value": round(1 / value, 4),
                "growth": growth_symbol,
                }
    return table

def calc_currency_from_to(currency_from, currency_to, amount):
    return amount * load_pair_rate(currency_from, currency_to)

## queries funcs
@log
def load_pair_rate(currency_from, currency_to):
    return requests.get(pair_query.format(currency_from,
        currency_to)).json()["rates"][currency_to]

#util
def previous_day(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date = date - datetime.timedelta(days=1)
    return date.strftime("%Y-%m-%d")


##parsing
@log
def get_first_value(words): 
    try:
        value_from = float(words[0])
        return value_from, words[1:]
    except:
        #first word is not number it is ok, try to translate from words
        pass

    number_words = list(itertools.takewhile(is_num_word, words))
    end = len(number_words)
    if end == 0:
        raise ParseError("Can't find number in " + str(words))

    number_words = normalize_words(number_words)
    n = russian_number_to_int(number_words)
    return n, words[end:]

@log
def get_currency(words):
    if words[0].upper() in code_to_name:
        return words[0].upper()

    currency = " ".join(words).lower()
    if currency not in name_to_code:
        raise ParseError("Can't parse currency in '{}'".format(" ".join(words)))
    return name_to_code[currency]


def get_from_currency(words):
    delimeters = ["to", "в", "in", "перевести"]

    currency = list(itertools.takewhile(lambda x: x not in delimeters, words))
    end = len(currency)

    currency = get_currency(currency)
    return (currency, words[end + 1:])

def is_num_word(word):
    if normalize_word(word) in ["тысяча", "миллион", "один", "миллиард"]:
        return True
    for result in morph.parse(word):
        if result.tag.POS == "NUMR":
            return True
    return False

def normalize_word(word):
    return morph.parse(word.lower())[0].normal_form

@log
def normalize_words(words):
    return list(filter(lambda x: x != '', map(str.strip, map(normalize_word, words))))


## Testing
def test():
    print(load_pair_rate("RUB", "USD")) 
    print(calculate_query("двадцать пять миллиона сорок одна тысяча пятьдесят шесть USD to EUR"))
