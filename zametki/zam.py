import curses
from curses import wrapper
#from collections import OrderedDict

class MenuList():
    # список элементов меню = ключ- горячая клавиша, значение (текст, функция обработчик)
    items = []
    lastKey = '1'
    selected = 0

    def __init__(self):
        self.items= list()

    def add(self, item, fun, args, key=None):
        if key == None:
            key = self.lastKey
            self.lastKey = chr(ord(self.lastKey) + 1)
        self.items.append((key, item, fun, args))

    def select(self):
        (key, text, fun, args) = self.items[self.selected]
        fun()

    def next(self):
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0

    def pred(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1


class MenuListCurses(MenuList):

    def __init__(self, win):
        self.win = win

    def display(self, win=False):
        if not win:
            win = self.win
        x = 1
        y = 0
        for (k, t, _, _) in self.items:
            y += 1
            if y - 1 == self.selected:
                win.addstr(y, x, '(' + k + ') ' + t, curses.color_pair(3) )
            else:
                win.addstr(y, x, '(' + k + ') ' + t)

    def handler(self):
        notEnd = True
        while notEnd:
            key = self.win.getch()
            if key == ord('q') or key == 27:
                notEnd = False
            if key == ord('j'):
                self.pred()
            if key == ord('k'):
                self.next()

            self.display()
            self.win.refresh()

def main(scr):
    scr.clear()
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK )
    scr.border()
    scr.bkgd(curses.color_pair(1))

    win0 = curses.newwin(20, 20, 3, 3)
    menu = MenuListCurses(win0)
    menu.add('someOne', print, '123test')
    menu.add('someTwo', print, 'afa fa fa a!fA!')
    menu.add('Thor', print, 'Thow')
    menu.next()
    menu.next()
    menu.select()

    scr.addstr(1,2, "heloha!")
    win0.border()
    win0.addstr(3,3, "win0")
    win0.bkgd(curses.color_pair(2))
    
    menu.display(win0)
    menu.handler()

    scr.refresh()
    win0.refresh()
    scr.getkey()

wrapper(main)
