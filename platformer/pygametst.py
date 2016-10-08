import pygame
import sys
sys.path += ["../modules"]
from stateSystem import *

# делать игрока сначала базового не зависящего от движка.

class Player():
    health = 100
    spd = 300
    moving = False

    def __init__(self):
        #surf
        pass

    def moveSide(self, dt):
        if self.moving == 1: #right
            self.x += self.spd * dt
        elif self.moving == -1:
            self.x -= self.spd * dt


def mechanic(dt):
    handleEvent('mechanic', dt)

WindowH = 550
WindowW = 800
Display = (WindowW, WindowH)
bgColor = "#004400"
player = Player()
bgSurface = None
screen = 0

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(Display)
    pygame.display.set_caption("/TXS/")
    global bgSurface
    bgSurface = pygame.Surface((WindowW, WindowH))
    bgSurface.fill(pygame.Color(bgColor))

    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', player.moveSide)


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

def keyDown(k, d):
    global player
    if k == pygame.K_RIGHT:
        player.moving = 1
    if k == pygame.K_LEFT:
        player.moving = -1

def keyUp(k, d):
    global player
    if k == pygame.K_RIGHT or k == pygame.K_LEFT:
        player.moving = False

def drawMain():
    screen.blit(bgSurface, (0, 0))
    pygame.display.update()

if __name__ == "__main__":
    main()
