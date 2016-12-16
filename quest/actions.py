from map_util import *
from util import *
from log import *

def door_action_start(key_sym, world): #передавать stateSys? объект у кот вызывать? передавать функ?
    if key_sym == 'o':
        log_msg('Открыть дверь в какой стороне?', world)
    else:
        log_msg('Закрыть дверь в какой стороне?', world)
    world.stateSystem.changeState('open_door')

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
            send_to_main_log(world.messages, obj.search_msg)
    if not found:
        log_msg('Ничего необычного', world)
    else:
        log_msg(found, world)

def do_take(_, world):
    log_msg('Взять откуда?', world)
    direction_do(world, take_from)

def take_from(x, y, world, _):
    obj = object_at_xy(x, y, world.objects)
    if obj:
        if obj.takeable:
            log_msg('Беру ' + obj.name, world)
            send_to_main_log(world.messages, 'Вы берёте ' + obj.name)
            inventory_add(obj, world.inventory)
            remove_obj(obj, world.objects)
        else:
            if obj.contain: # пока не содержат более одного объекта
                if obj.need_key:
                    send_to_main_log(world.messages, obj.name + ' заперт')
                    return
                contaiment = obj.contain[0]
                log_msg('Беру из {} {}'.format(obj.name, contaiment.name), world)
                send_to_main_log(world.messages, 'Вы берёте {} из {}'.format(contaiment.name, obj.name))
                obj.contain = False
                inventory_add(contaiment, world.inventory)
            else:
                log_msg('Это нельзя брать.', world)
    else:
        log_msg('Здесь нечего брать.', world)

def inventory_add(obj, inventory):
    inventory.append(obj)

def direction_do(world, fun, *args):
    world.direction_action = fun
    world.direction_args = args
    world.stateSystem.changeState('direction')

def direction_keypress(key_sym, world):
    direction = get_direction(key_sym)
    if direction:
        x, y = direction
        x = world.player.x + x
        y = world.player.y + y
        world.direction_action(x, y, world, world.direction_args)
        world.stateSystem.changeState('walk')
    else:
        log_msg('Неправильное направление. ', world)

def get_direction(key_sym):
    keyboard_fun = {
            'j':lambda _: (0, 1),
            'k':lambda _: (0, -1),
            'h':lambda _: (-1, 0),
            'l':lambda _: (1, 0),
            '.':lambda _: (0, 0),
            }
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        return fun(0)
    else:
        return False

INVENTORY_VIEW_ITEM = 'v'
INVENTORY_APPLY_ITEM = 'a'
def do_inventory_action(world, action, object_index):
    inventory_actions = {
        INVENTORY_VIEW_ITEM: inventory_view_action,
        INVENTORY_APPLY_ITEM: lambda w, x: direction_do(w, inventory_apply_action, x),
            }
    if object_index < len(world.inventory):
        fun = inventory_actions.get(action, False)
        if fun:
            fun(world, world.inventory[object_index])

def inventory_apply_action(x, y, world, applicator):
    pacient = object_at_xy(x, y, world.objects)
    if pacient:
        applicator = applicator[0]
        send_to_main_log(world.messages, 
                "Пытатетесь применить {} к {}...".format(applicator.name, pacient.name))# не должен быть .messages?
        result = object_apply(applicator, pacient, world)
        if not result:
            send_to_main_log(world.messages, "не получилось")
    else:
        log_msg('Не к чему применять', world)

def object_apply(applicator, pacient, world):
    objects_apply_table = { # to world?
            4001: {
                4000: try_key_door,
                },
        }
    table2 = objects_apply_table.get(applicator.id, False)
    if not table2:
        return False
    fun = table2.get(pacient.id, False)
    if fun:
        return fun(applicator, pacient, world)
    else:
        return False

def try_key_door(key, door, world):
    send_to_main_log(world.messages, 'Пытатетесь открыть '+ door.name +' ключом...')
    if door.need_key:
        if key.key_id == door.key_id:
            send_to_main_log(world.messages, 'Ключ подошёл, отпирате.')
            door.key_used = True
            door.need_key = False
        else:
            send_to_main_log(world.messages, 'Ключ не подходит')
    else:
            send_to_main_log(world.messages, door.name + ' не запертo')
    return True

def inventory_view_action(world, obj):
    world.messages.object_info = list()
    world.messages.object_info.append(obj.name)
    world.messages.object_info.append(obj.info_msg)
    world.stateSystem.changeState('inventory_view_object')

def go_inventory(key_sym, world):
    world.stateSystem.changeState('inventory')
    world.inventory_action = key_sym
