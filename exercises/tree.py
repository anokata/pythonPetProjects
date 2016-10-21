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
        if type(val) == BTree:
            self[BTree.LEFT] = val
        else:
            b = BTree()
            b.val = val
            self[BTree.LEFT] = b
            self.isLeaf = False
        return self._left

    def _sright(self, val):
        if type(val) == BTree:
            self[BTree.RIGHT] = val
        else:
            b = BTree()
            b.val = val
            self[BTree.RIGHT] = b
            self.isLeaf = False
        return self._right

    left = property(_left, _sleft)
    right = property(_right, _sright)

    def obxod(self, node, fun):
        if type(node) == BTree:
            fun(node.val)
            self.obxod(node.left, fun)
            self.obxod(node.right, fun)

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


# сделать двоичное дерево на словарях
# сделать алгоритм хаффмана
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
    msg = 'aadlfkfjafjsdlfjsdlfjaskldfjalfjlkcoixucvxucvuxuvuxuvxocvicxoaaoiuadaaaaaoifafu'
    # посчитаем количество каждого символа
    freq = pddict(int)
    for x in msg:
        freq[x] += 1
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

    #print(forest)
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
        #print(forest)
        b.obxod(b, print)
        print()

    #print(type(forest[0]))
    #print(len(forest))
    #print(forest[0].val)
    #print(forest[0].left.val)
    #print(forest[0].left.left)
    #print(forest[0].right.val)
    #print(forest[0])
    #print()
    forest[0].obxod(forest[0], lambda x: print(x))
    # нужно слияние деревьев. простое...
    b = BTree()
    b.val = 10
    b.left = 1
    b.right = 2
    c = BTree()
    c.val = 'a'
    c.left = 'b'
    c.right = b
    #print(type(c.right.left))
    #print(c.right == b)
    #print(c)
    return forest

if __name__ == '__main__':
    maintest()



