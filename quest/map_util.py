from mega import *
from util import *
from log import *
from collections import defaultdict

def object_by_char(objects, char): # ограничить полем видения
    for o in objects.values():
        if o[-1].char == char:
            return o[-1]
    return False

def object_at_xy(x, y, objects):
    obj = objects.get((x, y), False)
    if obj:
        return obj[-1]
    return obj

def remove_obj(obj, objects):
    objects.pop((obj.x, obj.y))

def object_at(point, objects): 
    x, y = point.x, point.y
    o = object_at_xy(x, y, objects)
    if o and o.name != 'self':
        return o
    return False

def can_be_there(x, y, world):
    objects = world.objects
    obj = object_at_xy(x, y, objects)
    if not obj or obj.name == 'self':
        return True
    walk_to_obj(world, obj)
    return obj.passable

def walk_to_obj(world, obj):
    if obj.walk_msg:
        log_main(obj.walk_msg)

def describe_objects(objects, world): #test
    strings = 'Вижу:\n'
    for o in objects:
        if o.viewable:
            strings += "     " + o.name + '(%s)\n'%o.char
    return strings

def retile_map(m, pairs): #test
    prs = dict(zip(pairs[::2], pairs[1::2]))
    prs = str.maketrans(prs)
    m = [line.translate(prs) for line in m]
    return m

def object_char_translate(obj):
    if type(obj.char) is int:
        obj.char = chr(obj.char)
    if hasattr(obj, 'close_char') and type(obj.close_char) is int:
        obj.close_char = chr(obj.close_char)
    return obj

def extract_objects(amap, objects_data, floor_char=' '): #test, join? extract?
    objects = defaultdict(list)
    for x in range(len(amap[0])):
        for y in range(len(amap)):
            char = amap[y][x]
            if char in objects_data:
                obj = DotDict(x=x, y=y, char=char)
                obj.update(objects_data[char]) #TODO recursive
                object_char_translate(obj)
                if obj.contain:
                    cont = list()
                    for obj_in_container in obj.contain:
                        _, obj_in = obj_in_container.popitem()
                        contaiment = DotDict(**obj_in)
                        object_char_translate(contaiment)
                        cont.append(contaiment)
                    obj.contain = cont
                #objects.append(obj)
                add_object(objects, obj)
                amap[y] = amap[y][:x] + floor_char + amap[y][x+1:]
    return objects

def add_object(objects, obj):
    objects[(obj.x, obj.y)].append(obj)

def get_object(objects_data, name):
    obj = DotDict(**objects_data[name])
    if type(obj.char) is int:
        obj.char = chr(obj.char)
    return obj

def objects_in_view(actor, world): 
    objects = world.objects
    w = world.map_width
    h = world.map_height
    objs = set()
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            x = actor.x + i
            y = actor.y + j
            if 0 <= x < w and 0 <= y < h:
                o = object_at(Point(x, y), objects)
                if o and o.name != 'self' and o.name != 'spawn':
                    objs.add(o)
    return objs

def get_room_at(world, x, y):
    tile = world.rooms_map[y][x]
    if world.rooms.contain(tile):
        room = world.rooms.get(tile)
        return room
    return world.rooms.current

def update_current_room(world):
    old_room = world.rooms.current
    new_room = get_room_at(world, world.player.x, world.player.y)
    if old_room != new_room:
        world.rooms.current = new_room
        log_main('Вхожу в ' + new_room.name)
