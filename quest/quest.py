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

import yaml
#TODO Rend: glow(hard), loop bright flick(частично сделал, но нужно чтобы незвисимо было у разных объектов, и возможно по разным каналам rgb)
#TODO инвентарь. возможность брать предметы, применять, комбинировать. 
#TODO +Октрывать +закрывать двери, замки, контейнеры, ключами.
# как сделать объекты содержащие объекты?
#TODO книги, записки, подсказки. Мысли героя. Описание местности куда входит. Лог сообщений. разным цветом смысловые слова и объекты выделять.
#TODO когда идёт в стену, объект, писать в лог. (сообщения на событие движения в объект у объекта) Описание звуков действий.
#TODO: Надобы отрефакторить и писать тесты. выделить maingl

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
ESQ - выход
i - инвентарь
'''

def make_actor(**kwargs):
    actor = DotDict(**kwargs)
    return actor

def init():
    state.font = init_font(font_file, 16, 16)
    set_font(state.font)
    init_map()
    init_states()

def init_map():
    world = DotDict()
    state.world = world
    world.level_data = yaml.load(open(map_file))
    world.map = world.level_data['map'][0].split('\n')
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
    world.messages = DotDict()
    world.messages.view_msg = 'none'
    world.messages.log_msg = 'log:'
    world.messages.help_mgs = help_mgs
    colors = DotDict()
    colors.color_multiplier = 1.0
    colors.color_multiplier_dir = True
    world.colors = colors
    world.inventory = list()
    world.inventory.append(get_object(world.objects_data, 'cup'))
    world.inventory.append(get_object(world.objects_data, 'cup'))

def init_states():
    stateSystem.addState('walk') 
    stateSystem.addState('open_door') 
    stateSystem.addState('inventory') 
    stateSystem.changeState('walk')
    stateSystem.setEventHandler('walk', 'keypress', walk_keypress)
    stateSystem.setEventHandler('open_door', 'keypress', door_open_keypress)
    stateSystem.setEventHandler('inventory', 'keypress', inventory_keypress)
    stateSystem.setEventHandler('walk', 'draw', draw_walk)
    stateSystem.setEventHandler('open_door', 'draw', draw_walk)
    stateSystem.setEventHandler('inventory', 'draw', draw_inventory)

def go_inventory(_, world):
    stateSystem.changeState('inventory')

def inventory_keypress(key_sym, world):
    keyboard_fun = {
            'q':go_inventory,
            }
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
            }
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        fun(key_sym, world)


def door_open_keypress(key_sym, world):
    keyboard_fun = {
            'j':lambda _: (0, 1),
            'k':lambda _: (0, -1),
            'h':lambda _: (-1, 0),
            'l':lambda _: (1, 0),
            }
    fun = keyboard_fun.get(key_sym, False)
    opend = ' '
    if fun:
        x, y = fun(0)
        opend = try_open_door(x, y, world.player, world.objects)
    stateSystem.changeState('walk')
    log_msg(opend, world)

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
