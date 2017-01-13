xrange = range

def solution(S):
    max_sum = 0
    current_sum = 0
    positive = False
    n = len(S)
    for i in xrange(n):
        item = S[i]
        if item < 0:
            if max_sum < current_sum:
                max_sum = current_sum
            current_sum = 0
            #print('<', max_sum, current_sum, positive, i)
        else:
            positive = True
            current_sum += item
    if (current_sum > max_sum):
        max_sum = current_sum
    if (positive):
        return max_sum
    return -1

def is_sorted(a):
    for i in xrange(1, len(a)):
        if a[i-1] > a[i]:
            return False
    return True

def solution3(A):
    if is_sorted(A):
        return True
    n = len(A)
    for i in xrange(n):
        for j in xrange(i+1, n):
            A[i], A[j] = A[j], A[i]
            if is_sorted(A):
                return True
            A[i], A[j] = A[j], A[i]
    return False

def solution1(A):
    length = 1
    index = 0
    while A[index] != -1:
        length += 1
        index = A[index]
    return length
        

print(solution([2,-1,2,-1,2]))
print(solution([1,-1,1,-1,1]))
import random
for i in range(10):
    n = random.randint(1, 10)
    l = list()
    for i in xrange(n):
        l.append(random.randint(-2, 2))
    #print(l, solution(l))

    n = random.randint(1, 10)
    l = list()
    for i in xrange(n):
        l.append(random.randint(1, 20))
    print(l, solution3(l))
