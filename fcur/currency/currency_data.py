
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
name_to_code["доллар новый зеландия"] = "NZD"
name_to_code["японский йена"] = "JPY"
name_to_code["чешский крон"] = "CZK"
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
