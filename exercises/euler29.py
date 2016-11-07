ab = set()
n = 100
for a in range(2,n+1):
    for b in range(2, n+1):
        ab |= {a**b}
print(len(ab))
