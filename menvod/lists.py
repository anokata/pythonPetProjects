import sys
sys.path.append('../modules')
import mega
import pytest
import ByteFont

current_list = None

def init(x=0, y=0, *items):
    lst = mega.Mega()
    lst.list = list()
    lst.selected = False
    lst.select_color = (1, 0, 0)
    lst.color = (1, 1, 0)
    lst.x = x
    lst.y = y
    for item in items:
        add(item, lst)
    global current_list
    current_list = lst
    return lst

def items(lst=None):
    lst = _get_lst(lst)
    return lst.list

def color(index, lst):
    lst = _get_lst(lst)
    return lst.color if lst.selected != index else lst.select_color

def colored(lst=None):
    lst = _get_lst(lst)
    return ((item, color(index, lst)) for index, item in enumerate(items(lst)))

def add(val, lst):
    lst = _get_lst(lst)
    return lst.list.append(val)

def next(lst=None):
    lst = _get_lst(lst)
    lst.selected += 1
    if lst.selected >= len(lst.list):
        lst.selected = 0

def get_selected(lst=None):
    lst = _get_lst(lst)
    return lst.list[lst.selected]

def _get_lst(lst):
    if lst == None:
        return current_list
    return lst

def render(lst=None):
    lst = _get_lst(lst)
    y = lst.y
    x = lst.x
    for item, color in colored(lst):
        ByteFont.draw_text(item, y=y, x=x, color=color)
        y += 1

## test
global test_data, lst
def setup_module(module):
    global test_data, lst
    test_data = list(range(3))
    lst = init()
    for i in test_data:
        add(i, lst)

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
    print(list(colored(lst)))

