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
import eventSystem

Sprite = pygame.sprite.Sprite

#TODO: наделать много вещей. коллекционирование. инвентарь. иконки.
#TODO: Систему событий с очередью. (звуки)

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

def toInventory():
    player.stop()
    changeState('inventory')

def toMenu():
    player.stop()
    runMenu('men1')

def shoot():
    player.startShoot()

def shootEvent(e):
    snd.pou.play()

def playerMove(k):
    player.send('playerMove', 'R')
    keyfuncs = {
        pygame.K_RIGHT: player.movingRight,
        pygame.K_LEFT: player.movingLeft,
        pygame.K_UP: player.movingUp,
        pygame.K_DOWN: player.movingDown,
            }
    fun = keyfuncs.get(k, False)
    if fun:
        fun()

def keyDown(k, d):
    global player
    keyfuncs = {
        pygame.K_RIGHT: (playerMove, k),
        pygame.K_LEFT: (playerMove, k),
        pygame.K_UP: (playerMove, k),
        pygame.K_DOWN: (playerMove, k),
        pygame.K_x: (shoot, None),
        pygame.K_z: (player.kick, None),
        pygame.K_i: (toInventory, None),
        pygame.K_SPACE: (toMenu, None),
        pygame.K_e: (player.eat, None)
            }
    fun, arg = keyfuncs.get(k, (False, None))
    if fun and arg != None:
        fun(arg)
    elif fun:
        fun()

def playerStop(x):
    player.send('playerStop', 'w')
    player.stop(x)

def playerStopShoot():
    player.stopShoot()

def keyUp(k, d):
    global player
    keyfuncs = {
        pygame.K_RIGHT: (playerStop, True),
        pygame.K_LEFT: (playerStop, True),
        pygame.K_UP: (playerStop, False),
        pygame.K_DOWN: (playerStop, False),
        pygame.K_x: (playerStopShoot, None),
        }
    fun, arg = keyfuncs.get(k, (False, None))
    if fun and arg != None:
        fun(arg)
    elif fun:
        fun()

#TODO Health Bar Progress!
class Hud():
    items = []
    enrg = 'Energy: %.2f'
    hp = 'HP: %d'

    hpBarBg = None
    H = 24
    HP_W = 100
    HP_PAD = 10
    HP_COLOR = (255, 4, 0)

    def __init__(self, layer, x=0, y=30):
        self.layer = layer
        i = self.items = list()
        self.id = 'hud'
        self.rect = pygame.Rect(0,0,0,0)
        self.font = Font(self.H, (250, 20, 90))
        self.x = x
        self.y = y
        i.append(self.hp)

        self.hpBarBg = pygame.Surface((100, self.H))
        self.hpBarBg = pygame.image.load(images.hpbarrectimg)
        #self.hpBarBg.fill((255, 255, 50))
        self.hpRect = pygame.Rect(x, y+self.H, 0, 0)
        self.hpBar = pygame.Surface((self.HP_W - self.HP_PAD*2, self.H//1.8))
        #self.hpBar = pygame.image.load(images.hpbarimg)
        self.hpBar.fill(self.HP_COLOR)
        self.hpbarRect = pygame.Rect(x+self.HP_PAD, y+self.H//0.8, 0, 0)
        self.refresh()

    def refresh(self):
        self.layer[self.id] = list()
        y = self.y
        if player.health > 0:
            #self.hpBar = pygame.Surface((int(self.HP_W*abs(player.health/100.0)*0.8), self.H//1.8))
            self.hpBar = pygame.transform.scale(self.hpBar, (int(self.HP_W*abs(player.health/100.0)*1.0), int(self.H//1.8)))

        for x in self.items:
            #t = self.font.render(x % player.energy)
            t = self.font.render(x % player.health)
            self.rect = t.get_rect()
            self.rect.top = y
            self.rect.left = self.x
            y += self.font.h // 1.5
            self.layer[self.id].append((t, self.rect))

    def draw(self, screen):
        screen.blit(self.hpBarBg, self.hpRect) 
        screen.blit(self.hpBar, self.hpbarRect) 
        for (e, r) in self.layer[self.id]:
            screen.blit(e, r)


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
    hud.draw(screen)
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
    global snd
    mainSubsriber.process()
    snd.mech()
    r = player.moveSide(d, p, e)
    collideObjects()
    for e in enemies:
        e.randomMove(d, p, e)
        e.go(d, p, e)
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
                #TODO надо очищать
                player.send('teleport', p.obj.baseObject.mapname)

#TODO звуковой модуль
class Sounds():
    def __init__(self):
        self.que = list()
        try:
            #pygame.mixer.pre_init(44100, -16, 8, 1024)
            pygame.mixer.pre_init(22050, -16, 1, 256)
            pygame.mixer.init()
            #snd = pygame.mixer.Sound('yabc.wav')
            #snd.set_volume(0.3)
            #snd.play()
            sndpou = pygame.mixer.Sound('sounds/piu2.wav')
            self.pou = sndpou
            self.step = pygame.mixer.Sound('sounds/step.wav')
            self.step.set_volume(0.3)
            self.bulletWall = pygame.mixer.Sound('sounds/bom.wav')
            self.explosion = pygame.mixer.Sound('sounds/expl.wav')
        except Exception(e):
            print(e)
    
    def add(self,s):
        if s not in self.que:
            self.que.append(s)

    def stop(self,s):
        self.que.remove(s)

    def mech(self):
        for s in self.que:
            s.play()

snd = 0
mainSubsriber = eventSystem.Subscriber()

def bulletEvent(e):
    snd.bulletWall.play()

def walkEvent(e):
    snd.step.play(loops=-1)

def walkStopEvent(e):
    snd.step.stop()

def killEvent(e):
    snd.explosion.play()

def dieEvent(e):
    loadMap(currentMap)

def mapChange(e):
    global currentMap
    currentMap = e.data
    loadMap(currentMap)

#TODO Прибраться, сгруппировать, выделить модули.
def main():
    global snd
    snd = Sounds()
    pygame.init()
    mainSubsriber.register('bullet', bulletEvent) # TODO имена событий отдельно
    mainSubsriber.register('playerMove', walkEvent)
    mainSubsriber.register('playerStop', walkStopEvent)
    mainSubsriber.register('killed', killEvent)
    mainSubsriber.register('shoot', shootEvent)
    mainSubsriber.register('die', dieEvent)
    mainSubsriber.register('teleport', mapChange)

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
currentMap = 'data/map.map'

def loadMap(mapname):
    global globmap
    global screen
    global collided, player, enemies
    enemies = list()
    globmap = Map(mapname, screen)
    collided = globmap.blockers # CHG TODO возвращать словарь?
    #globmap.save()
    #TODO игрока пересоздавать не надо, либо загружать
    player = pgPlayer(globmap.px, globmap.py, screen, globmap)
    eFactory = enemy.EnemyFactory(screen, globmap)

    for (x, y), (name, count) in globmap.enemies.items():
        for i in range(count):
            e = eFactory.create(name, x, y)
            e.hunt(player)
            enemies.append(e)

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
    hud = Hud(textLayer, WindowW-170, WindowH-70)

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
    print('last event: ', pygame.event.poll())
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()