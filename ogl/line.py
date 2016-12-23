from mega import MutableNamedTuple
import random

def create_line(x=0, y=0, w=30, h=30, r=0, g=0, b=1):
    line = list()
    state = MutableNamedTuple()
    state.dir = 'r'
    state.w = w
    state.h = h
    state.cr = r
    state.cg = g
    state.cb = b
    state.display = 10
    state.endable = random.choice([True, False])
    line.append(state)
    line.append((x, y))
    line.append((x+1, y))
    return line

def step_line(line):
    direction = line[0].dir
    state = line[0]
    x, y = line[-1]
    if direction == 'r':
       x += 1 
    if direction == 'l':
       x -= 1 
    if direction == 'u':
       y += 1 
    if direction == 'd':
       y -= 1 
    if x < 0:
        x = 0
        line[0].dir = 'r'
    if y < 0:
        y = 0
        line[0].dir = 'u'
    if x > state.w:
        x = state.w
        line[0].dir = 'l'
    if y > state.h:
        y = state.h
        line[0].dir = 'd'
    line[-1] = (x, y)
    return line

def turn_line(line):
    cur_dir = line[0].dir
    if cur_dir in {'r', 'l'}:
        direction = random.choice(['u', 'd'])
    else:
        direction = random.choice(['r', 'l'])
    x, y  = line[-1]
    if x == 0 and direction == 'l':
        direction = 'r'
    if y == 0 and direction == 'd':
        direction = 'u'
    line[0].dir = direction
    line.append(line[-1])
    return line

def gen_line(line, n):
    turn_chance = 0.1
    for i in range(n):
        is_turn = random.random() < turn_chance
        if is_turn:
            turn_line(line)
        else:
            step_line(line)
