import objects
import pygame
from util import Block, Font
objectFactory = objects.ObjectsFactory()


class GObject(Block):
    
    def __init__(self, name):
        self.baseObject = objectFactory.createObject(name)
        super().__init__(imgname=self.baseObject.imagename)
        self.typ = self.baseObject.typ

    def pack(self):
        return ObjectPack(self)

class ObjectPack():

    count = 1
    obj = None

    def __init__(self, obj):
        self.obj = obj
        self.image = obj.image

    def add(self):
        self.count += 1

    def eatOne(self):
        self.count -= 1

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((100,100))
    g1 = GObject('apple')
    g1.simpleDraw(screen)
    pygame.display.flip()
    import time
    time.sleep(2)

