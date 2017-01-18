
def solution(s):
    if s == '':
        return 1
    brs = list()
    opend = "([{"
    closd = {
        ')': '(',
        ']': '[',
        '}': '{',
        }
    for x in s:
        #print brs
        if x in opend:
            brs.append(x)
        else:
            if brs == []:
                return 0
            last = brs.pop()
            pair = closd[x]
            #print last, pair, x, brs
            if last != pair:
                return 0
    return 0 if brs != [] else 1
