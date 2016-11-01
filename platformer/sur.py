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
#from util import makeSpriteXY
from map import *
import gameObjects
import gameInventory
Sprite = pygame.sprite.Sprite

#TODO: наделать много вещей. коллекционирование. инвентарь. иконки.

# Globals
player = None
bgSurface = None
screen = 0
collided = list()
enemies = list()
cam = Camera(400, 300)
#http://www.pygame.org/docs/ref/key.html
entities = None
textLayer = None
menu = None
hud = None
globmap = 0
inventory = 0

def inventoryKeyDown(k, d):
    if k == pygame.K_i:
        changeState('mainRun')

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
    if k == pygame.K_z:
        player.kick()
    if k == pygame.K_i:
        changeState('inventory')

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
    #screen.set_colorkey((0,0,0))
    screen.blit(bgSurface.image, (0, 0))
    global cam, player, textLayer, globmap, inventory
    cam.stalkAt(player)
    
    for (e, r) in textLayer['hud']:
        screen.blit(e, r)

    globmap.draw(cam) 
    screen.blit(player.image, player.getRect(cam))
    pygame.display.flip()

def drawInventory():
    screen.blit(bgSurface.image, (0, 0))
    global inventory
    if inventory:
        inventory.draw()
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
    global collided, cam, player, enemies, Layers, textLayer, inventory
    global bgSurface
    screen = pygame.display.set_mode(Display)
    pygame.display.set_caption("/TXS/")

    bgSurface = pygame.sprite.Sprite()
    bgSurface.image = pygame.image.load('nightSky0.png').convert()
    bgSurface.image = pygame.Surface([800,1000])
    bgSurface.image.fill((0,0,0))
    player = pgPlayer(44, 44)
    addState('mainRun')
    addState('inventory')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', mainMechanic)
    setEventHandler('inventory', 'draw', drawInventory)
    setEventHandler('inventory', 'keyDown', inventoryKeyDown)
    
    global globmap
    b = Block()
    globmap = Map(2, screen)
    collided = globmap.blockers # CHG
    #globmap.save()

    mp = list()
    entities = list()
    textLayer = {'menu1': list()}

    # menu
    global menu, hud
    menu = createMenu('men1', ['it0','it2','end'])
    hud = Hud(textLayer, WindowW-150, WindowH-30)

    # gobj test
    g1 = gameObjects.GObject('apple')
    #print(g1.typ)
    #TODO добавление объекта, вишни, и чтобы стало 2 яблока. переключение категорий. выбор объектов, действия.
    inventory = gameInventory.GInventory(screen)
    inventory.add(g1)
    #print(inventory.food)

def mainLoop():
    clock = pygame.time.Clock()
    isExit = False
    pygame.time.set_timer(pygame.USEREVENT + 1, int(1000/90))
    while not isExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isExit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isExit = True
                    break
                handleEvent('keyDown', event.key, event)
            if event.type == pygame.KEYUP:
                handleEvent('keyUp', event.key, event)
            if event.type == pygame.USEREVENT + 1:
                handleEvent('mechanic', 1, collided, enemies)
        clock.tick()
        pygame.display.set_caption("fps: " + str(int(clock.get_fps())))
        handleEvent('draw')
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
