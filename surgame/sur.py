import pygame
import sys
sys.path += ["lib",'./']
from stateSystem import *
#import roomGenerator as rg
import random
from menu import *
from player import *
from camera import *
from consts import *
#from util import makeSpriteXY
from map import *
import gameObjects
import gameInventory
import enemy
import bullet
import images
import datafiles

Sprite = pygame.sprite.Sprite

#TODO: наделать много вещей. коллекционирование. инвентарь. иконки.

# Globals
bgSurface = None
screen = 0
collided = list()
enemies = list()
cam = Camera(400, 300)
entities = None
textLayer = None

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
    r = handleEvent('mechanic', dt)
    return r

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
    keyfuncs = { #TODO refactor other upper
        pygame.K_x: player.shoot,
            }
    fun = keyfuncs.get(k, False)
    if fun:
        fun()

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
    hp = 'HP: %d'

    def __init__(self, layer, x=0, y=10):
        self.layer = layer
        i = self.items = list()
        self.id = 'hud'
        self.rect = pygame.Rect(0,0,0,0)
        self.font = Font(24, (250, 250, 90))
        self.x = x
        self.y = y
        i.append(self.hp)
        self.refresh()

    def refresh(self):
        self.layer[self.id] = list()
        y = self.y
        for x in self.items:
            #t = self.font.render(x % player.energy)
            t = self.font.render(x % player.health)
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
    global cam, player, textLayer, globmap, enemies
    cam.stalkAt(player)
    
    globmap.draw(cam) 
    #screen.blit(player.image, player.getRect(cam))
    for (e, r) in textLayer['hud']:
        screen.blit(e, r)
    player.draw(cam)
    for e in enemies:
        screen.blit(e.image, e.getRect(cam))

    pygame.display.flip()

def drawInventory():
    screen.blit(bgSurface.image, (0, 0))
    global player
    if player.inventory:
        player.inventory.draw()
    pygame.display.flip()

def mainMechanic(d, p, e):
    r = player.moveSide(d, p, e)
    collideObjects()
    for e in enemies:
        e.randomMove(d, p, e)
    hud.refresh()
    return r

def collideObjects():
#if self.canPickUp:
    global player, globmap, collided
    for p in collided:
        if pygame.sprite.collide_rect(player, p):
            if p.obj.typ == FOOD:
                if player.inventory.add(p.obj):
                    #надо убрать объект с карты
                    globmap.removeObject(p)
            elif p.obj.typ == PORTAL:
                loadMap(p.obj.baseObject.mapname)

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(Display)
    pygame.display.set_caption("/SurGame/")
    mainInit()
    mainLoop()

#class World():
player = None
menu = None
hud = None
globmap = 0

def loadMap(mapname):
    global globmap
    global screen
    global collided, player, enemies
    globmap = Map(mapname, screen)
    collided = globmap.blockers # CHG
    #globmap.save()
    player = pgPlayer(globmap.px, globmap.py, screen, globmap)
    eFactory = enemy.EnemyFactory(screen, globmap)

    for i in range(10):
        enemies.append(eFactory.create('poringb', 100*i, 120))
        enemies.append(eFactory.create('poringp', 200*i, 120))

def stateInit():
    addState('mainRun')
    addState('inventory')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyDown', keyDown)
    setEventHandler('mainRun', 'keyUp', keyUp)
    setEventHandler('mainRun', 'mechanic', mainMechanic)
    setEventHandler('inventory', 'draw', drawInventory)
    setEventHandler('inventory', 'keyDown', inventoryKeyDown)

def bgInit():
    global bgSurface
    bgSurface = pygame.sprite.Sprite()
    bgSurface.image = pygame.image.load(images.bg).convert()
    #bgSurface.image = pygame.Surface([800,1000])
    #bgSurface.image.fill((0,0,0))

def mainInit():
    stateInit()
    bgInit()
    loadMap(datafiles.defmap)

    global Layers, textLayer
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
