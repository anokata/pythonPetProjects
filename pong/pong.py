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
  currentLevel = None
  blockWindowTopStart = 500
  blockWindowLeft = 500
  
  def __init__(self, width, height):
    self.blockWindowTopStart = height
    self.blockWindowLeft = width
    self.blocksAnims = dict()
    for (b, (imgBaseName, framesCount)) in self.blockImgNames.items():
      frames = list()
      for i in range(1, framesCount+1):
        img = pyglet.image.load(imgBaseName + str(i) + '.png')
        center_image(img)
        frames += [pyglet.image.AnimationFrame(img, 0.2)]
      anim = pyglet.image.Animation(frames)
      self.blocksAnims[b] = anim
    self.levels = list()
    for name in self.levelsNames:
      lev = Level(name, self.blockWindowLeft, self.blockWindowTopStart)
      self.levels += [lev]
      lev.loadBlocks(self)
      #lev.printLevel()
    self.currentLevel = self.levels[0]

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
  
class BaseBlock(HasSprite):
  btype = None
  
  def __init__(self, m, x, y, btype):
    self.sprite = pyglet.sprite.Sprite(m.getBlockAnim(btype), x=x, y=y)
    self.btype = btype
    
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
  playerWins = 0
  botWins = 0
  ball = None
  player = None
  bot = None
  
  window = None
  score_label = None
  infoLabel = None
  labels = []
  scoreText1 = "PlayerName Exp: "
  scoreText2 = "Bot: "
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
  blockAreaLeft = 0
  
  background = None
  foreground = None
  world = None
  
  def __init__(self):
    random.seed()
    self.drawable = list()
    self.stepping = list()
    
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
    
    wallimg = pyglet.image.load('wall.png')
    self.wall = pyglet.sprite.Sprite(wallimg, self.gameWindowWidth // 2, - wallimg.height + self.gameWindowHeigth - 40)
        
    self.score_label = pyglet.text.Label(text=self.getScore(), x=self.window.width - 90, y=self.gameWindowHeigth - 40, anchor_x='left', anchor_y='center')
    self.infoLabel = pyglet.text.Label(text=self.getInfo(), x=self.window.width - 90, y=self.gameWindowHeigth - 20)

    self.addToDrawable(self.infoLabel)
    self.addToDrawable(self.score_label)
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
    
    self.world = Map(self.blockAreaLeft, self.gameWindowHeigth - 25)
    self.addToLevelDrawable(self.world.getDrawables())
    
    self.stateToBallCapt()
    
    @window.event
    def on_draw():
      window.clear()
      for x in self.drawable:
        x.draw()
      for x in self.levelDrawable:
        x.draw()
      #self.wall.draw()
      self.ball.sprite.draw()
      self.player.sprite.draw()
      self.bot.sprite.draw()
      for x in self.labels:
        x.draw()
      
    @window.event
    def on_key_press(symbol, mod):
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

    @window.event
    def on_key_release(symbol, mod):
      if symbol == key.UP or symbol == key.DOWN or symbol == key.LEFT or symbol == key.RIGHT:
        g.player.isMove = False
    
  def addToLevelDrawable(self, x):
    self.levelDrawable = x
  
  def addParticles(self, x):
    self.addToDrawable(x)
    self.addToStepping(x)
    
  def addToDrawable(self, x):
    self.drawable += [x]
  def addToStepping(self, x):
    self.stepping += [x]

  def stateSet(self, s):
    self.state = s
  
  def stateToRun(self):
    if self.state == self.stateBallCapt:
      self.ball.drop(self.player.speed * 10 * self.player.isMove)
    self.stateSet(self.stateRun)
    
  def stateToBallCapt(self):
    self.ball.x = self.player.x + self.player.width
    self.stateSet(self.stateBallCapt)
  
  def stateHandle(self, dt):
    d = {
      self.stateBallCapt: self.mechanicCapt,
      self.stateRun: self.mechanicRun
    }
    fun = d[self.state]
    fun(dt)
    
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
    
  def blockCollision(self):
    if self.ball.x + self.ball.speed  > self.blockAreaLeft:
      for b in self.world.currentLevel.blocks:
        if self.ball.distanceFrom(b) < Level.blockWidth: #blockRadius
          self.ball.stepBack()
          self.numberGenerator.makeNumber(self.player.STR, b.x, b.y, 30)
          self.ball.dx = - (self.ball.dx)
          # up down collision?
          if self.ball.top < b.y or self.ball.bottom > b.y:
            self.ball.dy = -(self.ball.dy)
    
  def ballCaptureStep(self):
    self.ball.y = self.player.y
    
  def isCollision(self):
    colis = self.collisoinsDetect()
    if colis:
      if abs(self.ball.dx) < self.ball.maxspeed:
        self.ball.dx = abs(self.ball.dx) + self.difficult
      if type(colis) == Player:
        self.ball.dx = abs(self.ball.dx)
       # self.redParticles.restart(self.ball.left, colis.y)
        self.whiteParticles.restart(self.ball.left, colis.y)
      else:
        self.ball.dx = - abs(self.ball.dx)
        #self.redParticles.restart(500,300)
      
      if colis.isMove:
        self.ball.dy += colis.isMove * colis.speed * 2
    
  def getScore(self):
    return 'EXP:' + ' ' + str(self.playerWins)
  
  def updateScore(self):
    self.score_label.text = self.getScore()
  
  def updateLabels(self):
    self.infoLabel.text = self.getInfo()
    
  def getInfo(self):
    return "SPD: " + str(abs(self.ball.dx)) + '  '
    
  def isBallOut(self):
    if self.ball.x < self.gameWindowUp:
      #self.ball.ballReturn(1)
      return -1
    if self.ball.x > self.gameWindowWidth + self.enemyDeep:
      #self.ball.ballReturn(-1)
      return 1
    return 0
    
  def checkBallOut(self):
    isout = self.isBallOut()
    if 1 == isout:
      self.playerWins += random.randint(1,100)
      self.updateScore()
      self.blueParticles.restart(100,200)
      self.numberGenerator.makeNumber(self.playerWins, 50, 10, 30)
      #self.stateToBallCapt()
      self.ball.bounce()
    if -1 == isout:
      self.lose()
  
  def lose(self):
    self.botWins += 1
    self.updateScore()
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


class direction:
  up = 1
  down = -1

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
    
  
  def step(self):
    if self.isMove == direction.up:
      if (self.y ) < self.yMax:
        self.y += self.speed
    if self.isMove == direction.down:
      if (self.y ) > self.yMin:
        self.y -= self.speed
    
    self.top = self.y + self.height // 2
    self.bottom = self.y - self.height // 2

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
    self.dy = dy
    self.dx = self.speed


if __name__ == '__main__':
  g = Game()
  pyglet.app.run()
