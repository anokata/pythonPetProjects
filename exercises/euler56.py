def sumdigits(x):
    s = 0
    for d in str(x):
        s += int(d)
    return s

m = int()
for a in range(1, 101):
    for b in range(1, 101):
        c = a ** b
        s = sumdigits(c)
        if m < s:
            m = s
print(m)
