import pygame
def makeSpriteXY(imgname, x, y):
    s = pygame.sprite.Sprite()
    s.image = img = pygame.image.load(imgname).convert()
    s.rect = img.get_rect()
    w = s.rect.w
    h = s.rect.h
    s.rect.left = x * w
    s.rect.top = y * h
    return s

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


