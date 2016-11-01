import pygame
import gameObjects
from util import Block
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
    w = h = z = 0
    blockers = 0

    def __init__(self, z, screen):
        self.blockers = list()
        self.z = z
        self.load()
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
    
    def draw(self, cam):
        for lay in self.tiles:
            for (x,y), o in lay.items():
                if o:
                    o = o[0]
                    a, b = x * self.blockW, y * self.blockH
                    o.draw(a, b, cam, self.screen)

    def load(self):
        self.layers = layers = list() 
        with open('map.map', 'rt') as fin:
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

        z = self.z
        i = 0
        self.layersDim = list()
        self.tiles = list()
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
                    char = lev[y][x]
                    if char in mapObjects:
                        self.tiles[i][x,y] += [mapObjects[char]]
                        if mapObjects[char].baseObject.collided:
                            obj = mapObjects[char]
                            a, b = (x-0) * self.blockW, (y-0) * self.blockH
                            self.blockers.append(PhisycBlock(a, b, obj.rect.width, obj))
            i += 1

    def save(self):
        with open('map.map', 'wt') as fout:
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


