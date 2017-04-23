from currency.parse import *

def test_parse_value():
    assert(get_first_value("две тысячи чего-то".split(" "))[0] == 2000)
    assert(get_first_value("три чего-то".split(" "))[0] == 3)
    assert(get_first_value("три миллиона чего-то".split(" "))[0] == 3000000)
    assert(get_first_value("миллиона чего-то".split(" "))[0] == 1000000)
    assert(get_first_value("шести миллиона восемнадцати тысяч чего-то".split(" "))[0] == 6018000)

def test_currency():
    assert(get_currency("USD".split(" ")) == "USD")
    assert(get_currency("PHP".split(" ")) == "PHP")
    assert(get_currency("рубль".split(" ")) == "RUB")
    assert(get_currency("Шведская крона ".split(" ")) == "SEK")
    assert(get_currency("Японская йена".split(" ")) == "JPY")
    assert(get_currency(" йена".split(" ")) == "JPY")
    assert(get_currency(" юань ".split(" ")) == "CNY")
    assert(get_currency(" реал ".split(" ")) == "BRL")

def test_parse_value_and_currencies():
    v, f, t = parse_value_and_currencies("два доллара в рубли")
    assert(v == 2)
    assert(f == "USD")
    assert(t == "RUB")

    tests = {
            " 30  йена  в  юань " : "30.0 JPY CNY",
            "1 доллар в рублях": "1.0 USD RUB",
            "три чешская крона в евро": "3 CZK EUR",
            "3 USD to рубли": "3.0 USD RUB",
            "две тысячи USD TO EUR": "2000 USD EUR",
            "два SEK в USD": "2 SEK USD",
            "двадцать пять миллиона сорок одна тысяча пятьдесят шесть USD to EUR": "25041056 USD EUR",
            "один доллар новой зеландии в австралийских долларах": "1 NZD AUD",
            "сто Швейцарский франк в рубль": "100 CHF RUB",
            "20 рублей в японской йена": "20.0 RUB JPY",
            "1 лев в лей": "1.0 BGN RON",
            "один Венгерский форинт to Корейский вон": "1 HUF KRW",
            "один ринггит в шекель  ": "1 MYR ILS",
            "100 рублей в долларах": "100.0 RUB USD",
            "30.145 EUR to USD": "30.145 EUR USD",
            "одиннадцать новозеландских долларов в австралийских долларах": "11 NZD AUD",
            }
    for test, answer in tests.items():
        r = "{} {} {}".format(*parse_value_and_currencies(test))
        assert(r == answer)


