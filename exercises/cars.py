xrange = range

def solution(a):
    n = len(a)
    pas = 0
    cur = 0
    for i in xrange(n):
        if a[i] == 0:
            cur += 1
        else:
            pas += cur 
            if pas > 1000000000:
                return -1
        #print(pas, cur, lev)
    return pas
    
    for i in xrange(n):
        if a[i] == 0:
            for k in xrange(i+1, n):
                if a[k] == 1:
                    pas += 1
                    #print(i, k, a[i], a[k])
        else:
            pass
    #print(pas)
    return pas

assert(solution([0, 1, 0, 1, 1]) == 5)
assert(solution([0]) == 0)
assert(solution([0, 0]) == 0)
assert(solution([0, 1]) == 1)
assert(solution([0, 0, 1]) == 2)
assert(solution([0, 0, 1, 0, 0]) == 2)
assert(solution([0, 0, 1, 0, 0, 1]) == 6)
assert(solution([1, 0, 1, 0, 0, 1]) == 4)
#сколько нулей перед каждой единицей?
# ищем первый 1 считая до неё 0. след искать 1 то число + число * 2
