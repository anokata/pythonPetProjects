from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

ESCAPE = b'\033'

# Number of the glut window.
window = 0

def InitGL(Width, Height):				
    glClearColor(0.0, 0.0, 0.0, 0.0)	
    glClearDepth(1.0)					
    glDepthFunc(GL_LESS)				
    glEnable(GL_DEPTH_TEST)				
    glShadeModel(GL_SMOOTH)				
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
    if Height == 0:						
	    Height = 1
    glViewport(0, 0, Width, Height)		
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()					
	glTranslatef(-1.5, 0.0, -6.0)
	glBegin(GL_POLYGON)                 
	glColor3f(1.0, 0.0, 0.0)            
	glVertex3f(0.0, 1.0, 0.0)           
	glColor3f(1.0, 0.0, 0.0)            
	glVertex3f(1.0, -1.0, 0.0)          
	glColor3f(1.0, 1.0, 0.0)            
	glVertex3f(-1.0, -1.0, 0.0)         
	glEnd()                             
	
	glTranslatef(3.0, 0.0, 0.0)
	glBegin(GL_QUADS)                   
	glVertex3f(-1.0, 1.0, 0.0)          
	glVertex3f(1.0, 1.0, 0.0)           
	glVertex3f(1.0, -1.0, 0.0)          
	glVertex3f(-1.0, -1.0, 0.0)         
	glEnd()                             

	glutSwapBuffers()

def keyPressed(*args):
    print(args, ESCAPE)
    if args[0] == ESCAPE:
	    sys.exit()

def main():
	global window
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("")
	glutDisplayFunc(DrawGLScene)
	#glutFullScreen()
	glutIdleFunc(DrawGLScene)
	glutReshapeFunc(ReSizeGLScene)
	glutKeyboardFunc(keyPressed)
	InitGL(640, 480)
	glutMainLoop()

main()
    	
