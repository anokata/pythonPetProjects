from ByteFont import *

def mul_color(cl, color_multiplier):
    r, g, b = cl
    r *= color_multiplier
    g *= color_multiplier
    b *= color_multiplier
    return (r, g, b)

def draw_map(lines, colors):
    t = 0
    cl = (0.0, 0.3, 0.4)
    cl = mul_color(cl, colors.color_multiplier)
    for line in lines:
        draw_chars_tex(line, y=t, color=cl)
        t += 1

def color_mul_step(colors): 
    if colors.color_multiplier_dir:
        colors.color_multiplier += 0.1
    else:
        colors.color_multiplier -= 0.1
    if colors.color_multiplier > 1.3:
        colors.color_multiplier_dir = False 
    if colors.color_multiplier < 0.7:
        colors.color_multiplier_dir = True 

def draw_objects(objects):
    for o in objects:
        clr = tuple(o.color)
        draw_chars_tex(o.char, y=o.y, x=o.x, color=clr)

def draw_help(help_mgs):
    draw_chars_tex(help_mgs, y=0, x=27, color=(1.0, 1, 1))

def draw_view(messages):
    draw_chars_tex(messages.view_msg, y=25, x=1, color=(0, 0.5, 1))
    draw_chars_tex(messages.log_msg, y=20, x=1, color=(0.9, 0.5, 0.1))
