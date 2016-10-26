import pygame
import sys
sys.path += ["../modules",'./']
from stateSystem import *
import pyganim
import roomGenerator as rg
import random
from menu import *
from player import *
from camera import *
from consts import *

#TODO: наделать много вещей. коллекционирование. инвентарь. иконки.
# сначала всё же без генератора, сделать статичный мир. но интересный
# TODO: map, переделать отображение. сделать редактор, сохранение загрузка добавление новых блоков. редактор. выбор блоков.

def makeSpriteXY(imgname, x, y):
    s = pygame.sprite.Sprite()
    s.image = img = pygame.image.load(imgname).convert()
    s.rect = img.get_rect()
    w = s.rect.w
    h = s.rect.h
    s.rect.left = x * w
    s.rect.top = y * h
    return s

# делать игрока сначала базового не зависящего от движка.
class EnergySystem():
    map = {}

    def __init__(self):
        from collections import defaultdict
        self.map = defaultdict(list)

    def registr(self, obj, x, y):
        map[(x, y)].append(obj)

    def emit(self, x, y, energyAmount):
        pass

class Obj():
    energy = 0.0

class Block(pygame.sprite.Sprite): # base class for sprites?
    rect = 0
    def __init__(self, x=0, y=0, imgname='block1.png'):
        Sprite.__init__(self)
        self.image = pygame.image.load(imgname).convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])

    def draw(self, x, y, cam):
        screen.blit(self.image, cam.calcXY(x, y)) 
        #screen.blit(self.image, (self.rect.left, self.rect.top))

class PhisycBlock():
    rect = 0
    def __init__(self, x, y, w):
        self.rect = pygame.Rect(x, y, w, w)

class Map():
    tiles = 0
    w = h = z = 0
    blockers = 0

    def __init__(self, z):
        self.blockers = list()
        self.z = z
        self.load()

    def __setitem__(self, k, v):
        self.tiles[k] = v

    def __getitem__(self, k):
        return self.tiles[k]
    
    def draw(self, cam):
        for x in range(self.w):
            for y in range(self.h):
                for z in range(self.z):
                    for o in self.tiles[x,y,z]:
                        a, b = x * self.blockW, y * self.blockH
                        o.draw(a, b, cam)
    def load(self):
        lev= ["xxxxxxxxxxxxxxxxxxxxxxxxx",
          "x-----x-x-xx-------x----x",
          "x-----------x------x----x",
          "x---c---c-------c-------x",
          "xxxxx---xxxx---xxxxx----x",
          "x-----------------------x",
          "x----------xxx----------x",
          "x-----------------------x",
          "x-----x-------x----x----x",
          "x-x-xxxxx------xxxxx----x",
          "xx----------------------x",
          "xxxxxxx---------xxxx----x",
          "x-------x---xxxxxxxx----x",
          "x--xxx----------xxxx----x",
          "x-----------------------x",
          "x-----------------------x",
          "xxxxxxxxxxxxxxxxxxxxxxxxx",
             ]
        descrp = {
                'x': ('objects/block2.png',),
                '-': ('objects/ground0.png',),
                'c': ('objects/zap0.png',),
                }
        self.blockW = self.blockH = 32
        mapObjects = dict()
        for c, p in descrp.items():
            imgpath = p[0]
            sprite = Block(imgname=imgpath)
            mapObjects[c] = (sprite,)

        w = len(lev[0])
        h = len(lev) 

        self.w = w
        self.h = h
        z = self.z
        self.tiles = {(x, y, lay): l for x in range(w+1) for y in range(h+1) 
                for lay in range(z) for l in [list()]}

        for x in range(w):
            for y in range(h):
                self.tiles[x,y,0] += [mapObjects[lev[y][x]][0]]
                if lev[y][x] == 'x': # CHG
                    a, b = x * self.blockW, y * self.blockH
                    self.blockers.append(PhisycBlock(a, b, self.blockW))

# Globals
player = None
bgSurface = None
screen = 0
collided = list()
enemies = list()
cam = Camera(400, 300)
#http://www.pygame.org/docs/ref/key.html
Sprite = pygame.sprite.Sprite
entities = None
textLayer = None
menu = None
hud = None
globmap = 0

def menuKeyDown(k, d):
    if k == pygame.K_DOWN:
        menu.next()
    if k == pygame.K_UP:
        menu.pred()
    if k == pygame.K_SPACE:
        changeState('mainRun')

def mechanic(dt):
    handleEvent('mechanic', dt)

def keyDown(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving = -1
    if k == pygame.K_LEFT:
        player.moving = 1
    if k == pygame.K_SPACE:
        player.moving = 0
        player.movingud = 0
        runMenu('men1')
    if k == pygame.K_UP:
        player.movingud = 1
    if k == pygame.K_DOWN:
        player.movingud = -1

def keyUp(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving = 0
    elif k == pygame.K_LEFT:
        player.moving = 0
    if k == pygame.K_SPACE:
        pass
    if k == pygame.K_UP:
        player.movingud = 0
    if k == pygame.K_DOWN:
        player.movingud = 0

class Hud():
    items = []
    enrg = 'Energy: %.2f'

    def __init__(self, layer, x=0, y=10):
        self.layer = layer
        i = self.items = list()
        self.id = 'hud'
        self.rect = pygame.Rect(0,0,0,0)
        self.font = Font(24, (230, 50, 50))
        self.x = x
        self.y = y
        i.append(self.enrg)
        self.refresh()

    def refresh(self):
        self.layer[self.id] = list()
        y = self.y
        for x in self.items:
            t = self.font.render(x % player.energy)
            self.rect = t.get_rect()
            self.rect.top = y
            self.rect.left = self.x
            y += self.font.h // 1.5
            self.layer[self.id].append((t, self.rect))


def createMenu(id, lst): # add обработчик выбора, обработчик 
    addState(id)
    setEventHandler(id, 'keyDown', menuKeyDown)
    setEventHandler(id, 'draw', drawMenu)
    menu = MenuList(textLayer,  id)
    for x in lst:
        menu.addItem(x)
    return menu

def runMenu(id):
    changeState(id)
    return

def drawMenu():
    screen.blit(bgSurface.image, (0, 0))
    global textLayer
    for x in textLayer.values():
        for (e, r) in x:
            screen.blit(e, r)
    pygame.display.flip()

def drawMain():
    screen.blit(bgSurface.image, (0, 0))
    global cam, player, textLayer, globmap
    cam.stalkAt(player)
    
    for (e, r) in textLayer['hud']:
        screen.blit(e, r)

    globmap.draw(cam) 
    screen.blit(player.image, cam.calc(player))
    pygame.display.flip()

def mainMechanic(d, p, e):
    player.moveSide(d, p, e)
    hud.refresh()

def main():
    pygame.init()
    mainInit()
    mainLoop()

def mainInit():
    global screen
    global collided, cam, player, enemies, Layers, textLayer 
    global bgSurface
    screen = pygame.display.set_mode(Display)
    pygame.display.set_caption("/TXS/")

    bgSurface = pygame.sprite.Sprite()
    bgSurface.image = pygame.image.load('nightSky0.png').convert()
    bgSurface.image = pygame.Surface([800,1000])
    bgSurface.image.fill((0,0,0))
    player = pgPlayer(44, 44)
    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', mainMechanic)
    
    global globmap
    b = Block()
    globmap = Map(2)
    collided = globmap.blockers # CHG

    mp = list()
    entities = list()
    textLayer = {'menu1': list()}

    # menu
    global menu, hud
    menu = createMenu('men1', ['it0','it2','end'])
    hud = Hud(textLayer, WindowW-150, WindowH-30)

def mainLoop():
    clock = pygame.time.Clock()
    isExit = False
    pygame.time.set_timer(pygame.USEREVENT + 1, int(1000/90))
    while not isExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isExit = True
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isExit = True
                    continue
                handleEvent('keyDown', event.key, event)
            if event.type == pygame.KEYUP:
                handleEvent('keyUp', event.key, event)
            if event.type == pygame.USEREVENT + 1:
                handleEvent('mechanic', 1, collided, enemies)
        clock.tick()
        pygame.display.set_caption("fps: " + str(int(clock.get_fps())))
        handleEvent('draw')
    exit()

if __name__ == "__main__":
    main()
