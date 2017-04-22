#TODO
quantitives = {
        "миллион": 1000000,
        }

def russian_number_to_int(words):
    n = 0
    for word in words:
        n += get_value(word)
    return n

def is_quantitive(word):
    return word in quantitives

def get_quantitive(word):
    return quantitives[word]

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

if __name__=='__main__':
    print(russian_number_to_int("триста сорок один".split(' ')))
