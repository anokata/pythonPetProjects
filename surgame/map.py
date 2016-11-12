import pygame
import gameObjects
from util import Block, distance
import objectTypes
import enemy
# сначала всё же без генератора, сделать статичный мир. но интересный
# Свойства объектов, проходимые, непроходимые, поднимаемые...
# TODO: map сделать редактор, добавление новых блоков. выбор блоков.

#TODO Переделать загрузку объектов
# Обработка коллизий с нужными объектами
GRIDH = 42
ObjectLayer = 1
class PhisycBlock():
    rect = 0
    obj = None
    def __init__(self, x, y, w, obj):
        self.rect = pygame.Rect(x, y, w, w)
        self.obj = obj

class Map():
    tiles = 0
    w = h = 0
    blockers = 0
    lights = None
    px = py = 0

    def __init__(self, mapname, screen):
        self.blockers = list()
        self.load(mapname)
        self.screen = screen

    def __setitem__(self, k, v):
        self.tiles[k] = v

    def __getitem__(self, k):
        return self.tiles[k]

    def removeObject(self, phisObj):
        obj = phisObj.obj
        rect = phisObj.rect
        x = rect.left // GRIDH
        y = rect.top // GRIDH
        if obj in self.tiles[ObjectLayer][x,y]:
            self.tiles[ObjectLayer][x,y].remove(obj)
        self.blockers.remove(phisObj)
        #remove from phis objs
    
    def draw(self, cam, prect):
        for lay in self.tiles:
            for (x,y), o in lay.items():
                if o:
                    r = cam.calcXY(x*GRIDH, y*GRIDH)
                    p = cam.calcXY(prect.x, prect.y)
                    d = distance(p, r)

                    if d < 300:
                        o = o[0]
                        a, b = x * self.blockW, y * self.blockH
                        o.draw(a, b, cam, self.screen)

        self.drawEnemies(self.player, cam)
        self.drawShadow(cam, prect)

    def drawShadow(self, cam, prect):
        shadow0 = pygame.Surface([GRIDH, GRIDH], flags=pygame.SRCALPHA)
        shadow0.fill((0,0,0,255))
        shadow = pygame.Surface([GRIDH, GRIDH], flags=pygame.SRCALPHA)
        shadow.fill((0,0,0,200))
        shadow2 = pygame.Surface([GRIDH, GRIDH], flags=pygame.SRCALPHA)
        shadow2.fill((0,0,0,150))
        shadow3 = pygame.Surface([GRIDH, GRIDH], flags=pygame.SRCALPHA)
        shadow3.fill((0,0,0,100))
        for x in range(self.w):
            for y in range(self.h):
                #if (x, y) not in self.lights.keys():
                    r = cam.calcXY(x*GRIDH, y*GRIDH)
                    p = cam.calcXY(prect.x, prect.y)
                    d = distance(p, r)
                    if d > 300:
                        self.screen.blit(shadow0, pygame.Rect(r.x, r.y, GRIDH, GRIDH))
                    elif d > 200:
                        self.screen.blit(shadow, pygame.Rect(r.x, r.y, GRIDH, GRIDH))
                    elif d > 150:
                        self.screen.blit(shadow2, pygame.Rect(r.x, r.y, GRIDH, GRIDH))
                    elif d > 100:
                        self.screen.blit(shadow3, pygame.Rect(r.x, r.y, GRIDH, GRIDH))

    def drawEnemies(self, player, cam):
        for e in self.enemiesInstances: 
            r = e.getRect(cam)
            p = cam.calc(player)
            d = distance(p, r)
            if d < 200:
                self.screen.blit(e.image, e.getRect(cam))

    def mechanic(self, d, p, e):
        for e in self.enemiesInstances:
            e.go(d, p, e)

    def load(self, mapname):
        self.blockers = list()
        self.layers = layers = list() 
        with open(mapname, 'rt') as fin:
            line = 'trash'
            layersCount = int(fin.readline())
            self.layersCount = layersCount
            for i in range(layersCount):
                layers.append(list())
                while True:
                    line = fin.readline()
                    if line == '\n':
                        break
                    layers[i].append(line[:-1])

            objectNames = list()
            while True:
                objectName = fin.readline()[:-1]
                if objectName == 'endObjectNames':
                    break
                objectNames.append(objectName)

        self.objectNames = objectNames 
        self.blockW = self.blockH = GRIDH # CHG REad
        mapObjects = dict()
        # Объекты должны быть и разные, по экземпляру каждый раз. а может и нет. Просто для множества сделать ПакОбъект. а на карте они остаются в других ячейках же.
        for objectName in objectNames:
            obj = gameObjects.GObject(objectName)
            mapObjects[obj.baseObject.mapchar] = obj

        i = 0
        self.layersDim = list()
        self.tiles = list()
        self.enemies = dict()
        self.lights = dict()

        for lev in self.layers:
            w = len(lev[0])
            h = len(lev) 
            self.layersDim.append((w, h))

            self.w = w # not need?
            self.h = h

            self.tiles.append(dict())
            for x in range(w):
                for y in range(h):
                    self.tiles[i][x,y] = list()
                    if lev[y][x] == '.':
                        continue
                    if lev[y][x] == '~':
                        self.px = x * self.blockW
                        self.py = y * self.blockW
                        self.lights[(x, y)] = 3
                        
                    char = lev[y][x]
                    if char in mapObjects:
                        obj = mapObjects[char]
                        self.tiles[i][x,y] += [obj]

                        if obj.typ == objectTypes.ENEMY:
                            self.enemies[(x*self.blockW, y*self.blockW)] = (obj.baseObject.name, obj.baseObject.count)

                        if mapObjects[char].baseObject.collided:
                            obj = mapObjects[char]
                            a, b = (x-0) * self.blockW, (y-0) * self.blockH
                            self.blockers.append(PhisycBlock(a, b, obj.rect.width, obj))
            i += 1

    def loadEnemies(self, player):
        eFactory = enemy.EnemyFactory(self.screen, self)
        self.enemiesInstances = list()
        for (x, y), (name, count) in self.enemies.items():
            for i in range(count):
                e = eFactory.create(name, x, y)
                e.hunt(player)
                self.enemiesInstances.append(e)


    def save(self, mapname):
        with open(mapname, 'wt') as fout:
            fout.write(str(self.layersCount) + '\n')
            for lay in self.layers:
                for l in lay: # CHG Layers for all
                    fout.write(l+'\n')
                fout.write('\n')
        #CHNG!!!
            for c, img in self.descrp.items():
                img = img[0]
                fout.write(c + ' ' + img)
                fout.write('\n')
            fout.write('\n')


