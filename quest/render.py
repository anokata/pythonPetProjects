from ByteFont import *
from map_util import *
import math
from collections import OrderedDict

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
                    if o.takeable:
                        continue
                    #clr = tuple(o.color) #TODO off lighting setting on key. world.settings
                    #if visible in dark? or is not passable
                draw_chars_tex(o.char, y=o.y, x=o.x, color=clr)
    o = world.player
    clr = tuple(o.color)
    draw_chars_tex(o.char, y=o.y, x=o.x, color=clr)


def is_lighted(x, y, world):
    return world.light_map.get((x, y), False)

def draw_help(world):
    draw_text(world.messages.help_mgs, y=0, x=world.map_width*1.7 + 1, color=(1.0, 1, 1))

def draw_side_info(world):
    if world.side_help:
        draw_help(world)
    else:
        draw_char_info(world)

def draw_char_info(world):
    update_char_info(world) #TODO update if надо
    draw_text(world.messages.char_info, y=0, x=world.map_width*1.7 + 1, color=(1.0, 1, 1))

def update_char_info(world):
    info = ''
    player = world.player
    dinfo = (
            'Голова\n  температура:{:.2f}',(player.head.temp,),
            'Тело\n  температура:{:.2f}',(player.body.temp,),
            '  сила:({:.2f}/{:.2f})',(player.body.strength, player.body.max_strength),
            '  выносливость:({:.2f}/{:.2f})',(player.body.stamina, player.body.max_stamina),
            'Руки\n  температура:{:.2f}',(player.arms.temp,),
            '  сила:({:.2f}/{:.2f})',(player.arms.strength, player.arms.max_strength),
            '  выносливость:({:.2f}/{:.2f})',(player.arms.stamina, player.arms.max_stamina),
            'Ноги\n  температура:{:.2f}',(player.legs.temp,),
            '  сила:({:.2f}/{:.2f})',(player.legs.strength, player.legs.max_strength),
            '  выносливость:({:.2f}/{:.2f})',(player.legs.stamina, player.legs.max_stamina),
            #'', (,),
            'Энегрия({:.2f}/{:.2f}/{:.2f})', (player.available_energy, player.max_available, player.stock_energy),
            'Время {}', (world.tick,),
            )
    for k, v in zip(dinfo[::2], dinfo[1::2]):
        info += k.format(*v) + '\n'
    world.messages.char_info = info

def draw_view(messages):
    draw_text(messages.log_msg, y=messages.log_y, x=1, color=(0.9, 0.5, 0.1))
    draw_text(messages.view_msg, y=messages.view_y, x=1, color=(0, 0.5, 1))

def draw_main_log(messages):
    y = messages.main_log_y
    for msg, color in get_last_main_log(messages):
        draw_text(msg, y=y, x=1, color=color)
        y += 1

def get_last_main_log(messages): #to log module
    return messages.main_log[-messages.main_log_maxview:]

def draw_object_info(world):
    draw_lines_text(world.messages.object_info, 1, 1, (0, 1, 0.7))

def draw_inventory(world):
    i = 1
    for obj in world.inventory:
        line = "{}: {}".format(i, obj.name)
        if obj.contain:
            pass
            line += "({})".format(obj.contain[0].name)
        i += 1
        clr = obj.color
        draw_text(line, y=i, x=1, color=clr)

def distance(a, b, c, d):
    return math.sqrt((a-c)*(a-c)+(b-d)*(b-d))

def _gen_ray(alpha, R):
    r = 0.5
    while r <= R:
        x, y = math.cos(math.radians(alpha))*r, math.sin(math.radians(alpha))*r
        r += 0.5
        yield int(x), int(y)

def get_ray(alpha, R):
    ray = list(_gen_ray(alpha, R))
    sray = list()
    for r in ray:
        if r not in sray:
            sray.append(r)
    return sray

def get_circle_rays(R): #TODO static calc
    rays = list()
    for alpha in range(0, 370, 10):
        rays.append(get_ray(alpha, R))
    return rays

def cast_rays(world):
    R = 8
    px = world.player.x #TODO get_player_pos
    py = world.player.y
    rays = list()
    for ray in get_circle_rays(R):
        new_ray = list()
        for x, y in ray:
            obj = object_at_xy(x + px, y + py, world.objects) #TODO just world?.get_objects
            if not obj:
                new_ray.append((x, y))
            elif obj.passable:
                new_ray.append((x, y))
            else:
                new_ray.append((x, y))
                break
        rays.append(new_ray)
    return rays

if __name__=='__main__':
    print(get_ray(30, 5)) #TODO TEST
    print(get_circle_rays(5))
