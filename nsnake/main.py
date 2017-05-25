import paths
import curses
import time
import random
import stateSystem as ss
# teleports
# TODO 
# facade to curses -> makes classes like colors etc
# start menu: new game(game over, game state) scores(calc it, view) exit.

class Char:

    def __init__(self, char, color):
        self.char = char
        self.color = color

class Colors:
    pass

class BonusFactory:

    class Bonus:
        char = '\u25ca'

        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color

    def __init__(self, window):
        self.width = window.width
        self.height = window.height
        self.window = window

    def make(self):
        x = random.randint(1, self.width)
        y = random.randint(1, self.height)
        return BonusFactory.Bonus(x, y, self.window.colors.cl_ngreen)

class Snake:
    char = '\u25CF'
    head = '\u25C9'
    UP = 'w'
    DOWN = 's'
    LEFT = 'a'
    RIGHT = 'd'
    direction = RIGHT
    #snake = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (3, 6), (3, 7)]
    snake = [(1, 1)]

    def __init__(self, win):
        self.win = win.descriptor
        self.width = win.width
        self.height = win.height

    def update(self):
        last_segment = self.snake[0]
        x, y = last_segment
        dir_func = {
                Snake.RIGHT: lambda x, y : (x + 1, y),
                Snake.LEFT: lambda x, y : (x - 1, y),
                Snake.UP: lambda x, y : (x, y - 1),
                Snake.DOWN: lambda x, y : (x, y + 1),
                }
        fun = dir_func[self.direction]

        nx, ny = fun(x, y)

        if nx < 0:
            nx = self.width - 1
        if nx >= self.width:
            nx = 0
        if ny < 0:
            ny = self.height - 1
        if ny >= self.height:
            ny = 0

        self.snake[0] = (nx, ny)
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
            self.win.addstr(y, x, self.char, self.snake_color)
        x, y = self.snake[0]
        self.win.addstr(y, x, self.head, self.snake_color)

    def enlarge(self, x, y):
        self.snake.insert(0, (x, y))

class Window():
    width = 40
    height = 20
    colors = Colors()
    messages = None #TODO

    def __init__(self, descriptor, colors):
        self.descriptor = descriptor
        self.colors = colors


class App:
    colors = Colors()
    width = 40
    height = 20
    win = None
    snake = None
    bonusFactory = None
    bonuses = dict()

    def init_colors():
        all_colors = {
                'red': curses.COLOR_RED,
                'black': curses.COLOR_BLACK,
                'green': curses.COLOR_GREEN,
                }

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

        App.colors.cl_bwhite = curses.color_pair(2) | curses.A_BOLD
        App.colors.cl_dwhite = curses.color_pair(2) | curses.A_DIM
        App.colors.cl_nwhite = curses.color_pair(2)
        App.colors.cl_ngreen = curses.color_pair(3)


    def main(stdscr):
        curses.start_color()
        App.init_colors()
        stdscr.clear()
        curses.curs_set(False)

        App.window = Window(stdscr, App.colors)
        App.win = stdscr
        App.snake = Snake(App.window)
        App.snake.snake_color = curses.color_pair(1) | curses.A_BOLD

        App.bonusFactory = BonusFactory(App.window)
        for i in range(50):
            bonus = App.bonusFactory.make()
            App.bonuses[(bonus.x, bonus.y)] = bonus

        App.field = {(x,y):z for x in range(App.width) 
            for y in range(App.height) for z in [Char('.', App.colors.cl_nwhite)]}

        App.draw_field(App.field)
        stdscr.refresh()

        notEnd = True
        App.win.nodelay(True)
        while notEnd:
            App.intersect()
            App.update()
            App.draw_field(App.field)
            stdscr.refresh()
            time.sleep(0.1)

            key = App.win.getch()
            if key == curses.ERR:
                continue
            if chr(key) in ('w', 'a', 's', 'd'):
                App.snake.go(chr(key))
            if chr(key) == 'l':
                App.snake.enlarge(App.snake.snake[0][0], App.snake.snake[0][1])
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
                App.win.addstr(y, x, char, color)
        App.snake.draw()
        for bonus in App.bonuses.values():
            x, y = bonus.x, bonus.y
            App.win.addstr(y, x, bonus.char, bonus.color)

    def intersect():
        to_pop = list()
        for bonus in App.bonuses.values():
            x, y = bonus.x, bonus.y
            if (x, y) == App.snake.snake[0]:
                App.snake.enlarge(x, y)
                to_pop.append((x, y))
        for x, y in to_pop:
            App.bonuses.pop((x, y))



if __name__=='__main__':
     app = App()
