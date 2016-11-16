import pygame
import gameObjects
from util import Block, distance, distance4
import objectTypes
import enemy
import path
import yaml
import util
import consts
# сначала всё же без генератора, сделать статичный мир. но интересный
# Свойства объектов, проходимые, непроходимые, поднимаемые...
# TODO: map сделать редактор, добавление новых блоков. выбор блоков.

#TODO Переделать загрузку объектов
# Обработка коллизий с нужными объектами
GRIDH = 24
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
    view_dist_shadow = 350
    view_dist = 250
    view_dist_in_cells = 13

    def __init__(self, mapname, screen):
        self.blockers = list()
        self.load(mapname)
        self.screen = screen
        self.makeShadows(15)

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
        self.drawTiles(cam, prect)
        self.drawEnemies(self.player, cam)
        self.drawPlayerBullets(cam)
        self.drawShadow(cam, prect)

    def drawTiles(self, cam, prect):
        v = self.view_dist_in_cells
        for lay in self.tiles:
            for x in range(prect.x//GRIDH - v, prect.x//GRIDH + v):
                for y in range(prect.y//GRIDH - v, prect.y//GRIDH + v):
                    if (x, y) not in lay.keys():
                        continue
                    o = lay[(x, y)]
                    if o:
                        o = o[0]
                        a, b = x * self.blockW, y * self.blockH
                        o.draw(a, b, cam, self.screen)

    def drawPlayerBullets(self, cam):
        self.drawBullets(self.player.bullets, cam)

    def drawBullets(self, buls, cam):
        for b in buls:
            b.draw(b.rect.x, b.rect.y, cam, self.screen)

    def makeShadows(self, n):
        self.shadowimg = util.imgLoad('objects/shadow.png')
        self.shadowimg = pygame.transform.scale(self.shadowimg, consts.Display)

    def drawShadow(self, cam, prect):
        self.screen.blit(self.shadowimg, pygame.Rect(0,0,800,800))
    
    def drawEnemies(self, player, cam):
        for e in self.enemiesInstances: 
            r = e.getRect(cam)
            p = cam.calc(player)
            d = distance(p, r)
            if d < self.view_dist:
                e.draw(cam)
                self.drawBullets(e.bullets, cam)

    def mechanic(self, d, p, e):
        for e in self.enemiesInstances:
            e.go(d, p, e)

    def load_from_file(self, mapname):
        mapname = path.getPath(mapname)
        map_data = yaml.load(open(mapname))
        return map_data

    def load(self, mapname):
        self.layers = layers = list() 
        if isinstance(mapname, str):
            map_data = self.load_from_file(mapname)
        else:
            map_data = mapname
        layersCount = int(map_data['layers_count'])
        self.layersCount = layersCount
        for l in map_data['layers']:
            layers.append(l.split('\n')[:-1])
        objectNames = map_data['objects']
        self.objectNames = objectNames 
        self.blockW = self.blockH = GRIDH # CHG REad

        mapObjects = dict()
        for objectName in objectNames:
            obj = gameObjects.GObject(objectName)
            mapObjects[obj.baseObject.mapchar] = obj
            
        i = 0
        self.blockers = list()
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

if __name__ == '__main__':
       Map('data/town.yaml', 0) 

