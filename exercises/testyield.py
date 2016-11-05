def f(x):
    yield x
def t(x):
    while True:
        yield x
print(f(1), f(2))
print(list(f(1)))
print(t(1))
print(list(t(10))[:10])
