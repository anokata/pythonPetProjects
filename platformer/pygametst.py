import pygame
import sys
sys.path += ["../modules"]
from stateSystem import *
Sprite = pygame.sprite.Sprite
entities = 0
# делать игрока сначала базового не зависящего от движка.

def makeSpriteXY(imgname, x, y):
    s = pygame.sprite.Sprite()
    s.image = img = pygame.image.load(imgname)
    s.x = x * img.get_rect().size[0]
    s.y = y * img.get_rect().size[1]
    return s

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
    dy = 0
    dx = 0.0
    jumped = False

    def __init__(self):
        #surf
        pass

class pgPlayer(Player, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cat1.png')
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])

    def jump(self, j):
        self.jumped = True


    def moveSide(self, dt, platforms):
        #self.x -= self.dx * dt * self.moving
        if not self.isStand:
            self.dy += gravity

        if self.isStand and self.jumped:
            self.dy = -self.spdj
            self.isStand = False
            self.jumped = False

        self.isStand = False
        #self.y += dt * self.dy
        self.dx = - self.moving * self.spd

        self.rect.y += self.dy
        self.collide(0, self.dy, platforms)
        self.rect.x += self.dx
        self.collide(self.dx, 0, platforms)

    def collide(self, dx, dy, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if dx > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо
                if dx < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if dy > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.isStand = True          # и становится на что-то твердое
                    self.dy = 0                 # и энергия падения пропадает

                if dy < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.dy = 0                 # и энергия прыжка пропадает

    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))

class Block(pygame.sprite.Sprite): # base class for sprites?
    def __init__(self, x, y, imgname=''):
        Sprite.__init__(self)
        self.image = pygame.image.load('block0.png')
        #self.x = x
        #self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def mechanic(dt):
    handleEvent('mechanic', dt)

WindowH = 550
WindowW = 800
Display = (WindowW, WindowH)
bgColor = "#004400"
player = pgPlayer(32, 32)
bgSurface = None
screen = 0
mainDrawnings = list()
collided = list()
gravity = 0.2
#http://www.pygame.org/docs/ref/key.html
def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(Display)
    pygame.display.set_caption("/TXS/")
    global bgSurface
    #bgSurface = pygame.Surface((WindowW, WindowH))
    bgSurface = pygame.sprite.Sprite()
    #bgSurface.fill(pygame.Color(bgColor))
    bgSurface.image = pygame.image.load('nightSky0.png')

    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', player.moveSide)

    global mainDrawnings, collided
    mp = list()
    for x in range(140):
        mp += [(x,2)]
    m = Tiled('ground1.png', mp)
    mainDrawnings += [m]

    mp = list()
    for x in range(140):
        mp += [(x,1)]
    m = Tiled('sky0.png', mp)
    mainDrawnings += [m]

    entities = pygame.sprite.Group()
    for x in range(10):
        b = Block(x*32, 300)
        #mainDrawnings += [b]
        #collided += [b]
        #entities.add(b)

    lev= ["xxxxxxxxxxxxxxxxxxxxxxxxx",
          "x-----x-x-xx-------x----x",
          "x-----------x------x----x",
          "x-----------------------x",
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
                mainDrawnings += [b]
                collided += [b]
                entities.add(b)

    entities.add(player)

    isExit = False
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
        handleEvent('draw')
        handleEvent('mechanic', 1, collided)

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
    for x in mainDrawnings:
        x.draw()
    player.draw()
    #global entities
    #if entities:
    #    entities.draw(screen)
    pygame.display.update()

if __name__ == "__main__":
    main()
