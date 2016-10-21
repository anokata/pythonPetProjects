from collections import defaultdict
class Tree:
    """Реализация дерева на списках"""
    # если хранить текущий узел и возвращать self то можно делать типа tree.left.left.right?
    parent = None # Tree
    value = 0
    children = [] # [Tree]
    deep = 1

    def __init__(self, rootval, parent=None, deep=1):
        self.children = list()
        self.value = rootval
        self.parent = parent
        self.deep = deep

    def __repr__(self):
        plain = str(self.value) + str(self.children)
        return plain 
    __str__=__repr__

    def add(self, val):
        newnode = (Tree(val, self, self.deep + 1))
        self.children.append(newnode)
        return newnode

    def show(self):
        t = str(self.value)
        for n in self.children:
            t += '\n' + (' ' * (self.deep-1)*2) + '|-'  + n.show()
        return t

class pddict(defaultdict):
    def __str__(self):
        t =''
        for k, v in self.items():
            t += str(k) + ': ' + str(v) + '\n'
        return t
class pdict(dict):
    def __str__(self):
        t =''
        for k, v in self.items():
            t += str(k) + ': ' + str(v) + '\n'
        return t
class plist(list):
    def __str__(self):
        t = ''
        for x in self:
            t += str(x) + '\n'
        return ''
        
class BTree(pdict):
    val = ''
    LEFT = 'left'
    RIGHT = 'right'
    isLeaf = True

    def __init__(self):
        super().__init__(self)
        self[BTree.LEFT] = ''
        self[BTree.RIGHT] = ''
    
    def _left(self):
        return self[BTree.LEFT]

    def _right(self):
        return self[BTree.RIGHT]
    
    def _sleft(self, val):
        self.isLeaf = False
        if type(val) == BTree:
            self[BTree.LEFT] = val
        else:
            b = BTree()
            b.val = val
            self[BTree.LEFT] = b
        return self._left

    def _sright(self, val):
        self.isLeaf = False
        if type(val) == BTree:
            self[BTree.RIGHT] = val
        else:
            b = BTree()
            b.val = val
            self[BTree.RIGHT] = b
        return self._right

    left = property(_left, _sleft)
    right = property(_right, _sright)

    def obxod(self, node, fun, procval=True):
        if type(node) == BTree:
            if procval:
                fun(node.val)
            else:
                fun(node)
            self.obxod(node.left, fun, procval)
            self.obxod(node.right, fun, procval)

    def getCodes(self, node, codes, curpath=''):
        if not node.isLeaf:
            self.getCodes(node.left, codes, curpath+'0')
            self.getCodes(node.right, codes, curpath+'1')
        else: #isLeaf
            codes.append((node.val[0], curpath))


    def tostr(self):
        #self.obxod(self, print)
        return str(self.val)

    def _toStr(self, deep):
        deep += 1
        t = '' + str(self.val)
        t += '\n' + ' ' * deep
        if type(self.left) == BTree:
            t += self.left._toStr(deep)
        else: t += str(self.left)
        if type(self.right) == BTree:
            t += self.right._toStr(deep)
        else: t += str(self.right)
        t += ''
        return t

    def __repr__(self):
        #t= self._toStr(0)
        t= self.tostr()
        return t
    __str__ = __repr__


def str2Bytes(s):
    r = list()
    for x in s:
        r.append(ord(x))
    return r
# сделать двоичное дерево на словарях
# сделать алгоритм хаффмана
def huffman():
    END = chr(255)*2 + 'END.'
    msg = 'aadlfkfxx:afjsdlfjsdlfjaskldfjalfjlkcoixucvxucvuxuvuxuvxocvicxoaaoiuadaaaaaoifafu'
    # посчитаем количество каждого символа
    freq = pddict(int)
    for x in msg:
        freq[x] += 1
    # Добавим спец код для конца.
    freq[END] = 1
    # вычислим вероятность появления каждого символа
    for k, v in freq.items():
        freq[k] = (v, v/len(msg))
    #print(freq)
    # сделаем лес деревьв. отсортируем.
    forest = list()
    for k, v in freq.items():
        t = BTree()
        t.val = (k, v[0], v[1])
        forest.append(t)

    forest.sort(key=lambda k: k.val[1], reverse=True)

    while len(forest) > 1:
        l = forest[-1]
        r = forest[-2]
        del forest[-1]
        del forest[-1]
        b = BTree()
        b.left = l
        b.right = r
        b.val = ('NEW', l.val[1] + r.val[1], l.val[2]+r.val[2])
        forest.append(b)
        forest.sort(key=lambda k: k.val[1], reverse=True)

    print(forest[0])
    #forest[0].obxod(forest[0], lambda x: print(x))
    # теперь сделаем обход по листьям с запоминанием путя, получением кода для символов.
    abc = list()
    forest[0].obxod(forest[0], lambda x: abc.append(x) if x.isLeaf else '', False)
    print(abc)
    codes = list()
    forest[0].getCodes(forest[0], codes, '')
    #print(codes)
    codes = pdict(codes)
    print(codes)
    #Зашифруем сообщение
    msgEnc = ''
    for x in msg:
        msgEnc += (codes[x])
    endcode = codes[END]
    msgEnc += codes[END]
    msgEnc += codes[END] # добавив в конец конечных сиволов до дополнения байта
    print(msgEnc, len(msgEnc), len(msgEnc)%8)
    msgEnc = msgEnc[:-(len(msgEnc)%8)] # обрежем до байта
    print(msgEnc, len(msgEnc), len(msgEnc)%8)
    #Расшифруем сообщение
    invCodes = {v: k for k, v in codes.items()} # инвентируем словарь
    print(invCodes)
    curcode = ''
    msgDec = ''
    msgE = msgEnc
    while msgEnc != '':
        curcode += msgEnc[0]
        msgEnc = msgEnc[1:]
        if curcode in invCodes:
            if curcode != endcode: # Пропускаем сдополняющие коды конца
                if curcode in invCodes: # и если это правильный код(неправильный - после обрезания)
                    msgDec += invCodes[curcode] 
            curcode = ''
    #Проверим
    print(msgDec)
    print(msg)
    print(msg==msgDec)
    msgEnc = msgE
    #Преобразуем в последовательность байт.
    msgBytes = list()
    for x in range(0, len(msgEnc), 8):
        #print(msgEnc[x:x+8])
        byte = int(msgEnc[x:x+8], 2)
        msgBytes.append(byte)
    print(msgBytes)
    #дописывать словарь.
    # формат: размер словаря(байт). последний элемент - элемент END
    msgKey = list()
    msgKey.append(len(codes))
    ordCodes = list(codes.items())
    ordCodes.sort(key = lambda x: x[0]) # отсортируем чтобы конечный был в конце
    print(ordCodes)
    for k, v in ordCodes:
        msgKey.append(ord(k[0]))
        msgKey += str2Bytes(v)

    print(msgKey)
    

def maintest():
    t = Tree('a')
    t.add('b')
    t.add('c').add('x').add('xx').add('xxx')
    n = t.add('d')
    n.add('z')
    n.add('z2').add('y').add('yy')
    n.add('z3')
    #print(t)
    #print(t.show())

    b = BTree()
    b.val = 10
    b.left = 1
    b.right = 2
    c = BTree()
    c.val = 'a'
    c.left = 'b'
    c.right = b
    huffman()

if __name__ == '__main__':
    maintest()



