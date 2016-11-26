from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from PIL import Image

ESCAPE = b'\033'
window = 0

img = Image.open('font0.png')

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


window_width = 100.0
w = h = 0

def glob_xy_calc(x, y):
    return xy_calc(x, y, w, h, window_width)

def xy_calc(x, y, w, h, ww):
    asp = w/h
    if w<=h:
        a = x/w*ww
        b = ((h-y)/h*ww)/asp
    else:
        a = (x/w*ww)*asp
        b = (h-y)/h*ww
    return a, b

def ReSizeGLScene(Width, Height):
    global w, h
    w = Width
    h = Height
    if Height == 0:                     
        Height = 1
    glViewport(0, 0, Width, Height)     
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(Width)/float(Height)
    #gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    if Width <= Height:
        glOrtho(0.0, window_width, 0.0, window_width/aspect, 100.0, -100.0)
    else:
        glOrtho(0.0, window_width * aspect, 0.0, window_width, 100.0, -100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def step(d):
    global rotx, ic
    rotx += 5.0
    ic = random.random()*3.0
    glutPostRedisplay()
    glutTimerFunc(33, step, 1)

rotx = 0.0
ic = 1.0
def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    
    glDisable(GL_LIGHTING)
    glDisable(GL_CULL_FACE)             

    glColor3f(0, 0, 1.0)            
    glRectf(px, py,px+1,py+1)
    glRotatef(rotx, 1, 1, 0)
    #glEnable(GL_LIGHTING)
    glEnable(GL_BLEND)
    
    glTranslatef(0.1, 0.1, -2.0)
    glColor4f(1.0, 1.0, 0.0, 0.5)            
    for x in range(1, int(window_width), 4):
        for y in range(1, int(window_width), 4):
            glColor3f(ic/x, 10.0/y, 0.0)            
            glRectf(x, y, x+4, y+4)


    glEnable(GL_CULL_FACE)             
    glLoadIdentity()                    
    glTranslatef(50.1, 50.1, -8.0)
    glColor3f(0, 0, 1.0)            
    #glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)
    glutSolidTeapot(8)

    glLoadIdentity()                    
    glTranslatef(50.1, 50.1, -0.1)
    glColor4f(1.0, 0.0, 0.0, 0.5)            

    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 0.0, 0.0, 0.5)            
    glVertex3f(0.0, 1.0, 0.0)           
    glColor4f(1.0, 0.0, 0.0, 0.5)            
    glVertex3f(1.0, -1.0, 0.0)          
    glColor4f(1.0, 1.0, 0.0, 0.5)            
    glVertex3f(-1.0, -1.0, 0.0)         
    glEnd()                             
    glTranslatef(1.0, 0.0, -0.1)
    glRotatef(rotx, 1.0, 0.0, 0.0) 
    glBegin(GL_QUADS)                   
    glColor4f(0.0, 1.0, 0.0, 0.5)            
    glVertex3f(-1.0, 1.0, 0.0)          
    glVertex3f(1.0, 1.0, 0.0)           
    glColor4f(0.0, 1.0, 1.0, 0.5)            
    glVertex3f(1.0, -1.0, 0.0)          
    glVertex3f(-1.0, -1.0, 0.0)         
    glEnd()                             

    glutSwapBuffers()

def keyPressed(*args):
    print(args, ESCAPE)
    if args[0] == ESCAPE:
        sys.exit()

px = py = 0

def mouse(button, state, x, y):
    print(button, state)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        a, b = glob_xy_calc(x,y)
        global px, py
        px = a
        py = b
        glutPostRedisplay()

def motion(x, y):
    print(x, y)
    glutPostRedisplay()

def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("")
    glutDisplayFunc(DrawGLScene)
    #glutFullScreen()
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutTimerFunc(33, step, 1)
    InitGL(640, 480)
    glutMainLoop()

main()
        
