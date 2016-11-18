from pprint import pprint

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
        lines = list(filter(not_empty_line, lines))
        lines = list(filter(get_def, lines))
        funcs = dict()
        for l in lines:
            fun_name = get_func_name(l)
            fun_args = get_func_args(l)
            funcs[fun_name] = fun_args
        print_funcs(funcs)

if __name__ == '__main__':
    _()
