class Neuron:
    w = [] # weights

    def __init__(self, n):
        self.w = [0.0] * n
    
    def input(self, x):
        s = 0
        w = self.w
        for i in range(0, len(x)):
            s += x[i] * w[i]
        return self.F(s)


    def F(self, s):
        return s

n = Neuron(10)
print(n.w)
print(n.input([1,2,3,4,5,6,7,8,9,10]))

