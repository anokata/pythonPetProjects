import base64
import pickle
import datetime
import os

class pdict(dict):
    def __str__(self):
        t =''
        for k, v in self.items():
            t += str(k) + ': ' + str(v) + '\n'
        return t
      
class Storage():
    storage = pdict()
    fn = 'storage.dat'

    def __init__(self):
        if os.path.exists(self.fn) and os.path.isfile(self.fn):
            self.load()

    def __setitem__(self, key, val):
        nowstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        val = (nowstr, base64.b64encode(bytes(val, 'utf-8')))
        self.storage[key] = val

    def __getitem__(self, key):
        now, val = self.storage[key]
        val = base64.b64decode(val).decode('utf-8')
        return (now, val)

    def load(self):
        fl = open(self.fn, 'rb')
        self.storage = pickle.load(fl)
        fl.close()

    def save(self):
        fl = open(self.fn, 'wb')
        pickle.dump(self.storage, fl)
        fl.close()

    def __str__(self):
        return str(self.storage)
 
 
if __name__ == '__main__':
    #test
    storage = Storage()
    a = storage['etst']
    print(a)
    #storage['etst2'] = 'abc'
    storage.save()
    print(storage)


