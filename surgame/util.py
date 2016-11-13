import pygame
import images
import sys
sys.path += ["lib",'./']
import pyganim
from itertools import repeat
from math import hypot

def geomRange(start, count, coeff):
    """ Генератор геометрической прогрессии. """
    x = start
    c = 0
    while c < count:
        x = x * coeff
        c += 1
        yield int(x)

def distance(r1, r2):
    #return (r1.x-r2.x)*(r1.x-r2.x)+(r1.y-r2.y)*(r1.y-r2.y)
    return hypot(r1.x-r2.x, r1.y-r2.y)

def distance4(x, y, a, b):
    """ Вычисление расстояния между двумя точками. """
    return hypot(x-a, y-b)

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

def animLoad(animlist):
    AnimDelay = 0.1 # скорость смены кадров
    animlistdelay = list(zip(animlist, list(repeat(AnimDelay, len(animlist)))))
    ranim = pyganim.PygAnimation(animlistdelay)
    ranim.play()
    return ranim

class Block(pygame.sprite.Sprite): # base class for sprites?
    rect = 0
    def __init__(self, x=0, y=0, imgname=images.defaultBlock):
        Sprite.__init__(self)
        self.anim = False
        if isinstance(imgname, list):
            self.anim = animLoad(imgname)
            self.image = pygame.image.load(imgname[0]).convert_alpha()
            self.image.fill(pygame.Color(0,0,0,0))
            self.anim.blit(self.image, (0, 0))
            size = self.image.get_rect().size
            self.rect = pygame.Rect(x, y, size[0], size[1])
        else:
            self.image = pygame.image.load(imgname).convert_alpha()
            size = self.image.get_rect().size
            self.rect = pygame.Rect(x, y, size[0], size[1])

    def draw(self, x, y, cam, screen):
        if self.anim:
            self.image.fill(pygame.Color(0,0,0,0))
            self.anim.blit(self.image, (0, 0))
        screen.blit(self.image, cam.calcXY(x, y)) 
    def simpleDraw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

class Font():
    def __init__(self, size, color = (255, 255, 255), bgcolor=False):
        self.h = h = size
        self.color = color
        self.bg = bgcolor
        self.font = pygame.font.Font(None, h)

    def render(self, t):
        if self.bg:
            return self.font.render(t, 1, self.color, self.bg)
        else:
            return self.font.render(t, 1, self.color)

    def get_rect(self):
        return self.font.get_rect()


