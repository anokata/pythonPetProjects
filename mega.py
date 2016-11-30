# TODO add list indexing
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

    def add_attr(self, k, v):
        setattr(self, k, v)

    def __setattr__(self, k, v):
        super().__setattr__(k, v)
        if hasattr(self, '_keys'):
            if k != '_keys' and k not in self._keys:
                self._keys.append(k)
