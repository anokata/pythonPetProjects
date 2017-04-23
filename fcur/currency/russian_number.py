from .util import log

QUANTITIVES = {
    "миллион": 1000000,
    "тысяча": 1000,
    "миллиард": 1000000000,
}

class NumberParseError(Exception):
    pass

@log
def russian_number_to_int(words):
    try:
        current_number = 0
        total = 0
        for word in words:
            if word in QUANTITIVES:
                if current_number != 0:
                    total += current_number * QUANTITIVES[word]
                else:
                    total += QUANTITIVES[word]

                current_number = 0
            else:
                current_number += get_value(word)
        total += current_number
        return total
    except:
        raise NumberParseError("can't parse number: " + str(words))

def is_quantitive(word):
    return word in QUANTITIVES

def get_quantitive(word):
    return QUANTITIVES[word]

def get_value(word):
    numbers = {
        "один": 1,
        "два": 2,
        "три": 3,
        "четыре": 4,
        "пять": 5,
        "шесть": 6,
        "семь": 7,
        "восем": 8,
        "девять": 9,
        "десять": 10,
        "одиннадцать": 11,
        "двенадцать": 12,
        "тринадцать": 13,
        "четырнадцать": 14,
        "пятнадцать": 15,
        "шестнадцать": 16,
        "семнадцать": 17,
        "восемнадцать": 18,
        "девятнадцать": 19,
        "двадцать": 20,
        "тридцать": 30,
        "сорок": 40,
        "пятьдесят": 50,
        "шестьдесят": 60,
        "семьдесят": 70,
        "восемдесят": 80,
        "девяносто": 90,
        "сто": 100,
        "двести": 200,
        "триста": 300,
        "четыреста": 400,
        "пятьсот": 500,
        "шестьсот": 600,
        "семьсот": 700,
        "восемьсот": 800,
        "девятьсот": 900,
        "тысяча": 1000,
    }
    if word in numbers:
        return numbers[word]
    else:
        raise Exception("(!>>>) can't parse number")

