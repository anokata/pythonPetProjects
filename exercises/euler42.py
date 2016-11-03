import math
fn = '/home/ksi/p042_words.txt'
abc = {chr(c):n for (c,n) in zip(range(ord('A'), ord('Z')+1) ,range(1, ord('Z')-ord('A')+2))}
def wordNumber(w):
    n = 0
    for c in w:
        n += abc[c]
    return n

def getn(x):
    d = math.sqrt(8*x+1)
    x1 = (-1+d)/2
    x2 = (-1-d)/2
    return (x1, x2)

def isTriangleNum(x):
    x1, x2 = getn(x)
    return x1.is_integer() and x2.is_integer()

#print(list(filter(isTriangleNum, range(100))))
#print(isTriangleNum(1))

with open(fn, 'rt') as fin:
    s = fin.readlines()
    s = s[0].strip()
    s = eval(s)
    #print(len(s))
    #print(s[0:10])
    #print(abc)
    #print(wordNumber('SKY'))
    s = list(map(wordNumber, s))
    print(s[0:10])
    sum = 0
    count = 0
    for i in s:
        if isTriangleNum(i):
            sum += i
            count += 1
    print(sum,count)

