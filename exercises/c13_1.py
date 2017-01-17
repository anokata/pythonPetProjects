def solution(m, a):
    n = len(a)
    if n == 1:
        return 1
    start, end = 0, 0
    count = 0
    slice = set()
    slice.add(a[end])
    while count < 1000000000 and end != n-1:
        count += 1
        print(start, end, slice)
        end += 1
        if a[end] not in slice:
            slice.add(end)
        else:
            start += 1
            end = start
            slice = set()
            slice.add(a[end])
    return count
        
        
#print(solution(6, [1]))
#print(solution(6, [1,1]))
print(solution(6, [1,2]))
