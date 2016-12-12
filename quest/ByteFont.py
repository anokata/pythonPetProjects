from PIL import Image
from OpenGL.GL import *
from gl_texture import texture_init, draw_tex_quad

current_font = None

def init_font(name, char_width, char_height): # -> fontId
    imagep = Image.open(name)
    ix = imagep.size[0]
    iy = imagep.size[1]
    image = imagep.tobytes("raw", "RGBA", 0, -1)
    col_count = ix // char_width
    row_count = iy // char_height
    chars = dict()
    chars_tex = dict()
    code = 1

    char_win_w = char_width 
    char_win_h = char_height 

    for y in range(0, row_count * char_height, char_height):
        for x in range(0, col_count * char_width, char_width):
            i = imagep.crop((x,y, x + char_width, y + char_height))
            char_bytes = i.tobytes("raw", "RGBA", 0, -1)
            chars[code] = char_bytes
            tex = texture_init(char_bytes, char_width, char_height)
            chars_tex[code] = tex
            code += 1

    return {
            'col':col_count,
            'row':row_count,
            'w':char_width,
            'h':char_height,
            'width':ix,
            'height':iy,
            'img': image,
            'chars':chars,
            'chars_tex':chars_tex,
            'cw' : char_win_w,
            'ch' : char_win_h,
            }

def set_font(font):
    global current_font
    current_font = font

def gl_draw_char(data, w, h):
    glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)   

def gl_draw_char_tex(font, code, x, y, color=(1,0,0)):
    glColor3f(*color)
    w = font['w']
    h = font['h']
    draw_tex_quad(font['chars_tex'][code],x,y,x+w,y+h )

def draw_chars_tex(s, x=0, y=0, color=(0,0,1)):
    return draw_chars_tex_font(current_font, s, x, y, color)

def draw_chars_tex_font(font, s, x=0, y=0, color=(0,0,1)):
    dw = font['w']
    dh = font['h']
    cw = font['cw']
    ch = font['ch']
    y *= ch
    x *= cw
    cy = y
    cx = x
    for c in s:
        if c == '\n':
            cy += ch
            cx = x
            continue
        code = ord(c)
        gl_draw_char_tex(font, code, cx, cy, color)
        cx += cw

def draw_char(font, code):
    w = font['w']
    h = font['h']
    data = font['chars'][code]
    gl_draw_char(data, w, h)

def draw_chars(font, s, x=0, y=0):
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    dw = font['w']
    dh = font['h']
    cw = font['cw']
    ch = font['ch']
    y += 1
    y *= ch
    x *= cw

    for c in s:
        code = ord(c)
        glRasterPos2d(x, y)
        data = font['chars'][code]
        glDrawPixels(dw, dh, GL_RGBA, GL_UNSIGNED_BYTE, data)   
        x += cw
