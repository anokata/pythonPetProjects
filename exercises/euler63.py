def number_count(x):
    return len(str(x))

def n_pow_eq_count(x, n):
    a = x ** n
    l = number_count(a)
    return l == n

def npec():
    count = 0
    n = 1000000
    pw = 30
    for i in range(1, n):
        for p in range(1, pw):
            if n_pow_eq_count(i, p):
                print(i, p, i ** p)
                count += 1
    print('count: ', count)

npec()
