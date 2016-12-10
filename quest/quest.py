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

state = MutableNamedTuple()
state.window = 0
map_file = 'map.yaml'
font_file = 'font1.png'
help_mgs = ''

def make_actor(**kwargs):
    actor = DotDict(**kwargs)
    return actor

def go_down():
    actor = state.player
    actor.y += 1

def go_up():
    actor = state.player
    actor.y -= 1

def go_left():
    actor = state.player
    actor.x -= 1

def go_right():
    actor = state.player
    actor.x += 1

def init():
    font = init_font(font_file, 16, 16)
    state.font = font
    state.map = yaml.load(open(map_file))
    state.map['map'] = state.map['map'][0].split('\n')
    print(state.map)
    state.player = make_actor(x=0, y=0, char='\x01')
    print(state.player)
    state.objects = list()
    state.objects.append(state.player)
    # state = {'map': yaml.load(...
    #           'player' : make_actor ... 

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
        draw_chars_tex(state.font, o.char, y=o.y, x=o.x, color=(0.0, 0.3, 1.0))
        

def draw():
    #draw_chars_tex(state.font, 'AZX\x82\x83\x81', y=1, color=(1.0, 0.5, 0))
    #draw_chars_tex(state.font, '.#', y=1, color=(1.0, 0.5, 0))
    draw_map(state.map['map'])
    draw_objects(state.objects)
    draw_chars_tex(state.font, chr(1024), y=19, color=(1.0, 0, 0))



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
    print(args, args[0], key_sym)
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
