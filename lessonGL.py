from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
from PIL import Image

ESCAPE = b'\033'
window = 0

def lines():
    pass

def initFont(name, w, h): # -> fontId
    image = Image.open(name)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    tid = texture_init(image, ix, iy)
    col_count = ix // w
    row_count = iy // h
    return {'tid':tid,
            'col':col_count,
            'row':row_count,
            'w':w,
            'h':h,
            'width':ix,
            'height':iy,
            }

def font_coord_to_tex_coord(fid, x, y):
    w = fid['w'] + 1
    h = fid['h'] + 1
    width = fid['width']
    height = fid['height']
    s, t = x, y
    x *= w
    y *= h
    x = x/width
    y = 1.0 - y/height
    s = (s+1) * w 
    t = (t+1) * w 
    s = s/width
    t = 1.0 - t/height
    return x, t, s, y

def say_2dfont(font_id, msg): 
    tid = font_id['tid']
    col = font_id['col']
    glColor3f(1.0, 1.0, 1.0)
    x = window_width
    x /= 30
    y = x
    left = -40.0
    for char in msg:
        code = ord(char) - ord('a')
        xx = code % col
        yy = code // col
        a, b, s, t = font_coord_to_tex_coord(font_id, xx, yy)
        print(msg, char, code, x, a,b,s,t)
        glBindTexture(GL_TEXTURE_2D, tid)   
        glBegin(GL_QUADS)                   
        glTexCoord2f(a, b)
        glVertex3f(left-x, -y, 0.0)         
        glTexCoord2f(a, t)
        glVertex3f(left - x, y, 0.0)          
        glTexCoord2f(s, t)
        glVertex3f(left + x, y, 0.0)           
        glTexCoord2f(s, b)
        glVertex3f(left + x, -y, 0.0)          
        glEnd()
        left += 10

def texture_init(data, w, h):
    t = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, t)   
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    return t


def loadTexture(name):
    image = Image.open(name)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    #conver to BMP?
    t = texture_init(image, ix, iy)
    return t


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

    global texture, texturebg, font
    texture = loadTexture('font0.png')
    texturebg = loadTexture('bg.png')
    font = initFont('font0.png', 32, 32)
    glEnable(GL_TEXTURE_2D)


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
    global rotx, ic
    rotx += 5.0
    ic = random.random()*3.0
    glutPostRedisplay()
    glutTimerFunc(33, step, 1)

rotx = 0.0
ic = 1.0
texture = 0
texturebg = 0

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    
    glDisable(GL_LIGHTING)
    glDisable(GL_CULL_FACE)             
    glDisable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    #glAlphaFunc(GL_GEQUAL, 0.0625)
    #glEnable(GL_ALPHA_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_COLOR, GL_ONE)
#    glBlendFunc(GL_ONE, GL_SRC_COLOR)

    glColor3f(0, 0, 1.0)            
    glRectf(px, py,px+1,py+1)
    
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

    glLoadIdentity()                    
    glTranslatef(50.0, 50.0, -0.1)
    glColor3f(1.0, 1.0, 1.0)
    x = window_width
    x /= 4
    glBindTexture(GL_TEXTURE_2D, texture)   
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

    say_2dfont(font, "abcde")

    drawBg()

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
    glBindTexture(GL_TEXTURE_2D, texturebg)   
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
    #glutFullScreen()
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