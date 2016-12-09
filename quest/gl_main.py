from OpenGL.GL import *

ESCAPE = b'\033'

def InitGL(Width, Height):              
    glClearColor(0.3, 0.3, 0.3, 1.0)    
    glClearDepth(1.0)                   
    glDepthFunc(GL_LESS)                
    glEnable(GL_DEPTH_TEST)             
    glShadeModel(GL_SMOOTH)             
