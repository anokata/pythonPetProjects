# TODO add list indexing
# add append dict - mega.append({'x': 8...})
class MutableNamedTuple():
    def __init__(self, **kwargs):
        self._keys = list()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        s = ''
        for k in self._keys:
            s += str(k) + ':' + str(getattr(self, k)) + '\n'
        return s
    __repr__ = __str__

    def add_attr(self, k, v):
        setattr(self, k, v)

    def __setattr__(self, k, v):
        super().__setattr__(k, v)
        if hasattr(self, '_keys'):
            if k != '_keys' and k not in self._keys:
                self._keys.append(k)

    def set(self, k, v):
        setattr(self, k, v)

    def items(self):
        return self._keys

    def update(self, dct):
        for k,v in dct.items():
            self.add_attr(k, v)
    
    def get(self, key):
        return getattr(self, key)

    def contain(self, key):
        return key in self._keys

Mega = MutableNamedTuple
DotDict = Mega
def make_recursive_dotdict(dct):
    res = DotDict(**dct)
    for k, v in dct.items():
        if type(v) is dict:
            res.set(k, make_recursive_dotdict(v))
    return res
