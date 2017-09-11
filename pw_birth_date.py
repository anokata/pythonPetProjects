def pw(d, m, y):
    print("{:02d}{:02d}{}".format(d, m, y))
    print("{:02d}{:02d}{}".format(m, d, y))
    print("{}{:02d}{:02d}".format(y, m, d))

for day in range(1, 32):
    for month in range(1, 13):
        for year in range(1900, 2021):
            pw(day, month, year)
