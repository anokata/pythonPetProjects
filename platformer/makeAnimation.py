""" . """
import sys
sys.path += ["../modules"]
from pygletUtil import *
import pyglet
from util import *

def makeAnim(imgName, x, y, framesCount, delay):
    """ Создание cпрайта анимации. """
    frames = list()
    for i in range(0, framesCount-1):
        img = pyglet.image.load(imgName + str(i) + '.png')
        center_image(img)
        frames += [pyglet.image.AnimationFrame(img, delay)]
    anim = pyglet.image.Animation(frames)
    sprite = Sprite(anim, x=x, y=y)
    return sprite


def makeAnimObj( imgName, x, y, framesCount, delay):
    """ Создание объекта с анимацией. """
    obj = HasSprite()
    obj.sprite = makeAnim(imgName, x, y, framesCount, delay)
    return obj



