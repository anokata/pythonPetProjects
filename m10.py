def a_kv(n):
    return n*n*(-1)**n

def sumkv(n):
   return sum(map(a_kv, range(1, n+1))) 

def mysum(n):
    if (n % 2) == 0:
        k = n / 2
        print(2*k*k+k)
    else:
        k = (n+1) / 2
        print(-2*k*k+k)

print(sumkv(1))
print(sumkv(2))
print(sumkv(3))
print(sumkv(4))
mysum(1)
mysum(2)
mysum(3)
mysum(4)
