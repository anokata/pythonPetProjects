import pyglet
from pyglet.window import key
import random
import math
#bug: 0
def debugDecor(fn):
  def wrap(*args): 
    print(args)
    return fn(*args)
  return wrap

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

def objDistance(s1, s2):
  return distance(s1.x, s1.y, s2.x, s2.y)

def distance(x, y, a, b):
  from math import sqrt
  return sqrt((x-a)*(x-a) + (y-b)*(y-b))

def geomRange(start, count, coeff):
  x = start
  c = 0
  while c < count:
    x = x * coeff
    c += 1
    yield int(x)

class BlockType:
  emerald = 1
  ruby = 0
  pearl = 2

class HasSprite():
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
  
  def distanceFrom(self, obj):
    return distance(self.x, self.y, obj.x, obj.y)
#sprite.scale:float
#[(blockType, x, y),...] in file: blockType x y
  # map = dict( (x, y) : lev)
class Map:
  blocksAnims = {}
  blockImgNames = {BlockType.ruby : ('block1anim/ruby', 7),
           BlockType.pearl: ('block2anim/block2F', 7),
           BlockType.emerald: ('block3anim/emerald0', 7)}
  levelsNames = ['lv0.lev']
  levels = []
  levelsCoords = []
  levelsDone = []
  currentLevel = None
  blockWindowTopStart = 500
  blockWindowLeft = 500
  background = None
  
  def __init__(self, width, height, mapname):
    self.blockWindowTopStart = height
    self.blockWindowLeft = width
    self.blocksAnims = dict()
    self.levels = list()
    self.levelsCoords = list()
    self.levelsDone = list() # Список пройденных уровней ! загружать
    self.loadMap(mapname)
    self.loadBlockImages()
    self.loadLevels()
    
  def loadMap(self, mapname):
    with open(mapname, 'rt') as fin:
      self.background = fin.readline()[:-1] #without \n
      levelDir = fin.readline()[:-1]
      for l in fin:
        l = l.split()
        self.levelsCoords += [(int(l[0]), int(l[1]))]
      print(self.background, levelDir, self.levelsCoords)
    #load levels list
    self.levelsNames = list()
    from os import listdir
    from os.path import isfile, join
    self.levelsNames = [levelDir + f for f in listdir(levelDir) if isfile(join(levelDir, f))]
    self.levelsNames = list(filter(lambda x: x.find('.lev') > -1, self.levelsNames))
    self.levelsNames.sort()
    #load bg
    self.background = pyglet.sprite.Sprite(pyglet.image.load(self.background))
    
  def loadLevels(self):
    for name in self.levelsNames:
      lev = Level(name, self.blockWindowLeft, self.blockWindowTopStart)
      self.levels += [lev]
      lev.loadBlocks(self)
    self.currentLevel = self.levels[0]
  
  def loadBlockImages(self):
    for (b, (imgBaseName, framesCount)) in self.blockImgNames.items():
      frames = list()
      for i in range(1, framesCount+1):
        img = pyglet.image.load(imgBaseName + str(i) + '.png')
        center_image(img)
        frames += [pyglet.image.AnimationFrame(img, 0.2)]
      anim = pyglet.image.Animation(frames)
      self.blocksAnims[b] = anim
    self.levels = list()

  def getBlockAnim(self, btype):
    return self.blocksAnims[btype]
  
  def getDrawables(self):
    return self.currentLevel.getDrawables()

class Level:
  blocksGrid = [] #(btype, gridx, gridy)
  blocks= []
  name = 'lv0.lev'
  blockWidth = 32
  blockHeight = 32
  blockLeft = 500
  blockTop = 5
  blockWindowTopStart = 500
  
  def __init__(self, name, left, top):
    self.blocksGrid = list()
    self.blocks = list()
    self.readLevel(name)
    self.blockLeft = left# - 2.5 * self.blockWidth
    self.blockWindowTopStart = top
    
  def addBlock(self, btype, x, y):
    self.blocksGrid += [(btype, x, y)]
  
  def loadBlocks(self, m):
    for (b, x, y) in self.blocksGrid:
      # тут преобразуем координаты в реальные
      x = x * self.blockWidth + self.blockLeft
      y = self.blockWindowTopStart - y * self.blockHeight + self.blockTop
      self.blocks += [BaseBlock(m, x, y, b)]
    
  def writeLevel(self):
    with open(self.name, 'wt') as fout:
      for (b, x, y) in self.blocks:
        fout.write(str(b) + ' ' + str(x) + ' ' + str(y) + '\n')
  
  def readLevel(self, name):
    with open(name, 'rt') as fin:
      for line in fin:
        line = line.split()
        self.addBlock(int(line[0]), int(line[1]), int(line[2]))  # тут координаты сетки  

  def printLevel(self):
    for (b, x, y) in self.blocksGrid:
      print(b, x, y)
  
  def getDrawables(self):
    return self.blocks
    
  def blockCapture(self, block):
    self.blocks = list(filter(lambda x: x != block, self.blocks))
  
class BaseBlock(HasSprite):
  btype = None
  Health = 0
  price = 0
  
  def __init__(self, m, x, y, btype):
    self.sprite = pyglet.sprite.Sprite(m.getBlockAnim(btype), x=x, y=y)
    self.btype = btype
    # stats(Heath, price)
    baseStats = {BlockType.emerald: (2, 30), 
      BlockType.ruby: (5, 150),
      BlockType.pearl: (1, 10)}
    (self.Health, self.price) = baseStats[btype]
    
  def capture(self):
    self.sprite.visible = False
  
  def draw(self):
    self.sprite.draw()
    
# make fabric?
class ImgNumber:
  
  class DrawableNumber:
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
      self.images += [pyglet.image.load(str(i) + '.png')]
  
  def draw(self):
    for i in self.numbers:
      i.draw()
  
  def step(self):
    self.numbers[:] = filter(lambda x: x.step() != 0, self.numbers)
  
  def makeNumber(self, n, x, y, lifeTime=-1): 
    n = str(n)
    number = list()
    for i in n:
      num = pyglet.sprite.Sprite(self.images[int(i)])
      num.y = y
      num.x = x
      x += num.width
      number += [num]
    self.numbers += [self.DrawableNumber(number, lifeTime)]
      
class Particles:
  sprites = []
  speed = 2
  lifeTime = 100
  initLifeTime = 0
  speedDown = 0
  
  def __init__(self, img, n, lifeTime, x=0, y=0, speed=2, speedDown=0):
    self.sprites = list()  # Необходимо все неэлемнтарные типы так создавать
    self.lifeTime = 0
    self.initLifeTime = lifeTime
    self.speed = speed
    self.speedDown = 1 if speedDown == 0 else (100 - speedDown)/100
    for i in range(n):
      s = pyglet.sprite.Sprite(img, x=x,y=y)
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

#singleton
class Game:
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
    
    self.window = pyglet.window.Window(width=800, height = 550)
    window = self.window
    self.gameWindowHeigth = window.height - 20
    self.gameWindowWidth = window.width - 200
    self.blockAreaLeft = self.gameWindowWidth - 2.5 * Level.blockWidth
    
    self.background = pyglet.sprite.Sprite(pyglet.image.load('board1.png'), x=self.gameWindowLeft)
    self.addToDrawable(self.background)
    self.foreground = pyglet.sprite.Sprite(pyglet.image.load('foreground.png'))
    self.addToDrawable(self.foreground)
    
    self.ball = Ball(pyglet.image.load('ball4.png'), self.gameWindowWidth, self.gameWindowHeigth, self.gameWindowLeft)
    
    self.player = Player(pyglet.image.load('player.png'), self.gameWindowLeft, self.gameWindowLeft , self.gameWindowHeigth - self.gameWindowLeft)
    self.bot = Bot(pyglet.image.load('player.png'), self.gameWindowWidth - Level.blockWidth * 3, self.gameWindowLeft, self.gameWindowHeigth - self.gameWindowLeft)
    
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
    self.addToLevelDrawable(self.mmap.getDrawables())
    
    self.stateToBallCapt()

    self.addLabel(self.player.getStatText , 'Health: 0', PlayerStatIndex.Health)
    self.addLabel(self.player.getStatText , '', PlayerStatIndex.Str)
    self.addLabel(self.player.getStatText , 'Exp: 0', PlayerStatIndex.Lv)
    self.addLabel(self.player.getStatText , 'Lv: 0', PlayerStatIndex.Exp)
    self.addLabel(self.player.getStatText , '', PlayerStatIndex.statPoints)
    self.addLabel(self.player.getStatText , '', PlayerStatIndex.Speed)
    self.updateLabels()
    
    @window.event
    def on_draw():
      self.stateHandleDraw()
    @window.event
    def on_key_press(symbol, mod):
      self.stateHandleKeyPress(symbol, mod)
    @window.event
    def on_key_release(symbol, mod):
      self.stateHandleKeyRelease(symbol, mod)
  
  def addLabel(self, updateFun, initText, updateParam):
    self.labels += [pyglet.text.Label(text=initText, x=self.window.width - 90, y=self.gameWindowHeigth - 20 * len(self.labels) - 20)]
    self.labelsFun += [(updateFun, updateParam)]
    
  def addToLevelDrawable(self, x):
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
    """ . """
    if self.state == self.stateBallCapt:
      self.ball.drop(self.player.speed * 10 * self.player.isMove)
    self.stateSet(self.stateRun)
    
  def stateToBallCapt(self):
    self.ball.x = self.player.x + self.player.width
    self.stateSet(self.stateBallCapt)
  
  def stateToMap(self):
    
    self.stateSet(self.stateMap)
  #Обработчики механики от состояния
  def stateHandle(self, dt):
    d = {
      self.stateBallCapt: self.mechanicCapt,
      self.stateRun: self.mechanicRun,
      self.stateMap: self.mechanicMap
    }
    fun = d[self.state]
    fun(dt)
  #Обработчики отрисовки от состояния
  def stateHandleDraw(self):
    d = {
      self.stateBallCapt: self.playDraw,
      self.stateRun: self.playDraw,
      self.stateMap: self.mapDraw
    }
    fun = d[self.state]
    fun()
  #Обработчики нажатия кнопки в зависимости от состояния
  def stateHandleKeyPress(self, symbol, mod):
    d = {
      self.stateBallCapt: self.playKeyPress,
      self.stateRun: self.playKeyPress,
      self.stateMap: self.mapKeyPress
    }
    fun = d[self.state]
    fun(symbol, mod)
  
  def stateHandleKeyRelease(self, symbol, mod):
    d = {
      self.stateBallCapt: self.playKeyRelease,
      self.stateRun: self.playKeyRelease,
      self.stateMap: self.mapKeyRelease
    }
    fun = d[self.state]
    fun(symbol, mod)
    
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
    self.mmap.background.draw()
    
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
      self.stateToMap()

  def playKeyRelease(self, symbol, mod):
    if symbol == key.UP or symbol == key.DOWN or symbol == key.LEFT or symbol == key.RIGHT:
      g.player.isMove = False

  # Mechanic
  def mechanicMap(self, dt):
    pass
  
  def mechanicStd(self, dt):
    self.updateLabels()
    self.blueParticles.step()
    self.redParticles.step()
    for x in self.stepping:
      x.step()
    
  def mechanicCapt(self, dt):
    self.mechanicStd(dt)
    self.player.step()
    self.ballCaptureStep()

  def mechanicRun(self, dt):
    self.ball.step(dt)
    self.player.step()
    self.bot.randStep(self.ball.y, self.ball.x > self.gameWindowWidth // 2)
    self.checkBallOut()
    self.isCollision()
    self.blockCollision()
    self.mechanicStd(dt)
    
  # Physics
  def blockCollision(self):
    if self.ball.x + self.ball.speed  > self.blockAreaLeft:
      for b in self.mmap.currentLevel.blocks:
        if self.ball.distanceFrom(b) < Level.blockWidth: #blockRadius
          self.ball.stepBack()
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
  
  def isBallOut(self):
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
    self.updateLabels()
    self.redParticles.restart(self.ball.x, self.ball.y)
    self.stateToBallCapt()
  
  def collisoinsDetect(self):
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
    

class direction:
  up = 1
  down = -1

class PlayerStatIndex:
  Speed = 1
  Str = 2
  Health = 3
  Exp = 4
  Lv = 5
  statPoints = 6

class Player(HasSprite):
  isMove = False
  yMin = 0
  yMax = 0
  top = 0
  bottom = 0
  left = 0
  right = 0
  #Stats:
  speed = 20
  STR = 1
  Health = 10
  Exp = 0
  Lv = 0
  statPoints = 0
  
  LevelExp = {
    1: 100, 2: 300, 3: 1000 # сделать генератор?
  }
  
  
  #@debugDecor
  def __init__(self, img, x, yMin, yMax):
    center_image(img)
    x = x + img.width//2
    yMin = yMin + img.height // 2
    yMax -= img.height // 2
    self.sprite = pyglet.sprite.Sprite(img, x = x, y = yMin)
    self.yMin = yMin
    self.yMax = yMax
    self.left = x 
    self.right = x 
    self.LevelExp = dict(enumerate(geomRange(10, 51, 1.2)))
    #print(self.LevelExp)
  
  def step(self):
    if self.isMove == direction.up:
      if (self.y ) < self.yMax:
        self.y += self.speed
    if self.isMove == direction.down:
      if (self.y ) > self.yMin:
        self.y -= self.speed
    
    self.top = self.y + self.height // 2
    self.bottom = self.y - self.height // 2
    
  def capture(self, block):
    self.expGain(block.price)
    block.capture()
  
  def expGain(self, n):
    # смотрим сколько до след уровня
    tonext = self.LevelExp[self.Lv +1] - self.Exp
    if tonext > n: # если недостаточно то просто добавляем и выходим
      self.Exp += n
      return
    self.Exp += tonext # иначе добавляем сколько надо а остаток добавляем рекурсивно
    self.Lv += 1
    self.statPoints += 1
    self.expGain(n - tonext)
    
  def getStatText(self, stat):
    stats = {
      PlayerStatIndex.Exp: (self.Exp, 'Exp: '),
      PlayerStatIndex.Lv: (self.Lv, 'Lv '),
      PlayerStatIndex.Speed: (self.speed, 'Spd '),
      PlayerStatIndex.Str: (self.STR, 'Str '),
      PlayerStatIndex.statPoints: (self.statPoints, 'SP: '),
      PlayerStatIndex.Health: (self.Health, 'HP= ')
    }
    val, name = stats[stat]
    return name + str(val)

class Bot(Player):
  i = 0
  maxi = 4
  accur = 20
  #@debugDecor
  def __init__(self, img, x, yMin, yMax):
    x = x - img.width
    super().__init__(img, x, yMin, yMax)
    self.left = x + img.width
    self.right = x
    self.speed = 1 # difficult
  
  def randStep(self, ballY, inBotArea):
    self.i += 1
    if self.i > self.maxi:
      self.i = 0
      if inBotArea:
        if abs(ballY - self.y) > self.accur:
          if ballY > self.y:
            self.isMove = direction.up
          else:
            self.isMove = direction.down
        else:
          self.isMove = False
      else:
        #self.isMove = random.choice([direction.up, direction.down, False])
        self.isMove = False
    self.step()

class Ball(HasSprite):
  dx = 200
  dy = 200
  speed = 400
  collided = []
  wh = 0
  yMax = 0
  xMax = 0
  yMin = 0
  midX = 0
  midY = 0
  left = 0
  right = 0
  top = 0
  bottom = 0
  maxspeed = 1000
  
  def __init__(self, img, width, height, marginBottom):
    self.collided = list()
    center_image(img)
    self.midX = width // 2
    self.midY = height // 2
    self.sprite = pyglet.sprite.Sprite(img, x = width // 2, y = height // 2)
    self.wh = img.width // 2
    self.yMax = height - self.wh
    self.xMax = width - self.wh
    self.yMin = img.height // 2 + marginBottom 

  def step(self, dt):
    self.sprite.rotation += 100 * dt
    self.x += self.dx * dt
    self.y += self.dy * dt
    self.lastdt = dt
    self.recalcCoords()
    self.collisoins()
  
  def recalcCoords(self):
    self.right = self.x + self.width // 2
    self.left = self.x - self.width // 2
    self.top = self.y + self.height // 2
    self.bottom = self.y - self.height // 2
  
  def stepBack(self):
    self.x -= self.dx * self.lastdt
    self.y -= self.dy * self.lastdt
    self.recalcCoords()
  
  def bounce(self):
    self.stepBack()
    self.dx = -self.dx

  def collisoins(self):
    if self.y < self.yMin:
      self.dy = - self.dy
    if self.y > self.yMax:
      self.dy = - self.dy
  
  def ballReturn(self, direct):
    self.x = self.midX
    self.y = self.midY
    self.dx = self.speed * direct
    self.dy = 200
  
  def drop(self, dy):
    self.dy = dy if dy != 0 else random.randint(-50,50)
    self.dx = self.speed


if __name__ == '__main__':
  g = Game()
  pyglet.app.run()
