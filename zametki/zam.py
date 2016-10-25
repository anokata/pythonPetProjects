import curses
from curses import wrapper
#from collections import OrderedDict
from curses.textpad import Textbox, rectangle
import vault
from vault import * # из за загрузки pickle'ом ??? он не видит модули?
import random

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
ColorRW = 5
ColorMW = 6
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
            k, a = a
            self.path[0] = k
            self.menuContent.text = [str(a.value())]
            #self.menuContent.text = [str(a.value()), str(a), k]
            # TODO: надо как то хранить путь к текущему элементу для изменения
            return True

        self.menu = MenuListCurses()
        self.win = self.menu.win

        for k, v in self.store.items():
            if v.isDir():
                self.menu.add('['+k+']', MenuSelect, (k, v), MenuChange)
            else:
                self.menu.add(k, MenuSelect, (k, v), MenuChange)

    def __init__(self, scr):
        self.mainwin = scr
        scr.clear()
        self.wins = list()
        curses.curs_set(False)
        curses.init_pair(ColorBW, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK )
        curses.init_pair(ColorWBl, curses.COLOR_WHITE, curses.COLOR_BLUE )
        curses.init_pair(ColorRW, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(ColorMW, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        
        self.path = ['cc']
        scr.bkgd(curses.color_pair(ColorBW))
        self.mainRefresh()
        
        self.inp = inp = Inputer()
        self.menuContent = TextView()
        self.vit = ViTextEdit()

        self.store = vault.Storage(True)
        self.buildMenu()
        self.menu.highlight()

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
        if key == ord('e'): # Редактирование значения ??? TODO редактирование директорий особо. 
            newtext = self.vit.run(self.menuContent.text)
            # save new text
            self.store[self.path[0]] = ''.join(newtext)
            self.buildMenu()
        #TODO: add dir, save all. move to dir, path save.
        # строить меню по текущему пути. менять путь при переходе в дир.
            
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

    def work(self):
        notEnd = True
        while notEnd:
            self.refresh()
            self.win.addstr(curses.LINES-4,1,': '+self.path[0])
            notEnd = self.handler()
            self.refresh()

class Inputer():
    def __init__(self):
        self.win = makeWin(1+MenuWidth+TextWidth, 1, 20, 3)
     
    def run(self):
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
        else:
            self.msg += chr(key)
        return notEnd

    def display(self):
        win = self.win
        win.refresh()
        win.border()
        curses.curs_set(True)
        #curses.setsyx(4,82) 
        win.addstr(1, 2, self.msg, curses.color_pair(ColorBW))

INSERT = 0
COMMAND = 1
class ViTextEdit():
    mode = INSERT
    def __init__(self):
        self.width = TextWidth
        self.height = curses.LINES-3
        self.win = makeWin(1+MenuWidth, 1, self.width, self.height)
        self.win.bkgd(curses.color_pair(ColorRW))

    def run(self, text=''):
        #get text from storage selected
        self.msg = ''
        #self.text = text.split('\n')
        self.text = text
        self.currentLine = 0
        self.y = len(text)
        self.x = len(text[-1])
        self.key = ''
        self.display()
        self.mode2ins()
        nend = True
        while nend:
            if self.mode == INSERT:
                nend = self.handler()
            else:
                nend = self.handlerCom()
            self.display()
        self.win.clear()
        curses.curs_set(False)
        return self.text

    def addChar(self, c):
        if len(self.text[self.currentLine]) >= self.width-2:
            self.newLine()
        self.text[self.currentLine] = self.text[self.currentLine][:self.x-1] + c + self.text[self.currentLine][self.x-1:]
        self.cursorMove(1,0)

    def newLine(self):
        self.text.append('')
        self.currentLine += 1
        self.cursorMove(-1000,1)

    def bs(self):
        self.text[self.currentLine] = self.text[self.currentLine][:-1]
        self.cursorMove(-1,0)

    def mode2ins(self):
        self.mode = INSERT
        self.win.bkgd(curses.color_pair(ColorRW))

    
    def mode2com(self):
        self.mode = COMMAND
        self.win.bkgd(curses.color_pair(ColorMW))

    def cursorMove(self, dx, dy):
        self.y += dy
        self.x += dx
        if self.y < 1:
            self.y = 1
        if self.y > len(self.text): #self.height-2:
            self.y = len(self.text)
        self.currentLine = self.y-1

        if self.x < 1:
            self.x = 1
        if self.x > len(self.text[self.currentLine]):
            self.x = len(self.text[self.currentLine])+1

    def handlerCom(self):
        notEnd = True
        key = self.win.getkey()
        if ord(key) == ord('i'):
            self.mode2ins()
        elif ord(key) == 24:
            notEnd = False
        elif ord(key) == ord('j'):
            self.cursorMove(0, 1)
        elif ord(key) == ord('k'):
            self.cursorMove(0, -1)
        elif ord(key) == ord('h'):
            self.cursorMove(-1, 0)
        elif ord(key) == ord('l'):
            self.cursorMove(1, 0)

        return notEnd

    def handler(self):
        notEnd = True
        #key = self.win.getch()
        key = self.win.getkey()
        if ord(key) == 27: # escape
            self.mode2com()
        elif ord(key) == 10: # newline
            self.newLine()
        elif ord(key) == 24: # Ctrl-X ^X
            notEnd = False
        elif ord(key) == 127: # backspace
            self.bs()
        else:
            self.addChar(key)
            self.key = str(ord(key))
        return notEnd

    def display(self):
        win = self.win
        curses.curs_set(False)
        win.clear()
        win.refresh()
        win.border()
        win.addstr(self.height-1, 2, '    ', curses.color_pair(ColorBW))
        win.addstr(self.height-1, 2, self.key, curses.color_pair(ColorBW))
        y = 1
        for line in self.text:
            win.addstr(y, 1, line, curses.color_pair(ColorBW))
            y += 1
        curses.curs_set(True)
        #if self.mode == COMMAND:
        win.addstr(self.y, self.x, '', curses.color_pair(ColorBW))


def main(scr):
    w = Wincon(scr)
    w.refresh()
    w.work()
    curses.curs_set(True)

wrapper(main)
