import curses
import time

class Char:

    def __init__(self, char, color):
        self.char = char
        self.color = color

class Colors:
    pass

class Snake:
    char = 'S'
    UP = 'w'
    DOWN = 's'
    LEFT = 'a'
    RIGHT = 'd'
    direction = DOWN
    snake = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5)]

    def __init__(self, win):
        self.win = win

    def update(self):
        last_segment = self.snake[0]
        x, y = last_segment
        dir_func = {
                Snake.DOWN: lambda x, y : (x + 1, y),
                Snake.UP: lambda x, y : (x - 1, y),
                Snake.LEFT: lambda x, y : (x, y - 1),
                Snake.RIGHT: lambda x, y : (x, y + 1),
                }
        fun = dir_func[self.direction]

        self.snake[0] = fun(x, y)
        snake = self.snake
        a, b = x, y

        for i in range(1, len(self.snake)):
            x, y = snake[i]
            snake[i] = (a, b)
            a, b = x, y

    def go(self, direction):
        if set([self.direction, direction]) == set([Snake.UP, Snake.DOWN]):
            return
        if set([self.direction, direction]) == set([Snake.LEFT, Snake.RIGHT]):
            return
        self.direction = direction

    def draw(self):
        for s in self.snake:
            x, y = s
            self.win.addstr(x, y, self.char, self.snake_color)

class Window():
    pass

class App:
    colors = Colors()
    width = 20
    height = 40
    win = None
    snake = None

    def main(stdscr):
        App.win = stdscr
        #App.win.w = 0
        App.snake = Snake(App.win)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        App.colors.cl_bwhite = curses.color_pair(2) | curses.A_BOLD
        App.colors.cl_dwhite = curses.color_pair(2) | curses.A_DIM
        App.colors.cl_nwhite = curses.color_pair(2)
        App.snake.snake_color = curses.color_pair(1) | curses.A_BOLD
        stdscr.clear()
        curses.curs_set(False)

        App.field = {(x,y):z for x in range(App.width) 
            for y in range(App.height) for z in [Char('.', App.colors.cl_nwhite)]}

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
                App.snake.go(chr(key))
            notEnd = key != ord('q')

    def __init__(self):
        curses.wrapper(App.main)

    def update():
        App.snake.update()

    def draw_field(field):
        for x in range(App.width):
            for y in range(App.height):
                char = field[(x, y)].char
                color = field[(x, y)].color
                App.win.addstr(x, y, char, color)
        App.snake.draw()


if __name__=='__main__':
     app = App()
