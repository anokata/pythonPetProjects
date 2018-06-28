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
    line_number = None
    error = ""

    def __init__(self, line_number):
        self.line_number = line_number

    def visit(self, node):
        if isinstance(node, ast.FunctionDef):
            self.last_func = node

        l = getattr(node, 'lineno', None)
        ast.NodeVisitor.visit(self, node)
        if l == self.line_number and not self.in_func:
            self.in_func = True
            self.f_start = self.last_func.lineno
            self.doc = ast.get_docstring(self.last_func)
            if not self.doc:
                print("Line #{} : Missing docstring for function".format(self.last_func.lineno))
                error = "Line #{} : Missing docstring for function".format(self.last_func.lineno)

        if l and self.in_func and l > self.line_number and isinstance(node, ast.FunctionDef):
            self.in_func = False
            self.f_end = self.last_func.lineno - 1


def cut_lines(text, start, end):
    acc = ""
    for (i, line) in enumerate(text.split("\n")):
        if i + 1 >= start and i < end:
            acc = "\n".join([acc, line])
    return acc


class FindClass(ast.NodeVisitor):

    last_cls = None
    line_cls = None
    in_cls  = False
    f_start = None
    f_end = None
    doc = None
    line_number = None
    error = ""

    def __init__(self, line_number):
        self.line_number = line_number

    def visit(self, node):
        if isinstance(node, ast.ClassDef):
            self.last_cls = node

        l = getattr(node, 'lineno', None)
        ast.NodeVisitor.visit(self, node)
        if l == self.line_number and not self.in_cls:
            self.in_cls  = True
            self.f_start = self.last_cls.lineno
            self.line_cls = node

            self.doc = ast.get_docstring(self.last_cls)
            if not self.doc:
                print("Line #{} : Missing docstring for class".format(self.last_cls.lineno))

        if l and self.in_cls  and l > self.line_number and self.last_cls != self.line_cls:
            self.in_cls  = False
            self.f_end = self.line_cls.lineno - 1



testfile = "./extract_fun.py"
teststring = "self.last_func = node"

def check_doc_in_fun(filename, line):
    file_content = read_file(filename)
    tree = get_ast_tree(filename)
    line_number = line_num_for_phrase_in_file(line, filename)
    finder = FindFunc(line_number)
    finder.visit(tree)
    #print("{} - {}".format(finder.f_start, finder.f_end))
    #print(cut_lines(file_content, finder.f_start, finder.f_end))

def check_doc_in_class(filename, line):
    file_content = read_file(filename)
    tree = get_ast_tree(filename)
    line_number = line_num_for_phrase_in_file(line, filename)
    finder = FindClass(line_number)
    finder.visit(tree)
    #print("{} - {}".format(finder.f_start, finder.f_end))
    #print(cut_lines(file_content, finder.f_start, finder.f_end))


check_doc_in_fun(testfile, teststring)
check_doc_in_class(testfile, teststring)

diffile = "./diff"

def process_diff(filename):
    error_list = []
    diff_content = read_file(filename)
    for line in diff_content.split("\n"):
        if line.startswith("@"):
            print(line)
        else:
            pass

process_diff(diffile)
# если строка удалена?
# если изменена метод в классе то для класса тоже?
# 
