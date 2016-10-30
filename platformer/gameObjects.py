import objects
import pygame
from map import Block
objectFactory = objects.ObjectsFactory()

class GObject(Block):
    
    def __init__(self, name):
        self.baseObject = objectFactory.createObject(name)
        super().__init__(imgname=self.baseObject.imagename)


if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((100,100))
    g1 = GObject('apple')
    g1.simpleDraw(screen)
    pygame.display.flip()
    import time
    time.sleep(2)

