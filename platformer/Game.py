""" . """
import pyglet
from pyglet.window import key
from pyglet import clock
import random
import math
import sys
sys.path += ["../modules"]
from pygletUtil import *
from stateSystem import *
from makeAnimation import makeAnimObj
from Tiled import *
from Player import Player

WindowH = 550
WindowW = 800
WindowTop = 20
WindowLeft = 200
FPS = 40
gameWindowHeigth = WindowH - WindowTop
gameWindowWidth = WindowW - WindowLeft
window = None
mainDrawnings = list()
player = None

def drawMain():
    global window
    window.clear()
    global mainDrawnings
    for x in mainDrawnings:
        x.draw()
    fps_display.draw()

t = 0
def mechanic(dt):
    global t
    t += 1
    print(dt,1.0/120, t, 'FPS is %f' % clock.get_fps())
    handleEvent('mechanic', dt)

fps_display = 0

def pygletRun():
    random.seed()
    global window
    window = pyglet.window.Window(width=WindowW, height=WindowH)
    pyglet.gl.glClearColor(0.7,0.5,0.3, 1)

    gameInit()

    global fps_display
    fps_display = clock.ClockDisplay()
    clock.set_fps_limit(50)

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


def keyDown(k, d):
    global player
    if k == key.RIGHT:
        player.moving = 1
    if k == key.LEFT:
        player.moving = -1

def keyUp(k, d):
    global player
    if k == key.RIGHT or k == key.LEFT:
        player.moving = False

def gameInit():
    background = makeSprite('nightSky0.png')
    global mainDrawnings
    global player
    mainDrawnings += [background]
    player = cat = Player()

    addState('mainRun')
    changeState('mainRun')
    setEventHandler('mainRun', 'draw', drawMain)
    setEventHandler('mainRun', 'keyPress', keyDown)
    setEventHandler('mainRun', 'keyRelease', keyUp)
    setEventHandler('mainRun', 'mechanic', player.moveSide)

    a = makeAnimObj('../pong/block6anim/pearl', 100, 200, 8, 0.1)
    mainDrawnings += [a]

    mp = list()
    for x in range(140):
        mp += [(x,2)]
    m = Tiled('ground1.png', mp)
    mainDrawnings += [m]

    mp = list()
    for x in range(30):
        mp += [(x,3)]
    #m = Tiled('sky0.png', mp)
    #mainDrawnings += [m]

    #cat = makeSprite('cat0.png', 64,64)


    mainDrawnings += [cat]




def run():

    pygletRun()
