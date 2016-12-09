from OpenGL.GL import *

def texture_init(data, w, h):
    t = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, t)   
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 4)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    return t


def loadTexture(name):
    image = Image.open(name)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBA", 0, -1)
    #conver to BMP?
    t = texture_init(image, ix, iy)
    return t, image

def draw_tex_quad(tex, x, y, u, v):
    glBindTexture(GL_TEXTURE_2D, tex)   
    glBegin(GL_QUADS)                   
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, 0.0)         
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, v, 0.0)          
    glTexCoord2f(1.0, 0.0)
    glVertex3f(u, v, 0.0)           
    glTexCoord2f(1.0, 1.0)
    glVertex3f(u, y, 0.0)          
    glEnd()                             

def drawBg():
    x = state.w
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
