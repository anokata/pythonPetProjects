#import curses
from curses import wrapper

def main(scr):
    scr.clear()
    scr.addstr(1,2, "heloha!")
    scr.refresh()
    scr.getkey()

wrapper(main)
