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
    isStand = False
    onWall = False
    dy = 0
    dx = 0.0
    jumped = False

    def __init__(self):
        pass

# Player anim
AnimDelay = 0.1 # скорость смены кадров
AnimGoRight = ['catr1.png' ,'catr2.png']
AnimGoLeft = ['catl1.png','catl2.png']
AnimJumpLeft = ['catjl.png', 'catjl2.png']
AnimJumpRight = ['catjr.png','catjr2.png']
AnimJump = ['catjr.png']
AnimStand = ['cat3.png']

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

    def jump(self, j):
        if not self.jumped:# and self.isStand:
            self.jumped = True

    def changeAnim(self, a):
        self.image.fill(pygame.Color('#000000'))
        a.blit(self.image, (0, 0))

    def moveSide(self, dt, platforms, enemies):
        #self.x -= self.dx * dt * self.moving

        if self.dx < 0:
            self.changeAnim(self.AnimLeft)
        elif self.dx > 0:
            self.changeAnim(self.AnimRight)
        if self.onWall and self.dx < 0:
            self.changeAnim(self.AnimJumpLeft)
        elif self.onWall and self.dx >= 0:
            self.changeAnim(self.AnimJumpRight)

        #if not self.isStand:
        #    self.dy += gravity

        if (self.isStand or self.onWall) and self.jumped:
            self.dy = -self.spdj
            self.isStand = False
            self.onWall = False
            self.jumped = False
            self.dx = self.moving * self.spd

        self.isStand = False

        #self.y += dt * self.dy
        self.dx = - self.moving * self.spd

        if self.onWall:
            self.rect.y += self.dy* 0.2
            self.onWall = False
        else:
            self.rect.y += self.dy
        self.collide(0, self.dy, platforms)
        self.rect.x += self.dx
        self.collide(self.dx, 0, platforms)
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
                    self.onWall = True
                if dx < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево
                    self.onWall = True

                if dy > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.isStand = True          # и становится на что-то твердое
                    self.dy = 0                 # и энергия падения пропадает
                    if self.dx == 0.0:
                        self.changeAnim(self.AnimStand)

                if dy < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.dy = 0                 # и энергия прыжка пропадает

class Block(pygame.sprite.Sprite): # base class for sprites?
    rect = 0
    def __init__(self, x, y, imgname=''):
        Sprite.__init__(self)
        self.image = pygame.image.load('block0.png').convert()
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

def mechanic(dt):
    handleEvent('mechanic', dt)

def keyDown(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving += -1
    if k == pygame.K_LEFT:
        player.moving += 1
    if k == pygame.K_SPACE:
        player.jump(True)

def keyUp(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving += 1
    elif k == pygame.K_LEFT:
        player.moving += -1
    if k == pygame.K_SPACE:
        pass#player.jump(False)

def drawMain():
    screen.blit(bgSurface.image, (0, 0))
    global entities, layerBg, layerFg, cam, player
    cam.stalkAt(player)
    for e in layerBg:
        screen.blit(e.image, cam.calc(e))
    for e in entities:
        screen.blit(e.image, cam.calc(e))
    for e in layerFg:
        screen.blit(e.image, cam.calc(e))
    #pygame.display.update()
    pygame.display.flip()

def main():
    pygame.init()
    mainInit()
    mainLoop()

def mainInit():
    global screen
    global collided, cam, entities, layerBg, layerFg, player, enemies
    global bgSurface
    screen = pygame.display.set_mode(Display)
    pygame.display.set_caption("/TXS/")

    bgSurface = pygame.sprite.Sprite()
    bgSurface.image = pygame.image.load('nightSky0.png').convert()
    player = pgPlayer(32, 32)
    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', player.moveSide)

    mp = list()
    entities = pygame.sprite.Group()
    layerBg = pygame.sprite.Group()
    layerFg = pygame.sprite.Group()

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
    for x in range(len(lev)):
        for y in range(len(lev[0])):
            if lev[x][y] == 'x':
                b = Block(y*32, x*32,)
                collided += [b]
                entities.add(b)
            if lev[x][y] == 'c':
                e = Enemy(y*32, x*32+32//2)
                entities.add(e)
                enemies.append(e)

    layerFg.add(player)
    createEnemies(layerFg)
    randomClouds(layerBg)

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
