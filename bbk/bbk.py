# symbols: letters a-z, A-Z, + ! * #
# + is disjunction
# ! is "not"
# # is tau
# * is square symbol
# #1 *1 - connections

# 1. Introducing contractile symbols
# i.e. => as +!

symcom1 = "+ab"

def is_term(s):
    return False

def is_corr(s):
    return False

def subs(let, cs, s):
    return s

class Symbol:
    s = ' '
    def __init__(self, ch):
        self.s = ch
    
    def __str__(self):
        return self.s

    def __repr__(self):
        return self.s


