xrange = range

def to_sec(h, m, s):
    return h*60*60 + m*60 + s
    
def minuts(secs):
    m, r = divmod(secs, 60)
    if r:
        m += 1
    return m
    
def solution(S):
    s = S.split('\n')
    pay = 0
    calls = dict()
    for call in s:
        time, phone = call.split(',')
        h, m, s = time.split(':')
        h = int(h)
        m = int(m)
        s = int(s)
        sec = to_sec(h, m, s)
        if phone in calls:
            calls[phone].append(sec)
        else:
            calls[phone] = [sec]
    #print(calls)
    max_phone = ''
    max_total = 0
    for phone, secs in calls.items():
        total = sum(secs)
        #calls[phone] = total
        if max_total < total:
            max_total = total
            max_phone = phone

    for phone, secs in calls.items():
        total = sum(secs)
        if max_total == total:
            p1 = int(''.join(max_phone.split('-')))
            p2 = int(''.join(phone.split('-')))
            if p2<p1:
                max_phone = phone

    #print(calls, max_phone)
    
    for phone, secs in calls.items():
        if phone != max_phone:
            #print(secs)
            for dur in secs:
                if dur >= 300:
                    pay += minuts(dur) * 150
                else:
                    pay += dur * 3
    
    return pay
        
        
    

#assert(solution() == )
