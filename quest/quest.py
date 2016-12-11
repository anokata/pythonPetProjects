from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from mega import *
from ByteFont import *
from gl_texture import draw_tex_quad
from gl_main import *

import yaml
#TODO: объекты должны быть отдельно.
#TODO: Объекты цвет описания
#TODO Rend: glow, loop bright flick
#TODO инвентарь. возможность брать предметы, применять, комбинировать. 
#TODO Октрывать закрывать двери, замки, контейнеры, ключами.

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
'''

def make_actor(**kwargs):
    actor = DotDict(**kwargs)
    return actor

def get_object(x, y, amap, objects):
    char = amap[y][x]
    if char in objects:
        return objects[char]
    else:
        return {'pass':True}

def can_be_there(x, y, amap, objects):
    obj = get_object(x, y, amap, objects)
    return obj['pass']

def can_be_there_state(x, y):
    return can_be_there(x, y, state.old_map, state.objects_data)

def go_down():
    actor = state.player
    if can_be_there_state(actor.x, actor.y + 1):
        actor.y += 1

def go_up():
    actor = state.player
    if can_be_there_state(actor.x, actor.y - 1):
        actor.y -= 1

def go_left():
    actor = state.player
    if can_be_there_state(actor.x - 1, actor.y):
        actor.x -= 1

def go_right():
    actor = state.player
    if can_be_there_state(actor.x + 1, actor.y):
        actor.x += 1

def chars_in_view(actor, amap):
    w = len(amap[0])
    h = len(amap)
    chars = set()
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            x = actor.x + i
            y = actor.y + j
            if 0 <= x < w and 0 <= y < h:
                char = amap[y][x]
                if char not in ' ':
                    chars.add(char)
    return chars

def chars_describe(chars, objects):
    strings = 'Вижу:\n'
    for c in chars:
        if c in objects:
            strings += "     " + objects[c]['name'] + '(%s)\n'%c
    return strings

def retile_map(m, pairs):
    prs = dict(zip(pairs[::2], pairs[1::2]))
    prs = str.maketrans(prs)
    m = [line.translate(prs) for line in m]
    return m

def extract_objects(amap, objects_data, floor_char=' '):
    objects = list()
    for x in range(len(amap[0])):
        for y in range(len(amap)):
            char = amap[y][x]
            if char in objects_data:
                obj = DotDict(x=x, y=y, char=char)
                obj.update(objects_data[char])
                if type(obj.char) is int:
                    obj.char = chr(obj.char)
                objects.append(obj)
                amap[y] = amap[y][:x] + floor_char + amap[y][x+1:]
    return objects

        
def init():
    font = init_font(font_file, 16, 16)
    state.font = font
    state.level_data = yaml.load(open(map_file))
    state.map = state.level_data['map'][0].split('\n')
    state.old_map = state.level_data['map'][0].split('\n')
    state.map = [line for line in state.map if line != '']
    state.old_map = [line for line in state.old_map if line != '']
    state.player = make_actor(x=3, y=3, color=(0,1,1), char='\x01')
    state.objects = list()
    state.level_data['objects']
    state.objects_data = state.level_data['objects']
    state.objects += extract_objects(state.map, state.objects_data)
    state.objects.append(state.player)
    #print(state.objects_data)
    #print(state.objects)
    # state = {'map': yaml.load(...
    #           'player' : make_actor ... 
    state.map = retile_map(state.map, state.level_data['map_tiles'])
    state.messages = DotDict()
    state.messages.view_msg = 'none'
    state.inventory = list()

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
    glutPostRedisplay()
    glutTimerFunc(33, step, 1)

def draw_map(lines):
    t = 0
    for line in lines:
        draw_chars_tex(state.font, line, y=t, color=(1.0, 0.3, 0.4))
        t += 1

def draw_objects(objects):
    for o in objects:
        clr = tuple(o.color)
        draw_chars_tex(state.font, o.char, y=o.y, x=o.x, color=clr)

def draw_help():
    draw_chars_tex(state.font, help_mgs, y=0, x=27, color=(1.0, 1, 1))

def update_view(actor, amap, objects_data):
    chars = chars_in_view(actor, amap)
    return chars_describe(chars, objects_data)

def draw_view():
    state.messages.view_msg = update_view(state.player, state.old_map, state.objects_data)
    draw_chars_tex(state.font, state.messages.view_msg, y=20, x=1, color=(0, 0.5, 1))
        
def draw():
    draw_map(state.map)
    draw_objects(state.objects)
    draw_help()
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
    #print(args, args[0], key_sym)
    keyboard_fun = {
            'j':go_down,
            'k':go_up,
            'h':go_left,
            'l':go_right,
            }
    fun = keyboard_fun.get(key_sym, False)
    if fun:
        fun()

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
