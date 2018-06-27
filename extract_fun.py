#!/bin/env python
import ast

testfile = "./dump.py"
teststring = "'inn':inn,"


def read_file(filename):
    with open(filename, 'r') as fin:
        return fin.read()


def line_num_for_phrase_in_file(phrase, filename):
    with open(filename,'r') as f:
        for (i, line) in enumerate(f):
            if phrase in line:
                return i + 1
    return -1

def get_ast_tree(filename):
    try:
        with open(filename) as fin:
            code_text = fin.read()
    except:
        print("Error reading input file")
        exit()
    return ast.parse(code_text)

class FindFunc(ast.NodeVisitor):

    last_func = None
    in_func = False
    f_start = None
    f_end = None
    doc = None

    def visit(self, node):
        if isinstance(node, ast.FunctionDef):
            self.last_func = node

        l = getattr(node, 'lineno', None)
        #print(l, node)
        ast.NodeVisitor.visit(self, node)
        if l == line_number:
            #print(l, node, self.last_func.name, self.last_func.lineno)
            self.in_func = True
            self.f_start = self.last_func.lineno
            # TODO check docstring
            self.doc = ast.get_docstring(self.last_func)

        if l and self.in_func and l > line_number and isinstance(node, ast.FunctionDef):
            #print('end? ', node.lineno - 1)
            self.in_func = False
            self.f_end = self.last_func.lineno - 1
            #print("{} - {}".format(self.f_start, self.f_end))


def cut_lines(text, start, end):
    acc = ""
    for (i, line) in enumerate(text.split("\n")):
        if i + 1 >= start and i < end:
            acc = "\n".join([acc, line])
    return acc

#print(tree, tree.body)
#print(line_number)

file_content = read_file(testfile)
tree = get_ast_tree(testfile)
line_number = line_num_for_phrase_in_file(teststring, testfile)

finder = FindFunc()
finder.visit(tree)
#print("{} - {}".format(finder.f_start, finder.f_end))

print(cut_lines(file_content, finder.f_start, finder.f_end))
