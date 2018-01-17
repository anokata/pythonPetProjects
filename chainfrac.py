import math

c = [1,2,2,2]

def calc_chain(chain):
    def r(c, n):
        return 1/c[n]
    s = c[0]
    for i in range(1, len(chain)):
        s += 1/r(chain, i)
    return s

def calc_chain_f(prodF, n):
    pass

print(calc_chain(c))
print(math.sqrt(2))
