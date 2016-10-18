import pygame
import sys
sys.path += ["../modules",'./']
from stateSystem import *
import pyganim
import roomGenerator as rg
import random

def makeSpriteXY(imgname, x, y):
    s = pygame.sprite.Sprite()
    s.image = img = pygame.image.load(imgname).convert()
    s.rect = img.get_rect()
    w = s.rect.w
    h = s.rect.h
    s.rect.left = x * w
    s.rect.top = y * h
    return s

class Enemy(pygame.sprite.Sprite):
    rect = pygame.Rect(0,0,0,0)

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cucumber.png').convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])


# делать игрока сначала базового не зависящего от движка.
#Камера. у неё есть свои размеры и положение. она не даёт выйти за пределы игроку - меняет положение, следит. Она преобразует данные в неё координаты объекта так чтобы они отображались на экране( вычесть координаты камеры)
class Camera():

    def __init__(self, w, h):
        self.rect = pygame.Rect(0, 0, w, h)

    def stalkAt(self, p):
        """ Следить за """
        self.rect.left = min(self.rect.left, p.rect.left - WindowW//2) 
        self.rect.right = max(self.rect.right, p.rect.right)
        self.rect.top = min(self.rect.top, p.rect.top - WindowH//2)
        self.rect.right = max(self.rect.right, p.rect.right)
        self.rect.bottom = max(self.rect.bottom, p.rect.bottom)

    def calc(self, o):
        """ пересчитать координаты объекта на экран """
        r = pygame.Rect(0, 0, 0, 0)
        r.left = o.rect.left - self.rect.left #- WindowH//2
        r.top = o.rect.top - self.rect.top #+ WindowW//2
        #r.left = o.rect.left - self.rect.left
        #r.left = o.rect.left - self.rect.left
        return r


class Tiled():
    tiles = []

    def __init__(self, imgname, mp):
        tiles = list()
        for x,y in mp:
            self.tiles += [makeSpriteXY(imgname, x, y)]

    def draw(self):
        for x in self.tiles:
            screen.blit(x.image, (x.x, x.y))


class Player():
    health = 100
    spd = 3.0
    spdj = 5.0
    moving = 0
    movingud = 0
    dy = 0
    dx = 0.0

    def __init__(self):
        pass

# Player anim
AnimDelay = 0.1 # скорость смены кадров
AnimGoRight = ['wiz0.png' ,'wiz0.png']
AnimGoLeft = ['wiz0.png','wiz0.png']
AnimJumpLeft = ['wiz0.png', 'wiz0.png']
AnimJumpRight = ['wiz0.png','wiz0.png']
AnimJump = ['wiz0.png']
AnimStand = ['wiz0.png']

class pgPlayer(Player, pygame.sprite.Sprite):
    rect = pygame.Rect(0,0,0,0)

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.standimg = pygame.image.load('cat3.png').convert()
        self.standRightImg = pygame.image.load('cat3.png').convert()
        self.standLeftImg = pygame.image.load('cat2L.png').convert()
        self.image = self.standimg
        self.wallimg = pygame.image.load('catwall.png').convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])

        from itertools import repeat
        Anim = list(zip(AnimGoRight, list(repeat(AnimDelay, len(AnimGoRight)))))
        self.AnimRight = pyganim.PygAnimation(Anim)
        self.AnimRight.play()

        Anim = list(zip(AnimGoLeft, list(repeat(AnimDelay, len(AnimGoLeft)))))
        self.AnimLeft = pyganim.PygAnimation(Anim)
        self.AnimLeft.play()

        Anim = list(zip(AnimJumpLeft, list(repeat(AnimDelay, len(AnimJumpLeft)))))
        self.AnimJumpLeft = pyganim.PygAnimation(Anim)
        self.AnimJumpLeft.play()

        Anim = list(zip(AnimJumpRight, list(repeat(AnimDelay, len(AnimJumpRight)))))
        self.AnimJumpRight = pyganim.PygAnimation(Anim)
        self.AnimJumpRight.play()

        Anim = list(zip(AnimStand, list(repeat(AnimDelay, len(AnimStand)))))
        self.AnimStand = pyganim.PygAnimation(Anim)
        self.AnimStand.play()
        self.changeAnim(self.AnimStand)

    def changeAnim(self, a):
        self.image.fill(pygame.Color('#000000'))
        a.blit(self.image, (0, 0))

    def moveSide(self, dt, platforms, enemies):
        if self.dx < 0:
            self.changeAnim(self.AnimLeft)
        elif self.dx > 0:
            self.changeAnim(self.AnimRight)
        
        self.dx = - self.moving * self.spd
        self.dy = - self.movingud * self.spd

        
        self.rect.x += self.dx
        self.collide(self.dx, 0, platforms)

        self.rect.y += self.dy
        self.collide(0, self.dy, platforms)

        self.collideEnemies(enemies)

    def collideEnemies(self, enemies):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                self.dx = -self.dx

    def collide(self, dx, dy, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if dx > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо
                if dx < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if dy > 0:                    
                    self.rect.bottom = p.rect.top  

                if dy < 0:                   
                    self.rect.top = p.rect.bottom 

class Block(pygame.sprite.Sprite): # base class for sprites?
    rect = 0
    def __init__(self, x, y, imgname=''):
        Sprite.__init__(self)
        self.image = pygame.image.load('block1.png').convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])


# Globals
WindowH = 550
WindowW = 800
Display = (WindowW, WindowH)
bgColor = "#004400"
player = None
bgSurface = None
screen = 0
collided = list()
enemies = list()
gravity = 0.2
cam = Camera(400, 300)
#http://www.pygame.org/docs/ref/key.html
Sprite = pygame.sprite.Sprite
entities = None
layerBg = None
layerFg = None
textLayer = None
menu = None

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
        player.moving += -1
    if k == pygame.K_LEFT:
        player.moving += 1
    if k == pygame.K_SPACE:
        runMenu('men1')
    if k == pygame.K_UP:
        player.movingud = 1
    if k == pygame.K_DOWN:
        player.movingud = -1

def keyUp(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving += 1
    elif k == pygame.K_LEFT:
        player.moving += -1
    if k == pygame.K_SPACE:
        pass
    if k == pygame.K_UP:
        player.movingud = 0
    if k == pygame.K_DOWN:
        player.movingud = 0

class Font():
    def __init__(self, size, color = (255, 255, 255), bgcolor=False):
        self.h = h = size
        self.color = color
        self.bg = bgcolor
        self.font = pygame.font.Font(None, h)

    def render(self, t):
        if self.bg:
            return self.font.render(t, 1, self.color, self.bg)
        else:
            return self.font.render(t, 1, self.color)

    def get_rect(self):
        return self.font.get_rect()

class MenuList():
    items = []
    selected = 0

    def __init__(self, layer, id, x=20, y=10):
        self.layer = layer
        self.items = list()
        self.id = id
        self.rect = pygame.Rect(0,0,0,0)
        #self.font = Font(32, (100, 0, 250))
        self.font = Font(32, (100, 0, 250), (100, 100, 100))
        self.selfont = Font(32, (80, 100, 230), (180, 180, 180))
        self.x = x
        self.y = y

    def rend(self):
        self.layer[self.id] = list()
        y = self.y
        for x in self.items:
            if self.items.index(x) == self.selected:
                t = self.selfont.render(x)
            else:
                t = self.font.render(x)
            self.rect = t.get_rect()
            self.rect.top = y
            self.rect.left = self.x
            y += self.font.h // 1.5
            self.layer[self.id].append((t, self.rect))

    def addItem(self, text):
        self.items.append(text)
        self.rend()

    def pred(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1
        self.rend()

    def next(self):
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0
        self.rend()

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
    global cam, player, Layers, textLayer
    cam.stalkAt(player)
    
    for l in Layers:
        for e in l:
            screen.blit(e.image, cam.calc(e))
    
    #for x in textLayer.values():
    #    for (e, r) in x:
    #        screen.blit(e, r)

    pygame.display.flip()

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
    player = pgPlayer(44, 44)
    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', player.moveSide)

    mp = list()
    Layers = list()
    Layers.append(pygame.sprite.Group())
    Layers.append(pygame.sprite.Group())
    Layers.append(pygame.sprite.Group())

    layerBg = Layers[0]
    layerFg = Layers[2]
    entities = Layers[1]
    textLayer = {'menu1': list()}

    # menu
    global menu
    menu = createMenu('men1', ['it0','it2','end'])

    for x in range(30):
        mp += [(x,15)]
    m = Tiled('ground1.png', mp)
    for x in m.tiles:
        layerBg.add(x)

    mp = list()
    for x in range(140):
        mp += [(x,1)]
    m = Tiled('sky0.png', mp)
    for x in m.tiles:
        layerBg.add(x)

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
    blockwh = pygame.image.load('block1.png').get_rect().size[0]
    for x in range(len(lev)):
        for y in range(len(lev[0])):
            if lev[x][y] == 'x':
                b = Block(y*blockwh, x*blockwh,)
                collided += [b]
                entities.add(b)
            if lev[x][y] == 'c':
                e = Enemy(y*blockwh, x*blockwh+blockwh//2)
                entities.add(e)
                enemies.append(e)

    layerFg.add(player)
    createEnemies(layerFg)
    #randomClouds(layerBg)
    
def randomClouds(layer):
    count = 10
    w = 30
    width = 32
    points = list()
    for i in range(count):
        x = random.randint(1, w)
        y = random.randint(1, w)
        points.append((x,y))
    obj = Tiled('cloud0.png', points)
    print(points)
    for x in obj.tiles:
        layer.add(x)



def createEnemies(layer):
    count = 10
    w = 30
    width = 32
    for i in range(count):
        x = random.randint(1, w) * width
        y = random.randint(1, w) * width
        enemy = Enemy(x, y)
        layer.add(enemy)


def mainLoop():
    clock = pygame.time.Clock()
    isExit = False
    pygame.time.set_timer(pygame.USEREVENT + 1, int(1000/90))
    while not isExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isExit = True
                handleEvent('keyDown', event.key, event)
            if event.type == pygame.KEYUP:
                handleEvent('keyUp', event.key, event)
            if event.type == pygame.USEREVENT + 1:
                handleEvent('mechanic', 1, collided, enemies)
        clock.tick()
        pygame.display.set_caption("fps: " + str(int(clock.get_fps())))
        handleEvent('draw')

if __name__ == "__main__":
    main()
