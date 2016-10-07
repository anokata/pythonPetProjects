from pygletUtil import *
import math

class Particles:
    """ Система частиц. """
    sprites = []
    speed = 2
    lifeTime = 100
    initLifeTime = 0
    speedDown = 0

    def __init__(self, img, n, lifeTime, x=0, y=0, speed=2, speedDown=0):
        self.sprites = list()    # Необходимо все неэлемнтарные типы так создавать
        self.lifeTime = 0
        self.initLifeTime = lifeTime
        self.speed = speed
        self.speedDown = 1 if speedDown == 0 else (100 - speedDown)/100
        for i in range(n):
            s = Sprite(img, x=x, y=y)
            s.dx = math.cos(math.radians(360*i/n)) * self.speed
            s.dy = math.sin(math.radians(360*i/n)) * self.speed
            self.sprites += [s]

    def draw(self):
        if 0 != self.lifeTime:
            for x in self.sprites:
                x.draw()

    def step(self):
        if 0 == self.lifeTime:
            self.end()
            return
        self.lifeTime -= 1
        for x in self.sprites:
            x.x += x.dx
            x.y += x.dy
            x.dx *= self.speedDown
            x.dy *= self.speedDown
            x.opacity -= 30

    def end(self):
        pass

    def restart(self, x, y):
        for i in self.sprites:
            i.x = x
            i.y = y
            i.opacity = 255
        self.lifeTime = self.initLifeTime
