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


