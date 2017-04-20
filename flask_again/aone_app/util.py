def dir2tree(dirs):
    result = None
    for dir in dirs:
        if dir['parent_id']== None:
            result = Node(dir['id'], dir['name'])
        else:
            result.add_parent(dir['parent_id'], Node(dir['id'], dir['name']))
    return result

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.nodes = list()
        self.nodesid = list()

    def show(self):
        return "({} {})\n".format(self.id, self.name)

    def __str__(self):
        r = self.show()
        for n in self.nodes:
            r += '----' + str(n)
        return r

    def __repr__(self):
        return str(self)

    def add(self, node):
        self.nodes.append(node)
        self.nodesid.append(node.id)

    def add_parent(self, parent_id, node):
        if self.id == parent_id:
            self.add(node)
        for n in self.nodes:
            n.add_parent(parent_id, node)
    
    def map(self, fun):
        res = str(fun(self))
        for n in self.nodes:
            res += n.map(fun)
        return res
    
    def map_to_div(self, level=0):
        res = "<div id='{}' class='tree level-{}'>{}".format(self.id, level, self.name)
        for n in self.nodes:
            res += n.map_to_div(level + 1)
        return res + "</div>"

class Dir:
    def __init__(self, name, id, parent_id):
        self.name = name
        self.id = id
        self.parent_id = parent_id

    def __str__(self):
        return "|{} {} {}| ".format(self.name, self.id, self.parent_id)

    def __repr__(self):
        return str(self)

    def __getitem__(self, key): 
        return getattr(self, key)

dirs = [
        Dir("arot", 1, None),
        Dir("b", 2, 1),
        Dir("c", 3, 1),
        Dir("e", 5, 2),
        Dir("f", 6, 2),
        Dir("end", 7, 5),
]
d = dir2tree(dirs)
print(d)
print(d.nodes)
d.map(lambda x: print(x.name))
print(d.map_to_div())
