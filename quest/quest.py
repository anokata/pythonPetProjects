from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
sys.path.append('../modules')
import random
from mega import *
from ByteFont import *
from gl_main import *
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
font_file10x16 = 'font10x16.png'
def make_actor(**kwargs):
    stats_init={
            'temp':36.6,
            'strength':1,
            'max_strength':2,
            'stamina':3,
            'max_stamina':10,
            }
    actor = DotDict(**kwargs)
    actor.takeable = False
    actor.head = DotDict(temp=36.6, name='голова')
    actor.body = DotDict(**stats_init, name='тело')
    actor.arms = DotDict(**stats_init, name='руки')
    actor.legs = DotDict(**stats_init, name='ноги')
    actor.passable = True
    actor.available_energy = 5
    actor.max_available = 10
    actor.stock_energy = 5
    actor.live = True
    actor.water_level = 100 #100/100
    return actor

##new zone start##
##new zone end##
def init():
    state.font = init_font(font_file, 16, 16)
    state.font10x16 = init_font(font_file10x16, 10, 16)
    set_fonts(state.font, state.font10x16)
    init_map(map_file)
    init_states()

def init_player(world, x, y):
    world.player = make_actor(name='self', x=x, y=y, color=(0,1,1), char='\x01')
    add_object(world.objects, world.player)

def init_colors(world):
    colors = DotDict()
    colors.color_multiplier = 1.0
    colors.color_multiplier_dir = True
    world.colors = colors

def init_bed_spawn(world):
    spawn = object_by_char(world.objects, chr(21))
    sx, sy = spawn.x-1, spawn.y
    return sx, sy

def init_map(map_file):
    world = DotDict()
    world.tick = 0
    state.world = world
    world.stateSystem = stateSystem
    load_map(map_file, world)
    x, y = init_bed_spawn(world)
    init_player(world, x, y)
    init_colors(world)
    recalc_light(world)
    update_current_room(world)
    world.inventory = list()
    inventory_add(get_object(world, 'apple'), world.inventory)# init inv in map?plr?
    world.tick_events = make_recursive_dotdict(world.level_data['tick_events'])

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
            'm':do_smash,
            'J':do_warmup,
            'r':do_rest,
            'e':go_inventory,
            'H':help_turn,
            'W':go_inventory,
            }
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        fun(key_sym, world)
        update_current_room(world)
        recalc_light(world)

def do_rest(_, world):
    rest(1, world)
    log_main('Вы отдыхаете...', lgreen)

def help_turn(_, world):
    world.side_help = not world.side_help

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
        open_status, obj = try_open_door(world, x, y, world.player, world.objects)
        open_msg = open_messages[open_status]
        if open_status == OPEN_OPEND:
            log_main('Вы открыли {}'.format(obj.name))
        if open_status == OPEN_CLOSED:
            log_main('Вы закрыли {}'.format(obj.name))
    stateSystem.changeState('walk')
    log_msg(open_msg, world)

def step(d):
    color_mul_step(state.world.colors)
    glutPostRedisplay()
    glutTimerFunc(100, step, 1)

def update(world):
    world.messages.view_msg = describe_view(world)
    tick(world)

def describe_view(world):
    objs = objects_in_view(world.player, world)
    return describe_objects(objs, world)

def draw_walk(world):
    draw_map(world, world.colors) # почти не нужно
    draw_objects(world)
    draw_side_info(world)
    draw_view(world.messages)
    draw_main_log(world.messages)

##---##
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
    #print(key_sym, ord(args[0]))
    stateSystem.handleEvent('keypress', key_sym, state.world)
    update(state.world) # handle update

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        glutPostRedisplay()

def motion(x, y):
    pass

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
