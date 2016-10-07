from gameTypes import *
import pyglet
from util import *
from pygletUtil import *
from level import Level

class Map:
    blocksAnims = {} # Анимация блоков для получения спрайтов
    # @@ Имена блоков по типам. (вынести куда-то?)
    blockImgNames = {BlockType.ruby : ('block1anim/ruby', 7),
                     BlockType.pearl: ('block6anim/pearl', 7),
                     BlockType.emerald: ('block5anim/emerald', 7)}
    levelsNames = ['lv0.lev']    # имена уровней
    levels = [] # сам уровень формата [(blockType, x, y),...]
    levelsCoords = []    # координаты иконок уровней на карте
    levelsCaps = [] # спрайты иконок уровней на карте
    levelsDone = [] # пройденные уровни
    currentLevel = None
    blockWindowTopStart = 500
    blockWindowLeft = 500
    background = None
    capRadius = 30

    def __init__(self, width, height, mapname):
        self.blockWindowTopStart = height
        self.blockWindowLeft = width
        self.blocksAnims = dict()
        self.levels = list()
        self.levelsCoords = list()
        self.levelsCaps = list()
        self.levelsDone = list() # Список пройденных уровней ! загружать
        self.loadMap(mapname)
        self.loadBlockImages()
        self.loadLevels()

    def loadMap(self, mapname):
        with open(mapname, 'rt') as fin:
            self.background = fin.readline()[:-1] #without \n
            levelDir = fin.readline()[:-1]
            levelCap = pyglet.image.load('levelCap.png')
            center_image(levelCap)
            #Load Levels Coords
            for l in fin:
                l = l.split()
                x = int(l[0])
                y = int(l[1])
                self.levelsCoords += [(x, y)]
                self.levelsCaps += [Sprite(levelCap, x=x, y=y)]
            #print(self.background, levelDir, self.levelsCoords)
        #load levels list
        self.levelsNames = list()
        from os import listdir
        from os.path import isfile, join
        self.levelsNames = [levelDir + f for f in listdir(levelDir) if isfile(join(levelDir, f))]
        self.levelsNames = list(filter(lambda x: x.find('.lev') > -1, self.levelsNames))
        self.levelsNames.sort()
        #load bg
        self.background = Sprite(pyglet.image.load(self.background))

    def loadLevels(self):
        """ Загрузка всех уровней карты. """
        for name in self.levelsNames:
            lev = Level(name, self.blockWindowLeft, self.blockWindowTopStart)
            self.levels += [lev]
            lev.loadBlocks(self)
        self.currentLevel = self.levels[0]

    def loadBlockImages(self):
        """ загрузка изображений блоков. """
        for (b, (imgBaseName, framesCount)) in self.blockImgNames.items():
            frames = list()
            for i in range(1, framesCount+1):
                img = pyglet.image.load(imgBaseName + str(i) + '.png')
                center_image(img)
                frames += [pyglet.image.AnimationFrame(img, 0.2)]
            anim = pyglet.image.Animation(frames)
            self.blocksAnims[b] = anim
        self.levels = list()

    def getBlockAnim(self, btype):
        return self.blocksAnims[btype]

    def getDrawables(self):
        return self.currentLevel.getDrawables()

    def draw(self):
        self.background.draw()
        for x in self.levelsCaps:
            x.draw()

    def loadLevel(self, n):
        self.currentLevel = self.levels[n]
