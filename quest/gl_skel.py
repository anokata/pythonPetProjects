from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

ESCAPE = b'\033'
window = 0
window_width = 100.0
def ReSizeGLScene(Width, Height):
    persp = True
    persp = False
    if Height == 0:                     
        Height = 1
    glViewport(0, 0, Width, Height)     
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(Width)/float(Height)

    if persp:
        gluPerspective (130, 1, 50, 0)
    else:
        if Width <= Height:
            glOrtho(0.0, window_width, 0.0, window_width/aspect, 100.0, -100.0)
        else:
            glOrtho(0.0, window_width * aspect, 0.0, window_width, 100.0, -100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def InitGL(Width, Height):              
    glClearColor(0.0, 0.0, 0.0, 1.0)    
    glClearDepth(1.0)                   
    glDepthFunc(GL_LESS)                
    glEnable(GL_DEPTH_TEST)             
    glShadeModel(GL_SMOOTH)             
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

def init_window():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("")

def glLine(x, y, e, d):
    glBegin(GL_LINE_STRIP)
    glVertex2f(x, y)
    glVertex2f(e, d)
    glEnd()

def draw_axis():
    glLineWidth(2)
    glPushMatrix()
    #glLoadIdentity()                    
    glColor3f(1, 0, 0)
    glLine(-1000, 0, 1000, 0)
    glColor3f(0, 0, 1)
    glLine(0, -1000, 0, 1000)
    glColor3f(0, 1, 0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, -1000)
    glVertex3f(0, 0, 1000)
    glEnd()
    glPopMatrix()

def draw_grid():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    n = 20
    for x in range(-n//2+2, n//2-1):
        glVertex3f(x * 5, 0, n*2)
        glVertex3f(x * 5, 0, -n*2)
    for y in range(-n//2+2, n//2-1):
        glVertex3f(n*2, 0, y * 5)
        glVertex3f(-n*2, 0, y * 5)
        #glVertex2f(n*2, y * 5)
        #glVertex2f(-n*2, y * 5)
    glEnd()
