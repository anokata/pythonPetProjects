import sys
sys.path.append('../modules')
from StringUtil import *
red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
lgreen = (0.5, 1, 0.5)
gray = (0.5, 0.5, 0.5)
lred = (1, 0.5, 0.5)
lblue = (0.5, 0.5, 1)
white = (1, 1, 1)

def send_to_main_log(messages, msg, color=gray):
    for line in msg.split('\n'):
        if line.strip():
            messages.main_log.append((line, color))

def log_msg(msg, world):
    world.messages.log_msg = msg

def set_main_log(messages):
    global main_log
    main_log = messages

def log_main(msg, color=(0.5, 0.5, 0.5), wrap=33):
    for msg in msg.split('\n'):
        for line in wrap_string(msg, wrap).split('\n'):
            send_to_main_log(main_log, line, color)

