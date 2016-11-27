from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from PIL import Image

ESCAPE = b'\033'
window = 0


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

    image = Image.open('font0.png')
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    #conver to BMP?
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))   # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_TEXTURE_2D)


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
texture = 0
def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    
    glDisable(GL_LIGHTING)
    glDisable(GL_CULL_FACE)             
    glDisable(GL_TEXTURE_2D)

    glColor3f(0, 0, 1.0)            
    glRectf(px, py,px+1,py+1)
    glRotatef(rotx, 1, 1, 0)
    #glEnable(GL_LIGHTING)
    #glEnable(GL_BLEND)
    
    glTranslatef(0.1, 0.1, -2.0)
    #glColor4f(1.0, 1.0, 0.0, 0.5)            
    for x in range(1, int(window_width), 4):
        for y in range(1, int(window_width), 4):
            glColor3f(ic/x, 10.0/y, 0.0)            
            #glRectf(x, y, x+4, y+4)

    glLoadIdentity()                    
    glTranslatef(0.1, 0.1, -2.0)
    glLineWidth(8)
    glColor3f(0.2, 0.4, 1.0)
    glBegin(GL_LINE_STRIP)
    x = y = 0
    for i in range(10):
        x += random.random()*5
        y += random.random()*5
        glVertex2f(x, y)
    glEnd()

    glEnable(GL_TEXTURE_2D)
    #glEnable (GL_BLEND)
    #glBlendFunc (GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_CULL_FACE)             
    glLoadIdentity()                    
    glTranslatef(50.1, 50.1, -8.0)
    glColor3f(0, 0, 1.0)            
    #glShadeModel(GL_FLAT)
    #glShadeModel(GL_SMOOTH)
    #glutSolidTeapot(8)

    glLoadIdentity()                    
    glTranslatef(50.1, 50.1, -10.1)
    glColor4f(1.0, 0.0, 0.0, 0.5)            
    glRotatef(rotx, 1.0, 0.0, 0.0) 

    glDisable(GL_CULL_FACE)             
    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 0.0, 0.0, 0.5)            
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-10.0, -10.0, 0.0)         
    glColor4f(1.0, 0.0, 0.0, 0.5)            
    glTexCoord2f(1.0, 0.0)
    glVertex3f(10.0, -10.0, 0.0)          
    glColor4f(1.0, 1.0, 0.0, 0.5)            
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0.0, 10.0, 0.0)           
    glEnd()                             

    x = window_width
    x /= 2
    glLoadIdentity()                    
    glTranslatef(50.0, 50.0, -0.1)
    glBegin(GL_QUADS)                   
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, -x, 0.0)         
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x, x, 0.0)          
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, x, 0.0)           
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, -x, 0.0)          
    glEnd()                             

    err = glGetError()
    if err:
        print(err, gluErrorString(err))

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
        
