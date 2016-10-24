import curses
from curses import wrapper
#from collections import OrderedDict
from curses.textpad import Textbox, rectangle
import vault
from vault import * # из за загрузки pickle'ом ??? он не видит модули?

def makeWin(x, y, w, h):
    win = curses.newwin(h, w, y, x)
    win.border()
    win.bkgd(curses.color_pair(ColorBlW))
    return win

class MenuList():
    # список элементов меню = ключ- горячая клавиша, значение (текст, функция обработчик)
    items = []
    lastKey = '1'
    selected = 0

    def __init__(self):
        self.items= list()

    def add(self, item, fun, args, highlightfun, key=None):
        if key == None:
            key = self.lastKey
            self.lastKey = chr(ord(self.lastKey) + 1)
        self.items.append((key, item, fun, args, highlightfun))

    def select(self):
        (key, text, fun, args, *_) = self.items[self.selected]
        return fun(args)

    def highlight(self):
        (key, text, fun, args, hf, *_) = self.items[self.selected]
        return hf(args)

    def next(self):
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0

    def pred(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1

MenuWidth = 20
TextWidth = 60
class MenuListCurses(MenuList):

    def __init__(self):
        super().__init__()
        self.win = makeWin(1, 1, MenuWidth, curses.LINES-3)

    def display(self):
        win = self.win
        win.refresh()
        win.clear()
        win.border()
        x = 1
        y = 0
        for (k, t, _, *_) in self.items:
            y += 1
            if y - 1 == self.selected:
                win.addstr(y, x, '(' + k + ') ' + t, curses.color_pair(ColorWBl) )
            else:
                win.addstr(y, x, '(' + k + ') ' + t, curses.color_pair(ColorBW))

class TextView():
    def __init__(self):
        self.win = makeWin(1+MenuWidth, 1, TextWidth, curses.LINES-3)
        self.text = list()

    def display(self):
        win = self.win
        win.refresh()
        win.clear()
        win.border()
        x = 2
        y = 0
        for t in self.text:
            y += 1
            win.addstr(y, x, t, curses.color_pair(ColorBW))

ColorBW = 1
ColorBlW = 2
ColorRB = 3
ColorWBl = 4
class Wincon():
    mainwin = None
    wins = []
    menu = None
    debugwin = None
    menuContent = None #
    
    def mainRefresh(self):
        self.mainwin.refresh()
        #self.mainwin.clear()
        self.mainwin.border()
        self.mainwin.addstr(curses.LINES-1, 2, "[k:up j:down q:exit ]")

    def buildMenu(self):
        def MenuSelect(a):
            #m = self.inp.run()
            #self.buildMenu()
            return True

        def MenuChange(a):
            self.menuContent.text = [str(a.value())]
            return True

        self.menu = MenuListCurses()
        self.win = self.menu.win

        for k, v in self.store.items():
            if v.isDir():
                self.menu.add('['+k+']', MenuSelect, v, MenuChange)
            else:
                self.menu.add(k, MenuSelect, v, MenuChange)

    def __init__(self, scr):
        self.mainwin = scr
        scr.clear()
        self.wins = list()
        curses.curs_set(False)
        curses.init_pair(ColorBW, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK )
        curses.init_pair(ColorWBl, curses.COLOR_WHITE, curses.COLOR_BLUE )
        scr.bkgd(curses.color_pair(ColorBW))
        self.mainRefresh()
        
        self.inp = inp = Inputer(scr)
        self.menuContent = TextView()

        self.store = vault.Storage(True)
        self.buildMenu()

    def handler(self):
        notEnd = True
        key = self.win.getch()
        if key == ord('q') or key == 27:
            notEnd = False
        if key == ord('j'):
            self.menu.next()
            self.menu.highlight()
        if key == ord('k'):
            self.menu.pred()
            self.menu.highlight()
        if key == ord(' '):
            return self.menu.select()
        if key == ord('a'): # добавление элемента
            name = self.inp.run()
            self.store[name] = name 
            self.buildMenu()
        if key == ord('e'): # Редактирование значения ??? TODO
            pass
            
        self.win.addstr(curses.LINES-5,1,'вы нажали: '+str(key))
        return notEnd

    def addWin(self):
        pass

    def refresh(self):
        self.mainRefresh()
        for w in self.wins:
            w.refresh()
        self.menuContent.display()
        self.menu.display()
        if self.inp.running:
            self.inp.display()

    def work(self):
        notEnd = True
        while notEnd:
            self.refresh()
            notEnd = self.handler()
            self.refresh()

class Inputer():
    def __init__(self, scr):
        self.keys = list()
        self.win = makeWin(1+MenuWidth+TextWidth, 1, 20, 3)
        self.scr = scr
        self.running = False
     
    def run(self):
        self.running = True
        self.msg = ''
        self.display()
        nend = True
        while nend:
            nend = self.handler()
            self.display()
        self.win.clear()
        curses.curs_set(False)
        return self.msg

    def handler(self):
        notEnd = True
        key = self.win.getch()
        if key == 10 or key == 27:
            notEnd = False
            self.running = False
        else:
            self.msg += chr(key)
        self.win.addstr(2,1,'вы нажали: '+str(key))
        return notEnd

    def display(self):
        win = self.win
        win.refresh()
        win.border()
        curses.curs_set(True)
        curses.setsyx(4,82) 
        x = 2
        y = 1
        win.addstr(y, x, self.msg, curses.color_pair(ColorBW))

def main(scr):
    w = Wincon(scr)
    w.refresh()
    w.work()
    curses.curs_set(True)

wrapper(main)
