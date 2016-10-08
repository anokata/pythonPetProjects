import pygame
import sys
sys.path += ["../modules"]
from stateSystem import *

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
    spd = 2.0
    moving = 0

    def __init__(self):
        #surf
        pass

    def moveSide(self, dt):
        self.x -= self.spd * dt * self.moving

class pgPlayer(Player, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cat0.png')
        self.rect = pygame.Rect(x, y, 20, 20)
        self.x = 20
        self.y = 20

    def draw(self):
        screen.blit(self.image, (self.x,self.y))

def mechanic(dt):
    handleEvent('mechanic', dt)

WindowH = 550
WindowW = 800
Display = (WindowW, WindowH)
bgColor = "#004400"
player = pgPlayer(10, 10)
bgSurface = None
screen = 0
mainDrawnings = list()
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

    global mainDrawnings
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
        handleEvent('mechanic', 1)

def keyDown(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving += -1
    if k == pygame.K_LEFT:
        player.moving += 1

def keyUp(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving += 1
    elif k == pygame.K_LEFT:
        player.moving += -1

def drawMain():
    screen.blit(bgSurface.image, (0, 0))
    for x in mainDrawnings:
        x.draw()
    player.draw()
    pygame.display.update()

if __name__ == "__main__":
    main()
