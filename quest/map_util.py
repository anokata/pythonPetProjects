from mega import *

def object_at(x, y, objects): # Выделить точку, и карту с объктами вместе
    for o in objects:
        if o.x == x and o.y == y:
            return o
    return False

def can_be_there(x, y, amap, objects):
    obj = object_at(x, y, objects)
    if not obj:
        return True
    return obj.passable


def chars_in_view(actor, amap): #join
    w = len(amap[0])
    h = len(amap)
    chars = set()
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            x = actor.x + i
            y = actor.y + j
            if 0 <= x < w and 0 <= y < h:
                char = amap[y][x]
                if char not in ' ':
                    chars.add(char)
    return chars

def chars_describe(chars, objects): #test
    strings = 'Вижу:\n'
    for c in chars:
        if c in objects:
            strings += "     " + objects[c]['name'] + '(%s)\n'%c
    return strings

def retile_map(m, pairs): #test
    prs = dict(zip(pairs[::2], pairs[1::2]))
    prs = str.maketrans(prs)
    m = [line.translate(prs) for line in m]
    return m

def extract_objects(amap, objects_data, floor_char=' '): #test, join? extract?
    objects = list()
    for x in range(len(amap[0])):
        for y in range(len(amap)):
            char = amap[y][x]
            if char in objects_data:
                obj = DotDict(x=x, y=y, char=char)
                obj.update(objects_data[char])
                if type(obj.char) is int:
                    obj.char = chr(obj.char)
                if hasattr(obj, 'close_char') and type(obj.close_char) is int:
                    obj.close_char = chr(obj.close_char)
                if obj.contain:
                    cont = list()
                    for obj_in_container in obj.contain:
                        _, obj_in = obj_in_container.popitem()
                        cont.append(DotDict(**obj_in))
                    obj.contain = cont
                objects.append(obj)
                amap[y] = amap[y][:x] + floor_char + amap[y][x+1:]
    return objects
