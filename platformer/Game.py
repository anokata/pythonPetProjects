""" . """
import pyglet
from pyglet.window import key
import random
import math
import sys
sys.path += ["../modules"]
from pygletUtil import *
from stateSystem import *
from makeAnimation import makeAnimObj
from Tiled import *

WindowH = 550
WindowW = 800
WindowTop = 20
WindowLeft = 200
FPS = 30
gameWindowHeigth = WindowH - WindowTop
gameWindowWidth = WindowW - WindowLeft
window = None
mainDrawnings = list()

def drawMain():
    global window
    window.clear()
    global mainDrawnings
    for x in mainDrawnings:
        x.draw()

def mechanic(x):
    handleEvent('mechanic')

def pygletRun():
    random.seed()
    global window
    window = pyglet.window.Window(width=WindowW, height=WindowH)
    pyglet.gl.glClearColor(0.7,0.5,0.3, 1)
    pyglet.clock.schedule_interval(mechanic, 1.0/FPS)

    @window.event
    def on_draw():
        handleEvent('draw')
    @window.event
    def on_key_press(symbol, mod):
        handleEvent('keyPress', symbol, mod)
    @window.event
    def on_key_release(symbol, mod):
        handleEvent('keyRelease', symbol, mod)
    @window.event
    def on_mouse_press(x, y, button, mod):
        handleEvent('keyMousePress', x, y, button, mod)

    pyglet.app.run()


def gameInit():
    background = makeSprite('nightSky0.png')
    global mainDrawnings
    mainDrawnings += [background]

    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    #setEventHandler('mainRun', 'mechanic', lambda: print(1))
    #addState('tst')
    #setChangeHandler('tst','mainRun',lambda: print('tm'))
    #setChangeHandler('mainRun','tst',lambda: print('mt'))
    #changeState('tst')
    #changeState('mainRun')

    a = makeAnimObj('../pong/block6anim/pearl', 100, 100, 8, 0.1)
    mainDrawnings += [a]

    mp = list()
    for x in range(30):
        mp += [(x,2)]
    m = Tiled('ground1.png', mp)
    mainDrawnings += [m]

    mp = list()
    for x in range(30):
        mp += [(x,3)]
    m = Tiled('sky0.png', mp)
    mainDrawnings += [m]

    cat = makeSprite('cat0.png', 64,64)
    mainDrawnings += [cat]

def run():
    gameInit()
    pygletRun()
