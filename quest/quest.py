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

def load_map(map_file, world):
    world.level_data = yaml.load(open(map_file)) # map load method, from string?
    world.map = world.level_data['map'][0].split('\n')
    world.map_width = len(world.map[0])
    world.map_height = len(world.map)
    world.old_map = world.level_data['map'][0].split('\n')
    world.map = [line for line in world.map if line != '']
    world.old_map = [line for line in world.old_map if line != '']
    world.objects = list()
    world.level_data['objects']
    world.objects_data = world.level_data['objects']
    world.objects += extract_objects(world.map, world.objects_data)
    spawn = object_by_char(world.objects, '@')
    world.player = make_actor(name='self', x=spawn.x, y=spawn.y, color=(0,1,1), char='\x01')
    remove_obj(spawn, world.objects)
    world.objects.append(world.player)
    # state = {'map': yaml.load(... #TODO переделать в виде явных данных
    #           'player' : make_actor ... 
    world.map = retile_map(world.map, world.level_data['map_tiles'])
    init_messages(world)
    load_rooms(world)
    log_msg(world.level_data['mapname'], world)
    send_to_main_log(world.messages, world.level_data['start_msg'])

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

def init_colors(world):
    colors = DotDict()
    colors.color_multiplier = 1.0
    colors.color_multiplier_dir = True
    world.colors = colors

def load_rooms(world):
    rooms = make_recursive_dotdict(world.level_data['rooms'])
    world.rooms = rooms
    world.rooms.current = get_room_at(world, 3, 3)
    update_current_room(world)

def init_map(map_file):
    world = DotDict()
    state.world = world
    world.stateSystem = stateSystem
    load_map(map_file, world)
    init_colors(world)
    world.inventory = list()
    world.inventory.append(get_object(world.objects_data, 'a')) # init inv in map?plr?

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
##---##
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
    glutTimerFunc(100, step, 1)

def update(world):
    world.messages.view_msg = describe_view(world.player, world.old_map, world.objects_data)

def describe_view(actor, amap, objects_data):
    chars = chars_in_view(actor, amap)
    return chars_describe(chars, objects_data)

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
    if ord(args[0]) > 127:
        print('Switch to Latin keyboard layout. Переключите на латинскую раскладку.')
        return
    key_sym = bytes.decode(args[0])
    stateSystem.handleEvent('keypress', key_sym, state.world)
    update(state.world) # handle update

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        glutPostRedisplay()

def motion(x, y):
    pass

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    state.window = glutCreateWindow("")
    glutDisplayFunc(DrawGLScene)
    #glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    #glutMouseFunc(mouse)
    #glutMotionFunc(motion)
    glutTimerFunc(100, step, 1)
    InitGL(640, 480)
    init()
    glutMainLoop()

if __name__=='__main__':
    main()
