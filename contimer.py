#!/usr/bin/env python
# Таймер непрерывности

from subprocess import getoutput as exc
import curses
from curses import wrapper
import datetime
# global
class State:
    started = False
    time_started = 0
    records = []

    def toggle(self):
        self.started = not self.started
        # just started
        if self.started:
            self.time_started = datetime.datetime.now()
        else:
        # stopped
            delta = self.get_delta()
            self.records.append(delta)
            # TODO save for day, limit 20 rec


    def get_delta(self):
        now = datetime.datetime.now()
        return now - self.time_started

state = State()

def preczeroformat(a):
    a = int(a)
    if a < 10:
        return "0{}".format(a)
    return str(a)

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    main_loop(stdscr)
    stdscr.refresh()

def main_loop(stdscr):
    while True:
        redraw(stdscr)
        isend = input_handle(stdscr)
        if isend:
            break


def input_handle(stdscr):
    global state
    c = stdscr.getch()
    if c == ord('q'):
        return True
    if c == ord(' '):
        state.toggle()

    return False

def redraw(stdscr):
    global state

    stdscr.clear()
    now = datetime.datetime.now()
    stdscr.addstr(0, 0, "(q) - Exit")
    stdscr.addstr(1, 0, "{}".format(get_datetimestr(now)))
    if state.started:
        stdscr.addstr(2, 0, "started: {}".format(get_datetimestr(state.time_started)), curses.color_pair(1))
        delta = state.get_delta()
        stdscr.addstr(3, 0, "past: {}".format(get_timestr(delta)), curses.color_pair(3))
    else:
        stdscr.addstr(2, 0, "stoped", curses.color_pair(2))

    y = 4
    for r in state.records:
        y += 1
        stdscr.addstr(y, 0, "{}".format(get_timestr(r)))
        if y > 20: break


def get_timestr(d):
    return "{}:{}".format(d.seconds // 60, d.seconds % 60)

def get_datetimestr(d):
    return "{}:{}:{}".format(d.hour, preczeroformat(d.minute), preczeroformat(d.second))


wrapper(main)
