from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from mega import MutableNamedTuple
from line import *
from gl_skel import *
# TODO layers, lighting, rects blinks, symbols

def draw_line(line):
    glLoadIdentity()                    
    glTranslatef(0.1, 0.1, -2.0)
    glLineWidth(8)
    state = line[0]
    glColor3f(state.cr, state.cg, state.cb)
    glBegin(GL_LINE_STRIP)
    start = len(line) - state.display
    if start < 1 or not state.endable:
        start = 1
    for x, y in line[start:-1]:
        glVertex2f(x, y)
    glColor3f(1.0, 1.0, 1.0)
    x, y = line[-1]
    glVertex2f(x, y)
    glEnd()

data = MutableNamedTuple()
data.lines = list()
data.lines.append(create_line(w=100,h=100, g=1, b=0))
data.lines.append(create_line(w=100,h=100, x=100))
data.lines.append(create_line(w=100,h=100, y=100, r=1, b=0))
data.lines.append(create_line(w=100,h=100, y=100, x=100, r=0.4, b=0.4, g=0.4))
data.rotx = 0
data.roty = 0
data.rotz = 0

def step2(d):
    spd = 3
    data.rotx += spd
    data.roty += spd
    data.rotz += spd
    for l in data.lines:
        gen_line(l, 5)
    glutTimerFunc(1, step2, 1)
    glutPostRedisplay()

    

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    
    glShadeModel(GL_SMOOTH)
    glTranslatef(50, 50, -10)
    glRotatef(50, 1, 1, 0)
    #glRotatef(data.rotx, 1, 0, 0)
    #glRotatef(data.roty, 0, 1, 0)
    #glRotatef(data.rotz, 0, 0, 1)
    draw_axis()
    draw_grid()

    for l in data.lines:
        draw_line(l)

    glutSwapBuffers()

def keyPressed(*args):
    print(args, ESCAPE)
    if args[0] == ESCAPE:
        sys.exit()

def main():
    init_window()
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    glutTimerFunc(3, step2, 1)

    glutReshapeFunc(ReSizeGLScene)
    InitGL(640, 480)
    glutMainLoop()

if __name__=='__main__':
    main()
