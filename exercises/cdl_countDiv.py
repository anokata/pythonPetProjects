def solution(A, B, K):
    d, rem = divmod(B-A, K)
    if (not B%K and B) or (not A%K and A):
        d += 1
    return d
