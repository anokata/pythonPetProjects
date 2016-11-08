import pygame
from consts import *
#Камера. у неё есть свои размеры и положение. она не даёт выйти за пределы игроку - меняет положение, следит. Она преобразует данные в неё координаты объекта так чтобы они отображались на экране( вычесть координаты камеры)
class Camera():

    def __init__(self, w, h):
        self.rect = pygame.Rect(0, 0, w, h)

    def stalkAt(self, p):
        """ Следить за """
        self.rect.left = min(self.rect.left, p.rect.left - WindowW//2) 
        self.rect.right = max(self.rect.right, p.rect.right)
        self.rect.top = min(self.rect.top, p.rect.top - WindowH//2)
        self.rect.right = max(self.rect.right, p.rect.right)
        self.rect.bottom = max(self.rect.bottom, p.rect.bottom)

    def calcXY(self, x, y):
        """ пересчитать координаты объекта на экран """
        r = pygame.Rect(0, 0, 0, 0)
        r.left = x - self.rect.left #- WindowH//2
        r.top = y - self.rect.top #+ WindowW//2
        return r

    def calc(self, o):
        """ пересчитать координаты объекта на экран """
        r = pygame.Rect(0, 0, 0, 0)
        r.left = o.rect.left - self.rect.left #- WindowH//2
        r.top = o.rect.top - self.rect.top #+ WindowW//2
        #r.left = o.rect.left - self.rect.left
        #r.left = o.rect.left - self.rect.left
        return r


