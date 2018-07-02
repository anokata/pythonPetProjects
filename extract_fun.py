#!/bin/env python
import ast
import unidiff

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
        last_func_start = getattr(self.last_func, 'lineno', None)
        ast.NodeVisitor.visit(self, node)
        if last_func_start and l == self.line_number and not self.in_func and not isinstance(node, ast.ClassDef):
            self.in_func = True
            self.f_start = self.last_func.lineno
            self.doc = ast.get_docstring(self.last_func)
            if not self.doc:
                self.error = "Line #{} : Missing docstring for function {}".format(
                        self.last_func.lineno, self.last_func.name)

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

    last_func = None
    in_func = False
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
        if isinstance(node, ast.FunctionDef):
            self.last_func = node
        if isinstance(node, ast.ClassDef):
            self.last_cls = node
        if self.last_func and self.last_func.col_offset == 0:
            self.last_cls = None

        l = getattr(node, 'lineno', None)
        last_class_start = getattr(self.last_cls, 'lineno', None)
        ast.NodeVisitor.visit(self, node)
        if last_class_start and l and l == self.line_number and not self.in_cls:
            self.in_cls  = True
            self.f_start = self.last_cls.lineno
            self.line_cls = node

            self.doc = ast.get_docstring(self.last_cls)
            if not self.doc:
                self.error = "Line #{} : Missing docstring for class {}".format(self.last_cls.lineno, self.last_cls.name)

        if l and self.in_cls  and l > self.line_number and self.last_cls != self.line_cls:
            self.in_cls  = False
            self.f_end = self.line_cls.lineno - 1


def check_doc_in_fun(filename, line):
    file_content = read_file(filename)
    tree = get_ast_tree(filename)
    line_number = line_num_for_phrase_in_file(line, filename)
    finder = FindFunc(line_number)
    finder.visit(tree)
    #print("{} - {}".format(finder.f_start, finder.f_end))
    #print(cut_lines(file_content, finder.f_start, finder.f_end))
    return finder.error

def check_doc_in_class(filename, line):
    file_content = read_file(filename)
    tree = get_ast_tree(filename)
    line_number = line_num_for_phrase_in_file(line, filename)
    finder = FindClass(line_number)
    finder.visit(tree)
    return finder.error


#testfile = "./extract_fun.py"
#testfile = "./test_extract_fun_complex.py"
#teststring = "self.last_func = node"
#check_doc_in_fun(testfile, teststring)
#check_doc_in_class(testfile, teststring)

def process_diff(filename):
    error_list = []
    diff_content = read_file(filename)

    patch = unidiff.PatchSet(diff_content)
    for file in patch:
        if not file.path.endswith(".py"):
            continue
        for hunk in file:
            for line in hunk:
                error = check_doc_in_fun(file.path, line.value)
                error_list.append(error)
                error = check_doc_in_class(file.path, line.value)
                error_list.append(error)

    for e in set(error_list):
        print(e)


diffile = "./diff"
process_diff(diffile)
# если строка удалена?
# если изменен метод в классе то для класса тоже?
