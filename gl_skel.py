from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

ESCAPE = b'\033'
window = 0
window_width = 100.0
def ReSizeGLScene(Width, Height):
    if Height == 0:                     
        Height = 1
    glViewport(0, 0, Width, Height)     
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(Width)/float(Height)
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

