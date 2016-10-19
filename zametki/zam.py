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

    def __init__(self):
        self.win = curses.newwin(20, 20, 3, 3)
        self.win.border()
        self.win.bkgd(curses.color_pair(2))

    def display(self):
        win = self.win
        x = 1
        y = 0
        for (k, t, _, _) in self.items:
            y += 1
            if y - 0 == self.selected:
                win.addstr(y, x, '(' + k + ') ' + t, curses.color_pair(3) )
            else:
                win.addstr(y, x, '(' + k + ') ' + t)

    def handler(self):
            notEnd = True
#        while notEnd:
            key = self.win.getch()
            if key == ord('q') or key == 27:
                notEnd = False
            if key == ord('j'):
                self.next()
            if key == ord('k'):
                self.pred()

#            self.display()
            return notEnd
            #self.win.refresh()

class Wincon():
    mainwin = None
    wins = []
    menu = None
    debugwin = None

    def __init__(self, scr):
        self.mainwin = scr
        scr.clear()
        self.wins = list()
        curses.curs_set(False)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK )
        scr.border()
        scr.bkgd(curses.color_pair(1))

        menu = MenuListCurses()
        menu.add('someOne', print, '123test')
        menu.add('someTwo', print, 'afa fa fa a!fA!')
        menu.add('Thor', print, 'Thow')
        menu.add('someOne', print, '123test')
        self.menu = menu

    def addWin(self):
        pass

    def refresh(self):
        self.mainwin.refresh()
        for w in self.wins:
            w.refresh()
        self.menu.display()

        self.mainwin.addstr(0,0,str(self.menu.selected)+self.menu.items[self.menu.selected][1])

    def work(self):
        notEnd = True
        while notEnd:
            notEnd = self.menu.handler()
            self.refresh()

def main(scr):
    w = Wincon(scr)
    scr.addstr(curses.LINES-1, 2, "[k:up j:down q:exit ]")
    w.refresh()
    w.work()


wrapper(main)
