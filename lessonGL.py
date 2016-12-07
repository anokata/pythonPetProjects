from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from PIL import Image
from mega import MutableNamedTuple

ESCAPE = b'\033'
window = 0

def initFont(name, w, h): # -> fontId
    imagep = Image.open(name)
    ix = imagep.size[0]
    iy = imagep.size[1]
    image = imagep.tobytes("raw", "RGBX", 0, -1)
    col_count = ix // w
    row_count = iy // h

    char_width = w
    char_count = 3
    chars = dict()
    code = 0

    for y in range(0, char_count * char_width, char_width):
        for x in range(0, char_count * char_width, char_width):
            i = imagep.crop((x,y, x + char_width, y + char_width))
            char_bytes = i.tobytes("raw", "RGBX", 0, -1)
            chars[code] = char_bytes
            code += 1

    return {
            #'tid':tid,
            'col':col_count,
            'row':row_count,
            'w':w,
            'h':h,
            'width':ix,
            'height':iy,
            'img': image,
            'chars':chars
            }


def InitGL(Width, Height):              
    glClearColor(0.3, 0.3, 0.3, 1.0)    
    glClearDepth(1.0)                   
    glDepthFunc(GL_LESS)                
    glEnable(GL_DEPTH_TEST)             
    glShadeModel(GL_SMOOTH)             
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    global font
    font = initFont('font0.png', 32, 32)


font = 0
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
    glutPostRedisplay()
    glutTimerFunc(33, step, 1)

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    
    glDisable(GL_CULL_FACE)             
    glShadeModel(GL_SMOOTH)

    glColor3f(0, 0, 1.0)            
    glRectf(px, py,px+1,py+1)
    
    glTranslatef(50.0, 50.0, -0.1)
    glRasterPos2d(-50.0, -50.0)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glDrawPixels(128, 128, GL_RGBA, GL_UNSIGNED_BYTE, font['img'])   
    glRasterPos2d(-30.0, 0.0)
    #glPixelZoom(5.5,5.5)
    glDrawPixels(32, 32, GL_RGBA, GL_UNSIGNED_BYTE, font['chars'][1])   

    err = glGetError()
    if err:
        print(err, gluErrorString(err))

    glutSwapBuffers()

def drawBg():
    x = window_width
    x /= 2
    glLoadIdentity()                    
    glTranslatef(50.0, 50.0, -0.1)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)                   
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, -x, -10.0)         
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x, x, -10.0)          
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, x, -10.0)           
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, -x, -10.0)          
    glEnd()                             

def keyPressed(*args):
    print(args, ESCAPE)
    if args[0] == ESCAPE:
        sys.exit()

px = py = 0

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        a, b = glob_xy_calc(x,y)
        global px, py
        px = a
        py = b
        glutPostRedisplay()

def motion(x, y):
    glutPostRedisplay()

def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutTimerFunc(33, step, 1)
    InitGL(640, 480)
    glutMainLoop()

if __name__=='__main__':
    main()
    f = initFont('font0.png', 10,10)
    for i in range(12):
        #print(font_coord_to_tex_coord(f, i, i))
        pass
