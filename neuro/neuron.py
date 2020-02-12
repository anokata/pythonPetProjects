class Neuron:
    w = [] # weights
    
    def input(x):
        s = 0
        for i in range(0, len(x)):
            s += x[i] * w[i]
        return F(s)


    def F(s):
        return s

n = Neuron()

