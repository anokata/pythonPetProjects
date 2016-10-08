""" Platformer. """
import pyglet
from pyglet.window import key
import random
import math
import sys
sys.path += ["../modules"]
from pygletUtil import *
from stateSystem import *

WindowH = 550
WindowW = 800
WindowTop = 20
WindowLeft = 200
gameWindowHeigth = WindowH - WindowTop
gameWindowWidth = WindowW - WindowLeft

mainDrawnings = list()

def drawMain():
    mainDrawnings[0].draw()

def stateHandleKeyPress(symbol, mod):
    pass
def stateHandleKeyRelease(symbol, mod):
    pass
def stateHanderMousePress(x, y, button, mod):
    pass

def run():
    random.seed()
    window = pyglet.window.Window(width=WindowW, height=WindowH)
    pyglet.gl.glClearColor(0.7,0.5,0.3, 1)
    #pyglet.clock.schedule_interval(self.stateHandle, 1.0/30)

    background = Sprite(pyglet.image.load('../pong/board2.png'), x=100)
    global mainDrawnings
    mainDrawnings += [background]

    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)

    #addState('tst')
    #setChangeHandler('tst','mainRun',lambda: print('tm'))
    #setChangeHandler('mainRun','tst',lambda: print('mt'))
    #changeState('tst')
    #changeState('mainRun')


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

