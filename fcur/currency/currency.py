import requests
from .util import previous_day, get_growth_symbol, log, date_format
from .parse import parse_value_and_currencies, ParseError
from .currency_data import main_currency, currency_names

MAIN_QUERY = "http://api.fixer.io/latest?base=" + main_currency
PAIR_QUERY = "http://api.fixer.io/latest?symbols={0},{1}&base={0}"
HISTORY_QUERY = "http://api.fixer.io/{}?base={}"


# Loads table data with values and growth sing, real names in dict
# also return current data as string
def load_currency_table():
    res = requests.get(MAIN_QUERY)
    data = res.json()

    date = data["date"]
    last_date = previous_day(date)

    history_link = HISTORY_QUERY.format(last_date, main_currency)
    history_rates = requests.get(history_link).json()["rates"]

    table = fill_table(data["rates"], history_rates)

    return table, date_format(date)

# Parses query string to number and currency pair
# and transfer from one to another
def calculate_query(query):
    try:
        value_from, currency_from, currency_to = parse_value_and_currencies(query)
        value = calc_currency_from_to(currency_from, currency_to, value_from)
        value = round(value, 4)
        query += "FROM {} {} TO {} = {}".format(value_from,
                                                currency_from,
                                                currency_to,
                                                value)
        print(query)
        return ("{}".format(value),
                "{} {} = {} {}".format(value_from, currency_from, value, currency_to))
    except ParseError as exception:
        return "err", "Query error: " + str(exception)

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

# Translates specific amount of currency from one ot another base
def calc_currency_from_to(currency_from, currency_to, amount):
    return amount * load_pair_rate(currency_from, currency_to)

# Loads rate for one pair of currency in destination base
@log
def load_pair_rate(currency_from, currency_to):
    return requests.get(PAIR_QUERY.format(currency_from,
                                          currency_to)).json()["rates"][currency_to]

