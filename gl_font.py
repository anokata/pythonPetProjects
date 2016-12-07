
def initFont(name, w, h): # -> fontId
    imagep = Image.open(name)
    ix = imagep.size[0]
    iy = imagep.size[1]
    image = imagep.tobytes("raw", "RGBX", 0, -1)
    tid = texture_init(image, ix, iy)
    col_count = ix // w
    row_count = iy // h


    return {
            #'tid':tid,
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
    glDisable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tid)   
    glLoadIdentity()                    
    glTranslatef(50.0, 50.0, -0.1)
    x = window_width
    x /= 30
    y = x
    left = -40.0
    for char in msg:
        code = ord(char) - ord('a')
        xx = code % col
        yy = code // col
        a, b, s, t = font_coord_to_tex_coord(font_id, xx, yy)
        #print(msg, char, code, x, a,b,s,t)
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
