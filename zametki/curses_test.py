import curses
# mvc


def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.clear()
    curses.curs_set(False)
    stdscr.addstr(10, 10, 'z' * 100)
    stdscr.addstr(0,0, "RED ALERT!", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(1,0, "RED ALERT!", curses.color_pair(1))
    stdscr.addstr(2,0, "RED ALERT!", curses.color_pair(1) | curses.A_DIM)

    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
