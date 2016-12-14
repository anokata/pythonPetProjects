from map_util import can_be_there, object_at, objects_in_view
from util import *

def open_door(door):
    if door.opened:
        door.opened = False
        door.passable= False
        door.char = door.close_char
        return OPEN_CLOSED
    else:
        door.opened = True
        door.passable= True
        door.char = door.open_char
        return OPEN_OPEND

def try_open_door(x, y, actor, objects): #describe status
    x += actor.x
    y += actor.y
    obj = object_at(Point(x, y), objects)
    if obj:
        if obj.can_open:
            if obj.need_key:
                return OPEN_NEED_KEY, obj
            else:
                status = open_door(obj)
                return status, obj
        else:
            return OPEN_CANNOT, obj
    else:
        return OPEN_NODOOR, obj

def go_down(_, world): 
    actor = world.player
    if can_be_there(actor.x, actor.y + 1, world):
        actor.y += 1

def go_up(_, world): 
    actor = world.player
    if can_be_there(actor.x, actor.y - 1, world):
        actor.y -= 1

def go_left(_, world):
    actor = world.player
    if can_be_there(actor.x - 1, actor.y, world):
        actor.x -= 1

def go_right(_, world): 
    actor = world.player
    if can_be_there(actor.x + 1, actor.y, world):
        actor.x += 1

def do_search(_, world): 
    objs = objects_in_view(world.player, world)
    found = ''
    for obj in objs:
        if obj.contain:
            if obj.need_key:
                found += obj.name + ' заперт'
            else:
                for obj_in_container in obj.contain:
                    found += (obj.name + ' содержит ' + obj_in_container.name)
        elif obj.info_msg:
            found += obj.search_msg
    if not found:
        log_msg('Ничего необычного', world)
    else:
        log_msg(found, world)

def log_msg(msg, world):
    world.messages.log_msg = msg
