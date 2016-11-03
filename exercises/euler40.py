def gen_cham_const(n):
    r = '.'
    for i in range(1,n+1):
        r += str(i)
    return r
dec = 1
const = gen_cham_const(1000001)
m = 1
print(const[1], const[2], const[12-1])
for x in range(7):
    c = const[dec]
    print(c)
    m *= int(const[ dec ])
    dec *= 10
    
print(m)
