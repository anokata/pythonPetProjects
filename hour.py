import math

def angle(m):
    return 5.5 * m/60;

print(angle(20))

i = 0
for m in range(0,1440*60):
    a = angle(m) / 360
    d = a - math.floor(a)
    if (d < 0.00001):
        print(a, math.floor(a), d, d == 0.0)
        i += 1

print(i)

for m in range(25):
    print(360*m/5.5)
