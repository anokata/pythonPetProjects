import base64
import pickle
import datetime
import os

class pdict(dict):
    def __str__(self, pfx=''):
        t =''
        for k, v in self.items():
            t += pfx + str(k) + ': ' + str(v) + '\n'
        return t
class StorageItem():

    def __init__(self, nowstr, val):
        self.val = (nowstr, val)

    def __str__(self, pfx=''):
        return pfx + str(self.val)

    def __getitem__(self, k):
        return self.val[1][k]
    def get(self):
        return self.val
    def __setitem__(self, k, v):
        self.val[1][k] = v

    def addDir(self, x):
        self.val[1].addDir(x)

    def isDir(self):
        return False

    def value(self):
        return base64.b64decode(self.val[1]).decode('utf-8')

class StorageDir():
    storage = pdict() #!!!

    def __init__(self, name='main'):
        self.storage = pdict()
        self.name = name
        self.nowstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    def __setitem__(self, key, val):
        nowstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if type(val) != StorageDir:
            val = StorageItem(nowstr, base64.b64encode(bytes(val, 'utf-8')))
        else:
            val = StorageItem(nowstr, val)
        self.storage[key] = val

    def getItems(self):
        return self.storage

    def getItem(self, key):
        val = self.storage[key]
        now = 'x'
        if type(val) != StorageDir:
            now, val = val.get()
            val = base64.b64decode(val).decode('utf-8')
        else:
            now = val.nowstr
        return StorageItem(now, val)
        
    def __getitem__(self, key):
        val = self.storage[key]
        if type(val) != StorageDir:
            _, val = val.get()
            val = base64.b64decode(val).decode('utf-8')
        return val

    def __str__(self, pfx=''):
        return pfx + str(self.storage)

    def addDir(self, name):
        self.storage[name] = StorageDir(name)

    def get(self):
        return ('', self.name)

    def isDir(self):
        return True

    def pprint(self):
        for k, v in self.storage.items():
            print(' ', k, '||', v, type(v))

    def value(self):
        return self.name + ' ' + self.nowstr

class Storage():
    fn = 'storage.dat'
    mainDir = 0

    def __init__(self, isLoad=True):
        if os.path.exists(self.fn) and os.path.isfile(self.fn) and isLoad:
            self.load()
        else:
            self.mainDir = StorageDir()

    def __setitem__(self, k, v):
        self.mainDir.__setitem__(k, v)

    def __getitem__(self, k):
        return self.mainDir[k]

    def load(self):
        fl = open(self.fn, 'rb')
        self.mainDir = pickle.load(fl)
        fl.close()

    def save(self):
        fl = open(self.fn, 'wb')
        pickle.dump(self.mainDir, fl)
        fl.close()

    def __str__(self):
        return '' + str(self.mainDir)

 
    def addDir(self, name):
        self.mainDir.addDir(name)

    def pprint(self):
        self.mainDir.pprint()

    def items(self):
        return self.mainDir.storage.items()

 
if __name__ == '__main__':
    # types text url urllist dir(as substorage)
    storage = Storage(False)
    storage['mainValue'] = '10'
    storage.addDir('Dir1')
    storage.addDir('Dir2')
    storage['Dir1']['subdirval'] = '123876.23'
    storage['Dir2']['subdirval'] = '1ll.23'
    storage['Dir2'].addDir('SubDir0')
    storage['Dir2']['SubDir0']['1'] = 'TYY'
    storage.save()
    storage2 = Storage(True)
    print(storage2)
    print('*'*8)
    print(storage2['mainValue'])
    #print(storage2['subdirval'])
    print(storage2['Dir1']['subdirval'])
    print(storage2['Dir1'])
    print(storage2.mainDir.storage.keys())
    print(storage2['Dir2']['SubDir0']['1'])
    print('*'*8)
    storage2.pprint()
    print('*'*8)
    print(storage2['Dir1'].storage.keys())
    print(storage2['Dir2']['SubDir0'].getItem('1'))
    print('*'*8)
    a = storage['mainValue'] 
    for k, v in storage2.items():
        print(k, v, v.isDir(), type(v), '**' ,v.value())
    print(a)

