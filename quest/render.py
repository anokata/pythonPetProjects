from ByteFont import *
from map_util import *
import math

dark_color = (0.3, 0.3, 0.3)

def mul_color(cl, color_multiplier):
    r, g, b = cl
    r *= color_multiplier
    g *= color_multiplier
    b *= color_multiplier
    return (r, g, b)

def draw_map(world, colors):
    t = 0
    cl = (0.0, 0.3, 0.4)
    cl = mul_color(cl, colors.color_multiplier)
    for y in range(world.map_height):
        line = ''
        for x in range(world.map_width):
            line += world.map[(x, y)]
        draw_chars_tex(line, y=t, color=cl)
        t += 1

def color_mul_step(colors): 
    coeff = 0.1
    if colors.color_multiplier_dir:
        colors.color_multiplier += coeff
    else:
        colors.color_multiplier -= coeff
    if colors.color_multiplier > 1.3:
        colors.color_multiplier_dir = False 
    if colors.color_multiplier < 0.7:
        colors.color_multiplier_dir = True 

def draw_objects(world):
    objects  = world.objects
    for x in range(world.map_width):
        for y in range(world.map_height):
            o = object_at_xy(x, y, objects)
            if o:
                if is_lighted(x, y, world):
                    clr = tuple(o.color)
                else:
                    clr = dark_color
                    clr = tuple(o.color) #
                    #if visible in dark? or is not passable
                draw_chars_tex(o.char, y=o.y, x=o.x, color=clr)

def is_lighted(x, y, world):
    return world.light_map.get((x, y), False)

def draw_help(help_mgs):
    draw_chars_tex(help_mgs, y=0, x=27, color=(1.0, 1, 1))

def draw_view(messages):
    draw_chars_tex(messages.log_msg, y=messages.log_y, x=1, color=(0.9, 0.5, 0.1))
    draw_chars_tex(messages.view_msg, y=messages.view_y, x=1, color=(0, 0.5, 1))

def draw_main_log(messages):
    y = messages.main_log_y
    for m in get_last_main_log(messages):
        draw_chars_tex(m, y=y, x=1, color=(0.5, 0.5, 0.5))
        y += 1

def get_last_main_log(messages): #to log module
    return messages.main_log[-messages.main_log_maxview:]


def draw_object_info(world):
    draw_lines_tex(world.messages.object_info, 1, 1, (0, 1, 0.7))

def draw_inventory(world):
    i = 1
    for obj in world.inventory:
        line = "{}: {}({})".format(i, obj.name, obj.char)
        i += 1
        clr = obj.color
        draw_chars_tex(line, y=i, x=1, color=clr)

def distance(a, b, c, d):
    return math.sqrt((a-c)*(a-c)+(b-d)*(b-d))

def make_ray_gen(ax, ay, bx, by, n):
    dx = (bx-ax)/n
    dy = (by-ay)/n
    while ax != bx and ay != by:
        ax += dx
        ay += dy
        yield (int(ax), int(ay))

#def ray_(
