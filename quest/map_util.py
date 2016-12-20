from mega import *
from util import *
from log import *
from collections import defaultdict
import yaml
from light import *
help_mgs = '''Управление:
h - влево
l - вправо
j - вниз
k - вверх
, - взять
o - открыть
c - закрыть
s - исследовать
i - инвентарь
a - применить
v - осмотреть предмет
ESQ - выход
i - инвентарь
m - сломать
J - разминка ?
e - съесть
H - помощь выкл.
'''
def recalc_light(world):
    light_map = dict() 
    world.light_map = light_map
    px = world.player.x
    py = world.player.y
    light_map[(px, py)] = True
    #for r in get_circle_rays(5):
    for r in cast_rays(world):
        for x,y in r:
            light_map[(x+px, y+py)] = True

def cast_rays(world):
    R = 8
    px = world.player.x #TODO get_player_pos
    py = world.player.y
    rays = list()
    for ray in get_circle_rays(R):
        new_ray = list()
        for x, y in ray:
            obj = object_at_xy(x + px, y + py, world.objects) #TODO just world?.get_objects
            if not obj:
                new_ray.append((x, y))
            elif obj.passable:
                new_ray.append((x, y))
            else:
                new_ray.append((x, y))
                break
        rays.append(new_ray)
    return rays


def load_map(map_file, world):
    # state = {'map': yaml.load(... #TODO переделать в виде явных данных
    #           'player' : make_actor ... 
    world.level_data = yaml.load(open(map_file)) # map load method, from string?
    world.map = world.level_data['map'][0].split('\n')
    world.map = [line for line in world.map if line != '']
    world.map_width = len(world.map[0])
    world.map_height = len(world.map)
    world.rooms_map = world.map
    world.level_data['objects']
    world.objects_data = world.level_data['objects']
    world.objects = extract_objects(world)
    spawn = object_by_char(world.objects, '@')
    sx, sy = spawn.x, spawn.y
    remove_obj(spawn, world.objects)
    world.map = retile_map(world.map, world.level_data['map_tiles'])
    world.map = lines_to_xydict(world.map)
    init_messages(world)
    load_rooms(world)
    log_msg(world.level_data['mapname'], world)
    log_main(world.level_data['start_msg'], white)
    light_map = dict() # так может это в свойстве тайла карты. наверно нет т.к. постоянно заного обновлять? или стат свет
    world.light_map = light_map
    return sx, sy

def lines_to_xydict(amap):
    dict_map = dict()
    for x in range(len(amap[0])):
        for y in range(len(amap)):
            dict_map[(x,y)] = amap[y][x]
    return dict_map

def init_messages(world):
    msgs = DotDict()
    world.messages = msgs
    world.messages.view_msg = 'none'
    world.messages.log_msg = '...'
    world.messages.help_mgs = help_mgs
    world.messages.main_log = list()
    world.messages.main_log_maxview = 10
    world.messages.log_y = world.map_height
    msgs.main_log_y = msgs.log_y+1
    world.messages.view_y = msgs.main_log_y + 10
    world.side_help = False
    set_main_log(world.messages)

def load_rooms(world):
    rooms = make_recursive_dotdict(world.level_data['rooms'])
    world.rooms = rooms
    world.rooms.current = get_room_at(world, 0, 0)

def new_map_load(map_file, world):
    x, y = load_map(map_file, world)
    world.player.x = x
    world.player.y = y
    recalc_light(world)
    update_current_room(world)

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
    return walk_to_obj(world, obj)

def walk_to_obj(world, obj):
    if obj.walk_msg:
        log_main(obj.walk_msg)
    if obj.walk_action and obj.walk_action == 'map_load':
        new_map_load(obj.map_dest, world)
        return False
    return obj.passable

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

def convert_object(obj): #yaml dict to mega
    if obj.contain:
        cont = list()
        for obj_in_container in obj.contain:
            _, obj_in = obj_in_container.popitem()
            contaiment = DotDict(**obj_in)
            object_char_translate(contaiment)
            cont.append(contaiment)
        obj.contain = cont
    if obj.eatable and obj.reminder:
        obj.reminder = DotDict(**obj.reminder)
    object_char_translate(obj)

def extract_objects(world, floor_char=' '): #test, join? extract?
    objects_data = world.objects_data
    amap = world.map
    char2obj = world.level_data['char_to_objects_names']
    char2obj = dict(zip(char2obj[::2], char2obj[1::2]))
    world.char2obj = char2obj #TODO extract
    objects = defaultdict(list)
    for x in range(len(amap[0])):
        for y in range(len(amap)):
            char = amap[y][x]
            if char in char2obj:
                obj_name = char2obj[char]
                obj = DotDict(x=x, y=y, char=char)
                obj.update(objects_data[obj_name]) #TODO recursive. make obj
                convert_object(obj)
                add_object(objects, obj)
                amap[y] = amap[y][:x] + floor_char + amap[y][x+1:]
                continue

            if char in objects_data:
                print('char')
                obj = DotDict(x=x, y=y, char=char)
                obj.update(objects_data[char]) #TODO recursive. make obj
                convert_object(obj)
                add_object(objects, obj)
                amap[y] = amap[y][:x] + floor_char + amap[y][x+1:]
    return objects

def add_object(objects, obj):
    objects[(obj.x, obj.y)].append(obj)

def get_object(world, name):
    obj = DotDict(**world.objects_data[name])
    convert_object(obj)
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
