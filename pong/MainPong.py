""" Main module. """
import pyglet
from pyglet.window import key
import random
import math
#TODO: Выделить модули для использования в др проекте.
#ctrlAlt-F F3 F4 CA-t A-o A-w
import sys
sys.path += ["modules"]
from util import *
from gameTypes import *
from players import *
from pygletUtil import *
from Mmap import Map
from level import Level
from imgNumber import ImgNumber
from particles import Particles
from block import BaseBlock
#sprite.scale:float
#Форамт файла Уровня: [(blockType, x, y),...] in file: blockType x y
#Формат файла карты map = БГ, Папка уровней, dict( (x, y) : lev)

#singleton
class Game:
    """ Главный класс игры. """
    ball = None
    player = None
    bot = None

    window = None
    labels = []
    labelsFun = []
    difficult = 100

    gameWindowLeft = 20
    gameWindowUp = 20
    gameWindowWidth = 0
    gameWindowHeigth = 0
    enemyDeep = 80

    wall = None
    redParticles = None
    blueParticles = None
    whiteParticles = None
    drawable = []
    stepping = []
    levelDrawable = []

    state = 1
    stateRun = 1
    stateBallCapt = 2
    stateMap = 3
    stateWin = 4
    blockAreaLeft = 0

    background = None
    foreground = None
    mmap = None
    mmap = None

    def __init__(self):
        random.seed()
        self.drawable = list()
        self.stepping = list()
        self.labels = list()
        self.labelsFun = list()

        self.window = pyglet.window.Window(width=800, height=550)
        window = self.window
        self.gameWindowHeigth = window.height - 20
        self.gameWindowWidth = window.width - 200
        self.blockAreaLeft = self.gameWindowWidth - 2.5 * Level.blockWidth

        self.background = Sprite(pyglet.image.load('board2.png'), x=self.gameWindowLeft)
        self.addToDrawable(self.background)
        self.foreground = Sprite(pyglet.image.load('foreground.png'))
        self.addToDrawable(self.foreground)

        self.ball = Ball(pyglet.image.load('ball4.png'), self.gameWindowWidth,\
                         self.gameWindowHeigth, self.gameWindowLeft)

        self.player = Player(pyglet.image.load('player.png'), self.gameWindowLeft, \
                             self.gameWindowLeft , self.gameWindowHeigth - self.gameWindowLeft)
        self.bot = Bot(pyglet.image.load('player.png'), \
                       self.gameWindowWidth - Level.blockWidth * 3,\
                       self.gameWindowLeft, self.gameWindowHeigth - self.gameWindowLeft)

        pyglet.gl.glClearColor(0.7,0.5,0.3, 1)
        #window.push_handlers(pyglet.window.event.WindowEventLogger())
        pyglet.clock.schedule_interval(self.stateHandle, 1.0/30)

        self.redParticles = Particles(pyglet.image.load('redstar18.png'), 15, 14, 300, 100)
        self.whiteParticles = Particles(pyglet.image.load('whitestar12.png'), 15, 10, speed = 1)
        self.blueParticles = Particles(pyglet.image.load('bluestar24.png'), 15, 30, 300, 100, speedDown=5)
        self.addParticles(self.redParticles)
        self.addParticles(self.blueParticles)
        self.addParticles(self.whiteParticles)

        self.numberGenerator = ImgNumber()
        self.addToDrawable(self.numberGenerator)
        self.addToStepping(self.numberGenerator)

        self.mmap = Map(self.blockAreaLeft, self.gameWindowHeigth - 25, 'map1.map')
        self.setLevelDrawable(self.mmap.getDrawables())

        self.stateToBallCapt()

        self.addLabel(self.player.getStatText , 'Health: 0', PlayerStatIndex.Health)
        self.addLabel(self.player.getStatText , '', PlayerStatIndex.Str)
        self.addLabel(self.player.getStatText , 'Exp: 0', PlayerStatIndex.Lv)
        self.addLabel(self.player.getStatText , 'Lv: 0', PlayerStatIndex.Exp)
        self.addLabel(self.player.getStatText , '', PlayerStatIndex.statPoints)
        self.addLabel(self.player.getStatText , '', PlayerStatIndex.Speed)
        self.updateLabels()
        self.winLabel = self.makeLabel('WIN!', self.gameWindowWidth//2, self.gameWindowHeigth//2, 40)
        self.failLabel = self.makeLabel('FAIL!', self.gameWindowWidth//2, self.gameWindowHeigth//2, 40)

        @window.event
        def on_draw():
            self.stateHandleDraw()
        @window.event
        def on_key_press(symbol, mod):
            self.stateHandleKeyPress(symbol, mod)
        @window.event
        def on_key_release(symbol, mod):
            self.stateHandleKeyRelease(symbol, mod)
        @window.event
        def on_mouse_press(x, y, button, mod):
            self.stateHanderMousePress(x, y, button, mod)

    def makeLabel(self, text, x, y, size = 18):
        return pyglet.text.Label(text=text, x=x, y=y, font_size=size)

    def addLabel(self, updateFun, initText, updateParam):
        self.labels += [pyglet.text.Label(text=initText, x=self.window.width - 90, y=self.gameWindowHeigth - 20 * len(self.labels) - 20)]
        self.labelsFun += [(updateFun, updateParam)]

    def setLevelDrawable(self, x):
        """ Установка отрисовывающегося на уровне. """
        self.levelDrawable = x

    def addParticles(self, x):
        self.addToDrawable(x)
        self.addToStepping(x)

    def addToDrawable(self, x):
        self.drawable += [x]
    def addToStepping(self, x):
        self.stepping += [x]
    # States конечный автомат состояний
    def stateSet(self, s):
        """ Установка состояния. """
        self.state = s

    def stateToRun(self):
        """ Переход в состояние игры полёта мяча. """
        if self.state == self.stateBallCapt:
            self.ball.drop(self.player.speed * 10 * self.player.isMove)
        self.stateSet(self.stateRun)

    def stateToBallCapt(self):
        """ К захвату мяча. """
        self.ball.x = self.player.x + self.player.width
        self.stateSet(self.stateBallCapt)

    def stateToMap(self, dt):
        """ Переход на карту. """
        cap = self.mmap.levelsCaps[self.mmap.levels.index(self.mmap.currentLevel)]
        self.ball.x = cap.x
        self.ball.y = cap.y
        self.stateSet(self.stateMap)

    def stateToWin(self):
        self.stateIntervalToMap()
        self.numberGenerator.stopAll()
        self.bot.reinit()
        self.player.reinit()
        self.stateSet(self.stateWin)

    def stateIntervalToMap(self):
        #from pyglet import clock
        pyglet.clock.schedule_once(self.stateToMap, 3)

    #Обработчики механики от состояния
    def stateHandle(self, dt):
        d = {
            self.stateBallCapt: self.mechanicCapt,
            self.stateRun: self.mechanicRun,
            self.stateMap: self.mechanicMap,
            self.stateWin: False
        }
        fun = d[self.state]
        if fun:
            fun(dt)
    #Обработчики отрисовки от состояния
    def stateHandleDraw(self):
        d = {
            self.stateBallCapt: self.playDraw,
            self.stateRun: self.playDraw,
            self.stateMap: self.mapDraw,
            self.stateWin: self.winDraw
        }
        fun = d[self.state]
        fun()
    #Обработчики нажатия кнопки в зависимости от состояния
    def stateHandleKeyPress(self, symbol, mod):
        d = {
            self.stateBallCapt: self.playKeyPress,
            self.stateRun: self.playKeyPress,
            self.stateMap: self.mapKeyPress,
            self.stateWin: False
        }
        fun = d[self.state]
        if fun:
            fun(symbol, mod)

    def stateHandleKeyRelease(self, symbol, mod):
        d = {
            self.stateBallCapt: self.playKeyRelease,
            self.stateRun: self.playKeyRelease,
            self.stateMap: self.mapKeyRelease,
            self.stateWin: False
        }
        fun = d[self.state]
        if fun:
            fun(symbol, mod)

    def stateHanderMousePress(self, x, y, button, mod):
        d = {
            self.stateBallCapt: False,
            self.stateRun: False,
            self.stateMap: self.mapMousePress,
            self.stateWin: False
        }
        fun = d[self.state]
        if fun:
            fun(x, y, button, mod)
    # Draw
    def winDraw(self):
        self.playDraw()
        self.winLabel.draw()

    def playDraw(self):
        self.window.clear()
        for x in self.drawable:
            x.draw()
        for x in self.levelDrawable:
            x.draw()
        self.ball.sprite.draw()
        self.player.sprite.draw()
        self.bot.sprite.draw()
        for x in self.labels:
            x.draw()

    def mapDraw(self):
        self.window.clear()
        self.mmap.draw()
        self.ball.draw()

    # Key events
    def mapKeyPress(self, symbol, mod):
        if symbol == key.ENTER:
            self.stateToBallCapt()

    def mapKeyRelease(self, symbol, mod):
        pass

    def playKeyPress(self, symbol, mod):
        if symbol == key.RIGHT:
            g.player.isMove = direction.down
        if symbol == key.LEFT:
            g.player.isMove = direction.up
        if symbol == key.UP:
            g.player.isMove = direction.up
        if symbol == key.DOWN:
            g.player.isMove = direction.down
        if symbol == key.SPACE:
            self.stateToRun()
        if symbol == key._1:
            self.stateToMap(0)

    def playKeyRelease(self, symbol, mod):
        if symbol == key.UP or symbol == key.DOWN or symbol == key.LEFT or symbol == key.RIGHT:
            g.player.isMove = False

    def mapMousePress(self, x, y, b, m):
        """ Проверяем попал ли игрок на иконку уровня.
                И если да, то загружаем и запускаем его.
        """
        print(x, y)
        for (a, b) in self.mmap.levelsCoords:
            if distance(x, y, a, b) < self.mmap.capRadius:
                self.mmap.loadLevel(self.mmap.levelsCoords.index((a,b)))
                self.stateToBallCapt()

                self.setLevelDrawable(self.mmap.getDrawables())
                return

    # Mechanic
    def mechanicMap(self, dt):
        pass

    def mechanicStd(self, dt):
        """ Общая механика игры. """
        self.updateLabels()
        self.blueParticles.step()
        self.redParticles.step()
        for x in self.stepping:
            x.step()
        if self.mmap.currentLevel.isComplete():
            self.stateToWin()

    def mechanicCapt(self, dt):
        """ Механика при захваченном мяче. """
        self.mechanicStd(dt)
        self.player.step()
        self.ballCaptureStep()

    def mechanicRun(self, dt):
        """ Механика при летящем мяче. """
        self.ball.step(dt)
        self.player.step()
        self.bot.randStep(self.ball.y, self.ball.x > self.gameWindowWidth // 2)
        self.checkBallOut()
        self.isCollision()
        self.blockCollision()
        self.mechanicStd(dt)

    # Physics
    def blockCollision(self):
        """ Пересечения с блоками мяча. """
        if self.ball.x + self.ball.speed    > self.blockAreaLeft:
            for b in self.mmap.currentLevel.blocks:
                if self.ball.distanceFrom(b) < Level.blockWidth: #blockRadius
                    self.ball.stepBack(b.x, b.y)
                    self.numberGenerator.makeNumber(self.player.STR, b.x, b.y, 30)
                    self.ball.dx = - (self.ball.dx)
                    # up down collision?
                    if self.ball.top < b.y or self.ball.bottom > b.y:
                        self.ball.dy = -(self.ball.dy)
                    # strike block
                    b.Health -= self.player.STR
                    if b.Health <= 0:
                        self.player.capture(b)
                        self.numberGenerator.makeNumber(b.price, b.x, b.y, 30)
                        self.mmap.currentLevel.blockCapture(b)
                        self.updateLabels()

    def ballCaptureStep(self):
        self.ball.y = self.player.y

    def isCollision(self):
        """ Обработка пересечения игроков с мячом. """
        colis = self.collisoinsDetect()
        if colis:
            if abs(self.ball.dx) < self.ball.maxspeed:
                self.ball.dx = abs(self.ball.dx) + self.difficult
            if type(colis) == Player:
                self.ball.dx = abs(self.ball.dx)
                self.whiteParticles.restart(self.ball.left, colis.y)
            else:
                self.ball.dx = - abs(self.ball.dx)

            if colis.isMove:
                self.ball.dy += colis.isMove * colis.speed * 2
    # 2down Refactor
    def isBallOut(self):
        """ Проверка на вылет из поля. """
        if self.ball.x < self.gameWindowUp:
            return -1
        if self.ball.x > self.gameWindowWidth + self.enemyDeep:
            return 1
        return 0

    def checkBallOut(self):
        isout = self.isBallOut()
        if 1 == isout:
            self.updateLabels()
            self.ball.bounce()
        if -1 == isout:
            self.lose()

    def lose(self):
        """ Проигрыш при неотбивании. """
        self.updateLabels()
        self.redParticles.restart(self.ball.x, self.ball.y)
        self.stateToBallCapt()
        self.player.Health -= 2
        if self.player.Health < 1:
            self.player.lose()
            self.stateIntervalToMap()

    def collisoinsDetect(self):
        """ Проверка на пересечения игроков с мячом. """
        faces = [self.player, self.bot]
        for x in faces:
            hei = max(self.ball.top, x.top) - min(self.ball.bottom, x.bottom)
            allheight = self.ball.height + x.height
            wid = max(self.ball.left, x.left) - min(self.ball.right, x.right)
            allwid = self.ball.width + 0

            if hei <= allheight and wid <= allwid:
                return x
        return False

    def updateLabels(self):
        for (fun, param), lab in zip(self.labelsFun, self.labels):
            lab.text = fun(param)


if __name__ == '__main__':
    g = Game()
    pyglet.app.run()
