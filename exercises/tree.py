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
        
class BTree(pdict):
    val = ''

    def __init__(self):
        super().__init__(self)
        self['left'] = ''
        self['right'] = ''
    
    def _left(self):
        return self['left']

    def _right(self):
        return self['right']
    
    def _sleft(self, val):
        b = BTree()
        b.val = val
        self['left'] = b
        return self._left

    def _sright(self, val):
        b = BTree()
        b.val = val
        self['right'] = b
        return self._right

    left = property(_left, _sleft)
    right = property(_right, _sright)

    def __repr__(self):
        t = '{' + str(self.val)
        t += '\n'
        t += str(self.left)
        t += '\n'
        t += str(self.right)
        t += '}'
        return t
    __str__ = __repr__


# сделать двоичное дерево на словарях
# сделать алгоритм хаффмана
if __name__ == '__main__':
    t = Tree('a')
    t.add('b')
    t.add('c').add('x').add('xx').add('xxx')
    n = t.add('d')
    n.add('z')
    n.add('z2').add('y').add('yy')
    n.add('z3')
    print(t)
    print(t.show())
    msg = 'aadlfkfjafjsdlfjsdlfjaskldfjalfjlkcoixucvxucvuxuvuxuvxocvicxoaaoiuadaaaaaoifafu'
    # посчитаем количество каждого символа
    freq = pddict(int)
    for x in msg:
        freq[x] += 1
    # вычислим вероятность появления каждого символа
    for k, v in freq.items():
        freq[k] = (v, v/len(msg))
    print(freq)


    b = BTree()
    b.val = 10
    b.left = 1
    print(b)



