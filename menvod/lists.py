import sys
sys.path.append('../modules')
import mega
import pytest

def init():
    lst = mega.Mega()
    lst.list = list()
    lst.selected = False
    return lst

def items(lst):
    return lst.list

def add(lst, val):
    return lst.list.append(val)

def next(lst):
    lst.selected += 1
    if lst.selected >= len(lst.list):
        lst.selected = 0

def get_selected(lst):
    return lst.list[lst.selected]

## test
global test_data, lst
def setup_module(module):
    global test_data, lst
    test_data = list(range(3))
    lst = init()
    for i in test_data:
        add(lst, i)

def test_items_add():
    assert(len(items(lst)) == len(test_data))

def test_list_selnext():
    assert(get_selected(lst) == 0)
    next(lst)
    assert(get_selected(lst) == 1)
    next(lst)
    next(lst)
    assert(get_selected(lst) == 0)

if __name__=='__main__':
    print('main')
    setup_module('')
    next(lst)
    print(lst, lst.list, lst.selected)

