import ast

def a(x):
    print(x*2)
    y = [x*2 for x in list(str(x))]
    def b(z):
        print("some bizard")

    class C():
        pass
    return y
