import pygame
# сначала всё же без генератора, сделать статичный мир. но интересный
# Свойства объектов, проходимые, непроходимые, поднимаемые...
# TODO: map сделать редактор, добавление новых блоков. выбор блоков.

#TODO Переделать загрузку объектов
Sprite = pygame.sprite.Sprite

class Block(pygame.sprite.Sprite): # base class for sprites?
    rect = 0
    def __init__(self, x=0, y=0, imgname='block1.png'):
        Sprite.__init__(self)
        self.image = pygame.image.load(imgname).convert()
        size = self.image.get_rect().size
        #print(x,y, self.image, imgname, size, pygame.Rect)
        self.rect = pygame.Rect(x, y, size[0], size[1])

    def draw(self, x, y, cam, screen):
        screen.blit(self.image, cam.calcXY(x, y)) 
    def simpleDraw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

class PhisycBlock():
    rect = 0
    def __init__(self, x, y, w):
        self.rect = pygame.Rect(x, y, w, w)

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

            descrp = dict()
            while True:
                char = fin.read(1)
                if char == '\n':
                    break
                fin.read(1) # space
                imgpath = fin.readline()[:-1]
                descrp[char] = (imgpath,)

        self.lev = layers[0] # CHG
        self.descrp = descrp
        self.blockW = self.blockH = 42
        mapObjects = dict()
        for c, p in descrp.items():
            imgpath = p[0]
            sprite = Block(imgname=imgpath)
            mapObjects[c] = (sprite,)

        z = self.z
        i = 0
        self.layersDim = list()
        self.tiles = list()
        for lev in self.layers:
            w = len(lev[0])
            h = len(lev) 
            self.layersDim.append((w, h))

            self.w = w # layer CHG
            self.h = h

            self.tiles.append(dict())
            for x in range(w):
                for y in range(h):
                    self.tiles[i][x,y] = list()
                    if lev[y][x] == '.':
                        continue
                    self.tiles[i][x,y] += [mapObjects[lev[y][x]][0]]
                    if lev[y][x] == 'x': # CHG
                        a, b = x * self.blockW, y * self.blockH
                        self.blockers.append(PhisycBlock(a, b, self.blockW))
            i += 1

    def save(self):
        with open('map.map', 'wt') as fout:
            fout.write(str(self.layersCount) + '\n')
            for lay in self.layers:
                for l in lay: # CHG Layers for all
                    fout.write(l+'\n')
                fout.write('\n')
            for c, img in self.descrp.items():
                img = img[0]
                fout.write(c + ' ' + img)
                fout.write('\n')
            fout.write('\n')


