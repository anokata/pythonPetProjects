#!/usr/bin/env python
# Таймер непрерывности

from subprocess import getoutput as exc
import curses
from curses import wrapper
import datetime

def preczeroformat(a):
    a = int(a)
    if a < 10:
        return "0{}".format(a)
    return str(a)

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    main_loop(stdscr)
    stdscr.refresh()

def main_loop(stdscr):
    while True:
        redraw(stdscr)
        isend = input_handle(stdscr)
        if isend:
            break


def input_handle(stdscr):
        c = stdscr.getch()
        if c == ord('q'):
            return True

        return False

def redraw(stdscr):
    stdscr.clear()
    now = datetime.datetime.now()
    stdscr.addstr(0, 0, "(q) - Exit")
    stdscr.addstr(1, 0, "{}:{}".format(now.hour, preczeroformat(now.minute)))


wrapper(main)
