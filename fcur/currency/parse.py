import itertools
import pymorphy2
from .russian_number import russian_number_to_int
from .currency_data import *
from .util import *

morph = pymorphy2.MorphAnalyzer()

class ParseError(Exception):
    pass

# Extracts from query string value and translate currency to codes
def parse_value_and_currencies(query):
    words = normalize_words(query.split(" "))
    value_from, words = get_first_value(words)
    currency_from, words = get_from_currency(words)
    currency_to = get_currency(words)
    return value_from, currency_from, currency_to


@log
def get_first_value(words): 
    try:
        value_from = float(words[0])
        return value_from, words[1:]
    except ValueError:
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


