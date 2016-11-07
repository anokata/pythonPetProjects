from collections import defaultdict
d = defaultdict(int)
with open('/home/ksi/pyurl2.txt', 'rt') as fin:
    for l in fin:
        for c in l:
            d[c] += 1
t = list()
for k, v in d.items():
    if v == 1:
        t.append(k)

msg = ''
with open('/home/ksi/pyurl2.txt', 'rt') as fin:
    for l in fin:
        for c in l:
            if c in t:
                msg += c
print(msg)
