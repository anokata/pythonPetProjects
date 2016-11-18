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
        an = list()
        word = 'the is exis'.split()
        for w in word:
            an.append(s.find(w) > 0)
        return all(an)

    def dexor(s, key):
        r = list()
        i = 0
        while i <= len(s)-1:
            r.append(s[i] ^ key[i%n])
            i += 1
        return r

    def key_to_ords(key):
        r = list()
        s = ord('a')
        for i in range(n):
            key, m = divmod(key, 26)
            r.append(m+s)
        return r

    n = 3
    s = code_to_str(data)
    i = 0
    key = 0
    #while not meaning(s):
    while True:
        key += 1
        k = key_to_ords(key)
        d = dexor(data, k)
        s = code_to_str(d)
        i += 1
        if i % 1000 == 0:
            print(key, k, s[10:20])
        if meaning(s):
            print(s, k)
    print(key)
    s = code_to_str(dexor(data, k))
    print(s)

euler59()
