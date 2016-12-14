from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from mega import *
from ByteFont import *
from gl_texture import draw_tex_quad
from gl_main import *
sys.path.append('../modules')
import stateSystem
from map_util import *
from actions import *
from render import *
from util import *
from log import *
import yaml

state = MutableNamedTuple()
state.window = 0
map_file = 'map.yaml'
font_file = 'font1.png'
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
'''

def make_actor(**kwargs):
    actor = DotDict(**kwargs)
    actor.takeable = False
    return actor

def init():
    state.font = init_font(font_file, 16, 16)
    set_font(state.font)
    init_map(map_file)
    init_states()

def init_map(map_file):
    world = DotDict()
    state.world = world
    world.level_data = yaml.load(open(map_file)) # map load method, from string?
    world.map = world.level_data['map'][0].split('\n')
    world.map_width = len(world.map[0])
    world.map_height = len(world.map)
    world.old_map = world.level_data['map'][0].split('\n')
    world.map = [line for line in world.map if line != '']
    world.old_map = [line for line in world.old_map if line != '']
    world.player = make_actor(name='self', x=3, y=3, color=(0,1,1), char='\x01')
    world.objects = list()
    world.level_data['objects']
    world.objects_data = world.level_data['objects']
    world.objects += extract_objects(world.map, world.objects_data)
    world.objects.append(world.player)
    # state = {'map': yaml.load(... #TODO переделать в виде явных данных
    #           'player' : make_actor ... 
    world.map = retile_map(world.map, world.level_data['map_tiles'])
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
    send_to_main_log(world.messages, 'Я оказался в ' + world.level_data['mapname'])
    colors = DotDict()
    colors.color_multiplier = 1.0
    colors.color_multiplier_dir = True
    world.colors = colors
    world.inventory = list()
    world.inventory.append(get_object(world.objects_data, 'a'))
    #rooms = DotDict(**world.level_data['rooms'])
    rooms = make_recursive_dotdict(world.level_data['rooms'])
    world.rooms = rooms
    world.rooms.current = get_room_at(world, 3, 3)
    update_current_room(world)

def make_recursive_dotdict(dct):
    res = DotDict(**dct)
    for k, v in dct.items():
        if type(v) is dict:
            res.set(k, make_recursive_dotdict(v))
    return res

def get_room_at(world, x, y):
    tile = world.old_map[y][x]
    if world.rooms.contain(tile):
        room = world.rooms.get(tile)
        return room
    return world.rooms.current

def update_current_room(world):
    old_room = world.rooms.current
    new_room = get_room_at(world, world.player.x, world.player.y)
    if old_room != new_room:
        world.rooms.current = new_room
        send_to_main_log(world.messages, 'Вхожу в ' + new_room.name)

def init_states():
    stateSystem.addState('walk') 
    stateSystem.addState('open_door') 
    stateSystem.addState('inventory') 
    stateSystem.addState('direction') 
    stateSystem.addState('inventory_view_object') 
    stateSystem.changeState('walk')
    stateSystem.setEventHandler('walk', 'keypress', walk_keypress)
    stateSystem.setEventHandler('walk', 'draw', draw_walk)
    stateSystem.setEventHandler('open_door', 'keypress', door_open_keypress)
    stateSystem.setEventHandler('open_door', 'draw', draw_walk)
    stateSystem.setEventHandler('direction', 'keypress', direction_keypress)
    stateSystem.setEventHandler('direction', 'draw', draw_walk)
    stateSystem.setEventHandler('inventory', 'draw', draw_inventory)
    stateSystem.setEventHandler('inventory', 'keypress', inventory_keypress)
    stateSystem.setEventHandler('inventory_view_object', 'draw', draw_object_info)
    stateSystem.setEventHandler('inventory_view_object', 'keypress', wait_keypress)

def do_take(_, world):
    log_msg('Взять откуда?', world)
    direction_do(world, take_from)

def inventory_add(obj, inventory):
    inventory.append(obj)

def take_from(x, y, world, _):
    obj = object_at_xy(x, y, world.objects)
    if obj:
        if obj.takeable:
            log_msg('Беру ' + obj.name, world)
            send_to_main_log(world.messages, 'Я взял ' + obj.name)
            inventory_add(obj, world.inventory)
            remove_obj(obj, world.objects)
        else:
            if obj.contain: # пока не содержат более одного объекта
                contaiment = obj.contain[0]
                log_msg('Беру из {} {}'.format(obj.name, contaiment.name), world)
                send_to_main_log(world.messages, 'Я взял {} из {}'.format(contaiment.name, obj.name))
                obj.contain = False
                inventory_add(contaiment, world.inventory)
            else:
                log_msg('Это нельзя брать.', world)
    else:
        log_msg('Здесь нечего брать.', world)

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
    applicator = applicator[0]
    object_apply(applicator, pacient)
    send_to_main_log(world.messages, 
            "Пытаюсь применить {} к {}...".format(applicator.name, pacient.name))# не должен быть .messages?

def object_apply(applicator, pacient):
    pass

def inventory_view_action(world, obj):
    world.messages.object_info = list()
    world.messages.object_info.append(obj.name)
    world.messages.object_info.append(obj.info_msg)
    stateSystem.changeState('inventory_view_object')

def go_inventory(key_sym, world):
    stateSystem.changeState('inventory')
    world.inventory_action = key_sym

def draw_object_info(world):
    draw_lines_tex(world.messages.object_info, 1, 1, (0, 1, 0.7))

def wait_keypress(key_sym, world):
    stateSystem.changeState('walk')

def inventory_keypress(key_sym, world):
    keyboard_fun = {
            'q':go_inventory,
            }
    if ord('1') <= ord(key_sym) <= ord('9'):
        selected = ord(key_sym) - ord('1')
        do_inventory_action(world, world.inventory_action, selected)
        return
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        fun(key_sym, world)
    stateSystem.changeState('walk')

def direction_do(world, fun, *args):
    world.direction_action = fun
    world.direction_args = args
    stateSystem.changeState('direction')

def direction_keypress(key_sym, world):
    direction = get_direction(key_sym)
    if direction:
        x, y = direction
        x = world.player.x + x
        y = world.player.y + y
        world.direction_action(x, y, world, world.direction_args)
        stateSystem.changeState('walk')
    else:
        log_msg('Неправильное направление. ', world)

def walk_keypress(key_sym, world):
    keyboard_fun = {
            'j':go_down,
            'k':go_up,
            'h':go_left,
            'l':go_right,
            'o':door_action_start,
            'c':door_action_start,
            's':do_search,
            'i':go_inventory,
            ',':do_take,
            'v':go_inventory,
            'a':go_inventory,
            }
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        fun(key_sym, world)
        update_current_room(world)

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

def door_open_keypress(key_sym, world):
    open_msg = ' '
    open_messages = {
            OPEN_NEED_KEY: 'Нужен ключ',
            OPEN_OPEND: 'Дверь открыта',
            OPEN_CLOSED: 'Дверь закрыта',
            OPEN_CANNOT:'это нельзя открыть',
            OPEN_NODOOR:'тут нет двери',
            }
    direction = get_direction(key_sym)
    if direction:
        x, y = direction
        open_status, obj = try_open_door(x, y, world.player, world.objects)
        open_msg = open_messages[open_status]
        if open_status == OPEN_OPEND:
            send_to_main_log(world.messages, 'Я открыл {}'.format(obj.name))
        if open_status == OPEN_CLOSED:
            send_to_main_log(world.messages, 'Я закрыл {}'.format(obj.name))
    stateSystem.changeState('walk')
    log_msg(open_msg, world)

def door_action_start(key_sym, world): #передавать stateSys? объект у кот вызывать? передавать функ?
    if key_sym == 'o':
        log_msg('Открыть дверь в какой стороне?', world)
    else:
        log_msg('Закрыть дверь в какой стороне?', world)
    stateSystem.changeState('open_door')

def ReSizeGLScene(Width, Height):
    state.w = w = Width
    state.h = h = Height
    if Height == 0:                     
        Height = 1
    glViewport(0, 0, Width, Height)     
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, h, 0, 100.0, -100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def step(d):
    color_mul_step(state.world.colors)
    glutPostRedisplay()
    glutTimerFunc(33, step, 1)

def update(world):
    world.messages.view_msg = describe_view(world.player, world.old_map, world.objects_data)

def describe_view(actor, amap, objects_data):
    chars = chars_in_view(actor, amap)
    return chars_describe(chars, objects_data)

def draw_inventory(world):
    i = 1
    for obj in world.inventory:
        line = "{}: {}({})".format(i, obj.name, obj.char)
        i += 1
        clr = obj.color
        draw_chars_tex(line, y=i, x=1, color=clr)

def draw_walk(world):
    draw_map(world.map, world.colors)
    draw_objects(world.objects)
    draw_help(world.messages.help_mgs)
    draw_view(world.messages)
    draw_main_log(world.messages)

def gl_draw_pre():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    
    glDisable(GL_CULL_FACE)             
    glShadeModel(GL_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_DEPTH_TEST)
    glColor4f(0, 1, 1, 0.5)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

def gl_error_msg():
    err = glGetError()
    if err:
        print(err, gluErrorString(err))
    glutSwapBuffers()

def DrawGLScene():
    gl_draw_pre()
    stateSystem.handleEvent('draw', state.world)
    #draw(state.world)
    gl_error_msg()

def keyPressed(*args):
    if args[0] == ESCAPE:
        sys.exit()
    key_sym = bytes.decode(args[0])
    stateSystem.handleEvent('keypress', key_sym, state.world)
    update(state.world) # handle update

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        glutPostRedisplay()

def motion(x, y):
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    state.window = glutCreateWindow("")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutTimerFunc(33, step, 1)
    InitGL(640, 480)
    init()
    glutMainLoop()

if __name__=='__main__':
    main()
