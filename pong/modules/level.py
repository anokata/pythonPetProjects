from block import BaseBlock

class Level:
    blocksGrid = [] #(btype, gridx, gridy)
    blocks = []
    name = 'lv0.lev'
    blockWidth = 32
    blockHeight = 32
    blockLeft = 500
    blockTop = 5
    blockWindowTopStart = 500

    def __init__(self, name, left, top):
        self.blocksGrid = list()
        self.blocks = list()
        self.readLevel(name)
        self.blockLeft = left# - 2.5 * self.blockWidth
        self.blockWindowTopStart = top

    def addBlock(self, btype, x, y):
        self.blocksGrid += [(btype, x, y)]

    def loadBlocks(self, m):
        """ Загрузка блока. """
        for (b, x, y) in self.blocksGrid:
            # тут преобразуем координаты в реальные
            x = x * self.blockWidth + self.blockLeft
            y = self.blockWindowTopStart - y * self.blockHeight + self.blockTop
            self.blocks += [BaseBlock(m, x, y, b)]

    def writeLevel(self):
        """ Сохранение уровня. """
        with open(self.name, 'wt') as fout:
            for (b, x, y) in self.blocks:
                fout.write(str(b) + ' ' + str(x) + ' ' + str(y) + '\n')

    def readLevel(self, name):
        with open(name, 'rt') as fin:
            for line in fin:
                line = line.split()
                self.addBlock(int(line[0]), int(line[1]), int(line[2]))    # тут координаты сетки

    def printLevel(self):
        for (b, x, y) in self.blocksGrid:
            print(b, x, y)

    def getDrawables(self):
        return self.blocks

    def blockCapture(self, block):
        """ При захвате(уничтожение) блока игроком. """
        self.blocks = list(filter(lambda x: x != block, self.blocks))

    def isComplete(self):
        return len(list(filter(lambda x: x.btype == 0, self.blocks))) == 0
