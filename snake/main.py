from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
sys.path.append('../modules')
import random
from ByteFont import *
from gl_main import *
import stateSystem
import ByteFont

class State():
    pass 

state = State()
state.world = State()

def init():
    state.font = init_font(ByteFont.font_file, 16, 16)
    state.font10x16 = init_font(ByteFont.font_file10x16, 10, 16)
    set_fonts(state.font10x16, state.font)
    pass

def gl_draw_pre():
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

def gl_error_msg():
    err = glGetError()
    if err:
        print(err, gluErrorString(err))
    glutSwapBuffers()

def DrawGLScene():
    gl_draw_pre()
    stateSystem.handleEvent('draw', state.world)
    #draw(state.world)
    draw_chars_tex("hi", y=1, x=1, color=(0,1,0))
    gl_error_msg()

def keyPressed(*args):
    if args[0] == ESCAPE:
        sys.exit()
    if ord(args[0]) > 127:
        print('Switch to Latin keyboard layout. Переключите на латинскую раскладку.')
        return
    key_sym = bytes.decode(args[0])
    print(key_sym, ord(args[0]))
    stateSystem.handleEvent('keypress', key_sym, state.world)
    #update(state.world) # handle update

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        glutPostRedisplay()

def motion(x, y):
    pass

def step():
    pass

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

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    state.window = glutCreateWindow("")
    glutDisplayFunc(DrawGLScene)
    #glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutTimerFunc(100, step, 1)
    InitGL(640, 480)
    init()
    glutMainLoop()

if __name__=='__main__':
    main()
