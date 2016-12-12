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
#TODO: Надобы отрефакторить и писать тесты.

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
ESQ - выход
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
    state.level_data = yaml.load(open(map_file))
    state.map = state.level_data['map'][0].split('\n')
    state.old_map = state.level_data['map'][0].split('\n')
    state.map = [line for line in state.map if line != '']
    state.old_map = [line for line in state.old_map if line != '']
    state.player = make_actor(name='self', x=3, y=3, color=(0,1,1), char='\x01')
    state.objects = list()
    state.level_data['objects']
    state.objects_data = state.level_data['objects']
    state.objects += extract_objects(state.map, state.objects_data)
    state.objects.append(state.player)
    # state = {'map': yaml.load(... #TODO переделать в виде явных данных
    #           'player' : make_actor ... 
    state.map = retile_map(state.map, state.level_data['map_tiles'])
    state.messages = DotDict()
    state.messages.view_msg = 'none'
    state.messages.log_msg = 'log:'
    state.inventory = list()
    state.colors = DotDict()
    state.colors.color_multiplier = 1.0
    state.colors.color_multiplier_dir = True
    state.help_mgs = help_mgs
    state.world = DotDict()
    state.world.map = state.map
    state.world.old_map = state.old_map
    state.world.player = state.player
    state.world.objects = state.objects

def init_states():
    stateSystem.addState('walk') 
    stateSystem.addState('open_door') 
    stateSystem.changeState('walk')
    stateSystem.setEventHandler('walk', 'keypress', walk_keypress)
    stateSystem.setEventHandler('open_door', 'keypress', door_open_keypress)

def walk_keypress(key_sym):
    keyboard_fun = {
            'j':go_down,
            'k':go_up,
            'h':go_left,
            'l':go_right,
            'o':door_action_start,
            'c':door_action_start,
            's':do_search,
            }
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        fun(key_sym, state.world)

def do_search(_, world): #log:
    objs = objects_in_view(world.player, world)
    found = ''
    for obj in objs:
        if obj.contain:
            for obj_in_container in obj.contain:
                found += (obj.name + ' содержит ' + obj_in_container.name)
    if not found:
        log_msg('Ничего необычного')
    else:
        log_msg(found)

def door_open_keypress(key_sym):
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
        opend = try_open_door(x, y, state.player, state.objects)
    stateSystem.changeState('walk')
    log_msg(opend)

def door_action_start(key_sym, world): #передавать stateSys? объект у кот вызывать? передавать функ?
    if key_sym == 'o':
        log_msg('Открыть дверь в какой стороне?')
    else:
        log_msg('Закрыть дверь в какой стороне?')
    stateSystem.changeState('open_door')

def log_msg(msg): #state
    state.messages.log_msg = msg

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
    color_mul_step(state.colors)
    glutPostRedisplay()
    glutTimerFunc(33, step, 1)

def update_view(actor, amap, objects_data): # join? in_view
    chars = chars_in_view(actor, amap)
    return chars_describe(chars, objects_data)

def draw_view(): #state view upd
    state.messages.view_msg = update_view(state.player, state.old_map, state.objects_data)
    draw_chars_tex(state.messages.view_msg, y=25, x=1, color=(0, 0.5, 1))
    draw_chars_tex(state.messages.log_msg, y=20, x=1, color=(0.9, 0.5, 0.1))
        
def draw():
    draw_map(state.map, state.colors)
    draw_objects(state.objects)
    draw_help(state.help_mgs)
    draw_view()

def DrawGLScene():
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
    #draw_chars(state.font, '\x82\x81\x83', y=1, x=1)
    #draw_chars_tex(state.font, 'abc')
    #draw_chars_tex(state.font, 'abc', x=3, color=(0.5, 0.5, 0))
    #draw_chars(state.font, 'abc xyz ABC XYZ \x83\x81', y=3, x=0)
    draw()
    err = glGetError()
    if err:
        print(err, gluErrorString(err))
    glutSwapBuffers()

def keyPressed(*args):
    if args[0] == ESCAPE:
        sys.exit()
    key_sym = bytes.decode(args[0])
    stateSystem.handleEvent('keypress', key_sym)

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
