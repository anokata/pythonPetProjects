import curses
import time
# mvc

class Char:

    def __init__(self, char, color):
        self.char = char
        self.color = color

class Colors:
    pass

#class Snake

class App:
    colors = Colors()
    width = 20
    height = 40
    win = None
    snake = list()
    snake_char = 'S'
    snake_dir = 's'

    def main(stdscr):
        App.win = stdscr
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        App.colors.cl_bwhite = curses.color_pair(2) | curses.A_BOLD
        App.colors.cl_dwhite = curses.color_pair(2) | curses.A_DIM
        App.colors.cl_nwhite = curses.color_pair(2)
        App.snake_color = curses.color_pair(1) | curses.A_BOLD
        stdscr.clear()
        curses.curs_set(False)

        App.field = {(x,y):z for x in range(App.width) 
            for y in range(App.height) for z in [Char('.', App.colors.cl_nwhite)]}
        App.snake = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5)]

        App.draw_field(App.field)
        stdscr.refresh()

        notEnd = True
        App.win.nodelay(True)
        while notEnd:
            App.update()
            App.draw_field(App.field)
            stdscr.refresh()
            time.sleep(0.2)

            key = App.win.getch()
            if key == curses.ERR:
                continue
            if chr(key) in ('w', 'a', 's', 'd'):
                App.snake_dir = chr(key)
            notEnd = key != ord('q')

    def __init__(self):
        curses.wrapper(App.main)

    def update():
        last_segment = App.snake[0]
        x, y = last_segment
        dir_func = {
                's': lambda x, y : (x + 1, y),
                'w': lambda x, y : (x - 1, y),
                'a': lambda x, y : (x, y - 1),
                'd': lambda x, y : (x, y + 1),
                }
        fun = dir_func[App.snake_dir]

        App.snake[0] = fun(x, y)
        snake = App.snake
        a, b = x, y

        for i in range(1, len(App.snake)):
            x, y = snake[i]
            snake[i] = (a, b)
            a, b = x, y

    def draw_field(field):
        for x in range(App.width):
            for y in range(App.height):
                char = field[(x, y)].char
                color = field[(x, y)].color
                App.win.addstr(x, y, char, color)
        for s in App.snake:
            x, y = s
            App.win.addstr(x, y, App.snake_char, App.snake_color)


if __name__=='__main__':
     app = App()
