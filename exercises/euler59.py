class MutableNamedTuple():
    def __init__(self, **kwargs):
        self._keys = list()
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._keys.append(k)
    def __str__(self):
        s = ''
        for k in self._keys:
            s += str(k) + ':' + str(getattr(self, k)) + '\n'
        return s

a = MutableNamedTuple(c=213, bb='a')
print(a)

def euler59():
    data = 0
    with open('/home/ksi/p059_cipher.txt', 'rt') as fin:
        data = '[' +  fin.read() + ']'
        data = eval(data)

    def code_to_str(a):
        return ''.join(map(chr, a))

    def meaning(s):
        if s.find('\0') > 0:
            return False
        return s.find('the') > 0

    def dexor(s, key):
        return list(map(lambda x: x ^ key, s))

    key = 0
    s = code_to_str(data)
    while not meaning(s) and key <= 255:
        key += 1
        s = code_to_str(dexor(data, key))
        print(key, s[10:20])
    print(key)
    s = code_to_str(dexor(data, key))
    print(s)

