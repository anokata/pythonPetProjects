from currency.russian_number import *

def test_one():
    assert(russian_number_to_int(["один"]) == 1)
    assert(russian_number_to_int(["десять"]) == 10)
    assert(russian_number_to_int(["двадцать"]) == 20)
    assert(russian_number_to_int("двадцать один".split(" ")) == 21)
    assert(russian_number_to_int("двадцать два".split(" ")) == 22)
    assert(russian_number_to_int("сто два".split(" ")) == 102)
    assert(russian_number_to_int("сто тридцать два".split(" ")) == 132)
    assert(russian_number_to_int("триста тридцать два".split(" ")) == 332)
    assert(russian_number_to_int("девятьсот девяносто девять".split(" ")) == 999)
    assert(russian_number_to_int("тысяча".split(" ")) == 1000)
    assert(russian_number_to_int("тысяча один".split(" ")) == 1001)
    assert(russian_number_to_int("тысяча девять".split(" ")) == 1009)
    assert(russian_number_to_int("тысяча десять".split(" ")) == 1010)
    assert(russian_number_to_int("тысяча семнадцать".split(" ")) == 1017)
    assert(russian_number_to_int("тысяча четыреста восемдесят шесть".split(" ")) == 1486)
    assert(russian_number_to_int("два тысяча четыреста восемдесят шесть".split(" ")) == 2486)
    assert(russian_number_to_int("два тысяча".split(" ")) == 2000)
    assert(russian_number_to_int("два тысяча два".split(" ")) == 2002)
    assert(russian_number_to_int("два тысяча тридцать семь".split(" ")) == 2037)
    assert(russian_number_to_int("два тысяча шестьсот шестьдесят пять".split(" ")) == 2665)
    assert(russian_number_to_int("пятнадцать тысяча шестьсот шестьдесят пять".split(" ")) == 15665)
    assert(russian_number_to_int("семьсот пятнадцать тысяча шестьсот шестьдесят пять".split(" ")) == 715665)
    assert(russian_number_to_int("сорок миллион семьсот пятнадцать тысяча шестьсот шестьдесят пять".split(" ")) == 40715665)

