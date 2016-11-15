def inplace_reverse(s):
    s = list(s)
    for i in range(len(s)//2):
        s[i], s[len(s)-i-1] = s[len(s)-i-1], s[i]
    return ''.join(s)
#print(inplace_reverse("13"))

def grad_hour_min(h, m):
    one_hour_grad = 360 / 12
    min_grad = 6 * m
    hour_grad = one_hour_grad * h

    one_min_hour = one_hour_grad / 60
    # (360/12/60)*m
    add_hour = one_min_hour * m
    hour_grad_m = hour_grad + add_hour
    gr = min_grad - hour_grad_m
    return abs(gr)

print(grad_hour_min(3, 15))
print(grad_hour_min(10, 47))
