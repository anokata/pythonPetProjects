def next(p):
    f = False
    if p == 2:
        p = 1
    while not f:
        p += 2
        f = True
        for i in range(2, p):
            if p%i == 0:
                f = False

    return p

def primeFactorization(num): 
    p = 2
    r = list()
    while num != 0:
        d, m = divmod(num, p)
        print(d, m, p)
        if m == 0:
            num = d
            r.append(p)
        elif d == 0:
           num = 0
        else:
            p = next(p)
    return r

def lcm(nums): 
  l = 1
  ns = nums[:]
  d = False
  while not d:
    m = min(ns)
    l *= m
    ns.remove(m)
    d = True
    for x in nums:
      print(x, l%x)
      if l % x != 0:
        d = False
        break
  
  return l

