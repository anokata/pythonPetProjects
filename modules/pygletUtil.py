import pyglet
from util import *
Sprite = pyglet.sprite.Sprite

class HasSprite():
    """ Базовый класс для имеющих спрайт.
    Реализует простой доступ к некоторым полям через проперти """
    sprite = None
    def x_get(self):
        return self.sprite.x
    def y_get(self):
        return self.sprite.y
    def x_set(self, x):
        self.sprite.x = x
    def y_set(self, y):
        self.sprite.y = y
    x = property(x_get, x_set)
    y = property(y_get, y_set)
    def width_get(self):
        return self.sprite.width
    def height_get(self):
        return self.sprite.height
    def width_set(self, w):
        self.sprite.width = w
    def height_set(self, h):
        self.sprite.height = h
    width = property(width_get, width_set)
    height = property(height_get, height_set)

    def draw(self):
        self.sprite.draw()
    def distanceFrom(self, obj):
        return distance(self.x, self.y, obj.x, obj.y)


labels = list()

def makeLabel(text, x, y, size = 18):
    return pyglet.text.Label(text=text, x=x, y=y, font_size=size)

def addLabel( updateFun, initText, updateParam, x, y):
    global labels
    labels += [(makeLabel(initText, x=x, y=y), updateFun, updateParam)]

def updateLabels():
    global labels
    for (lab, (fun, param)) in labels:
        lab.text = fun(param)

#pyglet.clock.schedule_once(self.stateToMap, 3)

def center_image(image):
    """ Центрирование якорной точки изображения. """
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def makeSprite(imgname, x=0,y=0, center=False):
    img = pyglet.image.load(imgname)
    if center:
            center_image(img)
    s = Sprite(img, x=x, y=y)
    return s

def makeSpriteXY(imgname, x=0,y=0):
    """ Устанавливает спрайт в позицию относительно сетки из его размеров. """
    img = pyglet.image.load(imgname)
    x = x * img.width
    y = y * img.height
    s = Sprite(img, x=x, y=y)
    return s
