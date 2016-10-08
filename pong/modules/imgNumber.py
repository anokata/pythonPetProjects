import pyglet
from pygletUtil import *

class ImgNumber:
    """ Генератор цифр числа из изображений. С анимацией. """
    class DrawableNumber:
        """ Механика одного числа. """
        number = []
        lifeTime = 0
        def __init__(self, n, life=0):
            self.number = n
            self.lifeTime = life
        def draw(self):
            for i in self.number:
                i.draw()
        def step(self):
            for x in self.number:
                x.y += 3
            self.lifeTime -= 1
            if self.lifeTime != -1:
                self.fadeout()
            return self.lifeTime

        def fadeout(self):
            """ Исчезание. """
            spd = 8
            for x in self.number:
                if x.opacity - spd >= 0:
                    x.opacity -= spd

    images = []
    numbers = []

    def __init__(self):
        self.images = list()
        self.numbers = list()
        for i in range(10):
            self.images += [pyglet.image.load('nums0/'+str(i) + '.png')]

    def draw(self):
        for i in self.numbers:
            i.draw()

    def step(self):
        self.numbers[:] = filter(lambda x: x.step() != 0, self.numbers)

    def makeNumber(self, n, x, y, lifeTime=-1):
        """ Фабрика создающая число. """
        n = str(n)
        number = list()
        for i in n:
            num = Sprite(self.images[int(i)])
            num.y = y
            num.x = x
            x += num.width
            number += [num]
        self.numbers += [self.DrawableNumber(number, lifeTime)]

    def stopAll(self):
        self.numbers = list()
