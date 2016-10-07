from pygletUtil import *
from gameTypes import *

class BaseBlock(HasSprite):
    btype = None
    Health = 0
    price = 0

    def __init__(self, m, x, y, btype):
        self.sprite = Sprite(m.getBlockAnim(btype), x=x, y=y)
        self.btype = btype
        # stats(Heath, price)
        baseStats = {BlockType.emerald: (2, 30),
                     BlockType.ruby: (2, 150),
                     BlockType.pearl: (1, 10)}
        (self.Health, self.price) = baseStats[btype]

    def capture(self):
        self.sprite.visible = False

    def draw(self):
        self.sprite.draw()
