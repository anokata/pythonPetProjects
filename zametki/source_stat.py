from pprint import pprint
import re

def test ( a, b,  c , d,e):
    pass

def is_empty_line(s):
    if s.strip(' \n\t') == '':
        return s
    return False

not_empty_line = lambda s: not is_empty_line(s)

def get_def(l):
    if l.startswith('def'):
        return l
    else:
        return False

def get_func_name(l):
    return (l.split('(')[0][3:].strip())

def get_func_args(l):
    args = (l.split('(')[1].split(')')[0]).strip().split(',')
    args = list(map(str.strip, args))
    return args

def print_funcs(funcs):
    for fun_name, fun_args in funcs.items():
        print(fun_name, len(fun_args), fun_args)
#TODO посчёт оступов..
# подсчёт длинны функции
def _(fn='source_stat.py'):
    with open(fn, 'rt') as fin:
        lines = fin.readlines()
        print(idents(lines))
        lines = list(filter(not_empty_line, lines))
        lines = list(filter(get_def, lines))
        funcs = dict()
        for l in lines:
            fun_name = get_func_name(l)
            fun_args = get_func_args(l)
            funcs[fun_name] = fun_args
        print_funcs(funcs)

def validate_idents(idents):
    without_nulls = filter(notnull, idents)

#REFORM
#def validate_idents idents:
#    without_nulls = filter notnull idents
#ENDREFORM

def isnull(x): return x == 0
def notnull(x): return not isnull(x)

def idents(lines):
    ident = list()
    for l in lines:
        spaces = get_ident(l)
        ident.append(spaces)
    return ident

def get_ident(line):
    return count_start_space(line)

def count_start_space(line):
    count = 0
    for c in line:
        if c != ' ':
            return count
        count += 1

if __name__ == '__main__':
    _()
