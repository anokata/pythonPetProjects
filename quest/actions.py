from map_util import *
from util import *
from log import *
import random

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

def try_open_door(world, x, y, actor, objects): #describe status
    x += actor.x
    y += actor.y
    obj = object_at(Point(x, y), objects)
    if obj:
        if obj.can_open:
            if obj.need_key:
                return OPEN_NEED_KEY, obj
            else:
                status = open_door(obj)
                tire(world, actor.arms)
                return status, obj
        else:
            return OPEN_CANNOT, obj
    else:
        return OPEN_NODOOR, obj

def go_down(_, world):  # TODO все движущиеся должны менять и на карте положение
    actor = world.player
    if can_be_there(actor.x, actor.y + 1, world):
        actor.y += 1 # move_to(x, y, obj, objects)
        tire(world, world.player.legs)

def go_up(_, world): 
    actor = world.player
    if can_be_there(actor.x, actor.y - 1, world):
        actor.y -= 1
        tire(world, world.player.legs)

def go_left(_, world):
    actor = world.player
    if can_be_there(actor.x - 1, actor.y, world):
        actor.x -= 1
        tire(world, world.player.legs)

def go_right(_, world): 
    actor = world.player
    if can_be_there(actor.x + 1, actor.y, world):
        actor.x += 1
        tire(world, world.player.legs)

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
            log_main(obj.search_msg, lblue)
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
            log_main('Вы берёте ' + obj.name, lblue)
            inventory_add(obj, world.inventory)
            remove_obj(obj, world.objects)
            tire(world, world.player.arms)
        else:
            if obj.contain: # пока не содержат более одного объекта
                if obj.need_key:
                    log_main(obj.name + ' заперт', lred)
                    return
                contaiment = obj.contain[0]
                log_msg('Беру из {} {}'.format(obj.name, contaiment.name), world)
                log_main('Вы берёте {} из {}'.format(contaiment.name, obj.name))
                obj.contain = False
                inventory_add(contaiment, world.inventory)
                tire(world, world.player.arms)
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
        log_main("Пытатетесь применить {} к {}...".format(applicator.name, pacient.name))
        result = object_apply(applicator, pacient, world)
        if not result:
            log_main("не получилось", lred)
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
    log_main('Пытатетесь открыть '+ door.name +' ключом...')
    if door.need_key:
        tire(world, world.player.arms)
        if key.key_id == door.key_id:
            log_main('Ключ подошёл, отпирате.', lgreen)
            door.key_used = True
            door.need_key = False
        else:
            log_main('Ключ не подходит', lred)
    else:
            log_main(door.name + ' не запертo')
    return True

def inventory_view_action(world, obj):
    world.messages.object_info = list()
    world.messages.object_info.append(obj.name)
    world.messages.object_info.append(obj.info_msg)
    world.stateSystem.changeState('inventory_view_object')

def go_inventory(key_sym, world):
    world.stateSystem.changeState('inventory')
    world.inventory_action = key_sym

def do_smash(_, world):
    log_msg('Сломать где?', world)
    direction_do(world, smash_at)

def smash_at(x, y, world, _):
    obj = object_at_xy(x, y, world.objects)
    if obj:
        if obj.smashable:
            log_main('Вы пытаетесь сломать ' + obj.name)
            #TODO усталость? или статус и потом обработка или сообщение
            tire(world, world.player.legs, 0.5)
            if obj.need_strength_type == 'LEG':
                strength = world.player.legs.strength
            actual_probability = calc_smash_probablity(strength, obj.need_strength, obj.smash_probability)
            if take_chance(actual_probability):
                log_main('Получилось сломать', lgreen)
                obj.can_open = True
                obj.smashable = False
                obj.walk_msg = ''
                obj.search_msg = obj.smashed_msg
            else:
                log_main('Неполучилось сломать', lred)
        else:
            log_main('Это нельзя cломать')
    else:
        log_main('Здесь нечего ломать')

def calc_smash_probablity(strength, need, probablity):
    p = strength/need * probablity
    return p if p <= 1.0 else 1.0

def take_chance(probablity):
    dice = random.random()
    return dice < probablity

def tick(world):
    world.tick += 1
    if world.tick_events.contain(str(world.tick)):
        event = world.tick_events.get(str(world.tick))
        if event.type == 'MSG':
            log_main(event.msg, blue)
    print(world.tick)
    if not world.player.live:
        print('you not live, bye')
        exit()
    energy_exchange(world.player)

def energy_exchange(player):
    spend_energy(player, 0.01)
    if player.available_energy < player.max_available/3:
        energy_flow(player, 1)
    #TODO
    pass    

def energy_flow(player, val):
    if not dec_stock_energy(player, val):
        player.available_energy += val
        if player.available_energy > player.max_available:
            player.available_energy = player.max_available

def dec_stock_energy(player, val):
    player.stock_energy -= val
    if player.stock_energy <= 0:
        player.stock_energy = 0
        return True
    return False

def dec_available_energy(player, val):
    player.available_energy -= val
    if player.available_energy < 0.0 and player.stock_energy > 0.0:
        player.stock_energy -= 0.1
        player.available_energy += 0.1

def spend_energy(player, val):
    if player.available_energy > 0.0:
        dec_available_energy(player, val)
    #tick()
    if not (player.available_energy > 0.0 or player.stock_energy > 0.0):
        player.live = False
        log_main('Ваша энегрия иссякла, вы больше не можете функционировать.', red)

def rest(n, world):
    for i in range(n):
        if world.player.available_energy > 0.0:
            spend_energy(world.player, 0.1)
            tick(world)
            restore = world.player.legs.max_stamina/100.0
            rest_part(world.player.legs, restore)
            restore = world.player.arms.max_stamina/100.0
            rest_part(world.player.arms, restore)
            restore = world.player.body.max_stamina/100.0
            rest_part(world.player.body, restore)

def rest_part(part, val):
    part.stamina += val
    if part.stamina > part.max_stamina:
        part.stamina = part.max_stamina

def calc_water_loss(world):
    player_temp = calc_avg_temp(world.player)
    env_temp = world.rooms.current.temp
    #TODO
    return (env_temp**2)/400

def water_loss(world):
    world.player.water_level -= calc_water_loss(world)
    #TODO

def calc_avg_temp(player):
    return (player.body.temp + player.legs.temp + player.arms.temp + player.head.temp) / 4

def tire(world, part, amount=0.1):
    part.stamina -= amount
    if part.stamina <= 0.01:
        amount = part.stamina + amount
        part.stamina = 0
        log_main('Ваши {} полностью устали, вы упали без сил'.format(part.name), red)
        rest(10, world)
        log_main('Вы немного отдохнули', lred)
    sub_strength_part(part, amount/10.0)
    train_stamina(part, amount)
    train_strength(part, amount)
    water_loss(world)

def tired(part):
    return part.stamina == 0

def train_stamina(part, amount):
    part.max_stamina += amount/10.0

def train_strength(part, amount):
    part.max_strength += amount/20.0

def do_warmup(_, world):
    log_main('Вы делаете зарядку.', lgreen)
    actor = world.player
    if warm_up_all(world, actor):
        log_main('Вы чувствуете себя сильнее.', green)
    else:
        log_main('Никакого эффекта, только устали.', lred)
        
def warm_up_all(world, actor):
    b = warm_up_part(world, actor.body)
    l = warm_up_part(world, actor.legs)
    a = warm_up_part(world, actor.arms)
    return any([b,l,a])

def warm_up_part(world, part):
    if part.stamina == part.max_stamina:
        tire(world, part)
        return add_strength_part(part)
    tire(world, part)
    return False

def sub_strength_part(part, amount):
    part.strength -= amount
    if part.strength < 0:
        part.strength = 0

def add_strength_part(part):
    if part.strength == part.max_strength:
        return False
    part.strength += 1
    if part.strength > part.max_strength:
        part.strength = part.max_strength
    return True
