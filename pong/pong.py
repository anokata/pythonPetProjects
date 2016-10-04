import pyglet
from pyglet.window import key
import random
import math
#bug: старые числа показываются
def debugDecor(fn):
  def wrap(*args): 
    print(args)
    return fn(*args)
  return wrap

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

def objDistance(s1, s2):
  return distance(s1.sprite.x, s1.sprite.y, s2.sprite.x, s2.sprite.y)

def distance(x, y, a, b):
  from math import sqrt
  return sqrt((x-a)*(x-a) + (y-b)*(y-b))

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
  
  wall = None
  redParticles = None
  blueParticles = None
  whiteParticles = None
  drawable = []
  stepping = []
  
  state = 1
  stateRun = 1
  stateBallCapt = 2
  
  background = None
  foreground = None
  
  def __init__(self):
    random.seed()
    self.drawable = list()
    self.stepping = list()
    
    self.window = pyglet.window.Window(width=800, height = 550)
    window = self.window
    self.gameWindowHeigth = window.height - 20
    self.gameWindowWidth = window.width - 100
    
    self.background = pyglet.sprite.Sprite(pyglet.image.load('board1.png'), x=self.gameWindowLeft)
    self.addToDrawable(self.background)
    self.foreground = pyglet.sprite.Sprite(pyglet.image.load('foreground.png'))
    self.addToDrawable(self.foreground)
    
    self.ball = Ball(pyglet.image.load('ball3.png'), self.gameWindowWidth, self.gameWindowHeigth, self.gameWindowLeft)
    
    self.player = Player(pyglet.image.load('player.png'), self.gameWindowLeft, self.gameWindowLeft , self.gameWindowHeigth - self.gameWindowLeft)
    self.bot = Bot(pyglet.image.load('player.png'), self.gameWindowWidth, self.gameWindowLeft, self.gameWindowHeigth - self.gameWindowLeft)
    
    wallimg = pyglet.image.load('wall.png')
    self.wall = pyglet.sprite.Sprite(wallimg, self.gameWindowWidth // 2, - wallimg.height + self.gameWindowHeigth - 40)
        
    self.score_label = pyglet.text.Label(text=self.getScore(), x=self.gameWindowWidth // 2, y=self.gameWindowHeigth - 30, anchor_x='center', anchor_y='center')
    self.infoLabel = pyglet.text.Label(text=self.getInfo(), x=10, y=10)

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
    
    
    self.stateToBallCapt()
    
    @window.event
    def on_draw():
      window.clear()
      for x in self.drawable:
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
    self.ball.sprite.x = self.player.sprite.x + self.player.sprite.width
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
    self.bot.randStep(self.ball.sprite.y, self.ball.sprite.x > self.gameWindowWidth // 2)
    self.checkBallOut()
    self.isCollision()
    self.mechanicStd(dt)
    
  def ballCaptureStep(self):
    self.ball.sprite.y = self.player.sprite.y
    
  def isCollision(self):
    colis = self.collisoinsDetect()
    if colis:
      if abs(self.ball.dx) < self.ball.maxspeed:
        self.ball.dx = abs(self.ball.dx) + self.difficult
      if type(colis) == Player:
        self.ball.dx = abs(self.ball.dx)
       # self.redParticles.restart(self.ball.left, colis.sprite.y)
        self.whiteParticles.restart(self.ball.left, colis.sprite.y)
      else:
        self.ball.dx = - abs(self.ball.dx)
        #self.redParticles.restart(500,300)
      
      if colis.isMove:
        self.ball.dy += colis.isMove * colis.speed * 2
    
  def getScore(self):
    return self.scoreText1 + ' ' + str(self.playerWins) + '   ' + self.scoreText2 + ' ' + str(self.botWins)
  
  def updateScore(self):
    self.score_label.text = self.getScore()
  
  def updateLabels(self):
    self.infoLabel.text = self.getInfo()
    
  def getInfo(self):
    return "SPD: " + str(abs(self.ball.dx)) + '  '
    
  def isBallOut(self):
    if self.ball.sprite.x < self.gameWindowUp:
      #self.ball.ballReturn(1)
      return -1
    if self.ball.sprite.x > self.gameWindowWidth:
      self.ball.ballReturn(-1)
      return 1
    return 0
    
  def checkBallOut(self):
    isout = self.isBallOut()
    if 1 == isout:
      self.playerWins += random.randint(1,100)
      self.updateScore()
      self.blueParticles.restart(100,200)
      self.numberGenerator.makeNumber(self.playerWins, 50, 10, 30)
      self.stateToBallCapt()
    if -1 == isout:
      self.lose()
  
  def lose(self):
    self.botWins += 1
    self.updateScore()
    self.redParticles.restart(self.ball.sprite.x, self.ball.sprite.y)
    self.stateToBallCapt()
  
  def collisoinsDetect(self):
    faces = [self.player, self.bot]
    for x in faces:
      hei = max(self.ball.top, x.top) - min(self.ball.bottom, x.bottom)
      allheight = self.ball.sprite.height + x.sprite.height
      wid = max(self.ball.left, x.left) - min(self.ball.right, x.right)
      allwid = self.ball.sprite.width + 0
      
      if hei <= allheight and wid <= allwid:
        return x
    return False


class direction:
  up = 1
  down = -1

class Player:
  isMove = False
  speed = 20
  yMin = 0
  yMax = 0
  sprite = 0
  top = 0
  bottom = 0
  left = 0
  right = 0
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
      if (self.sprite.y ) < self.yMax:
        self.sprite.y += self.speed
    if self.isMove == direction.down:
      if (self.sprite.y ) > self.yMin:
        self.sprite.y -= self.speed
    
    self.top = self.sprite.y + self.sprite.height // 2
    self.bottom = self.sprite.y - self.sprite.height // 2

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
    self.speed = 10
  
  def randStep(self, ballY, inBotArea):
    self.i += 1
    if self.i > self.maxi:
      self.i = 0
      if inBotArea:
        if abs(ballY - self.sprite.y) > self.accur:
          if ballY > self.sprite.y:
            self.isMove = direction.up
          else:
            self.isMove = direction.down
        else:
          self.isMove = False
      else:
        #self.isMove = random.choice([direction.up, direction.down, False])
        self.isMove = False
    self.step()

class Ball():
  sprite = None
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
    self.sprite.x += self.dx * dt
    self.sprite.y += self.dy * dt
    self.right = self.sprite.x + self.sprite.width // 2
    self.left = self.sprite.x - self.sprite.width // 2
    self.top = self.sprite.y + self.sprite.height // 2
    self.bottom = self.sprite.y - self.sprite.height // 2
    self.collisoins()

  def collisoins(self):
    if self.sprite.y < self.yMin:
      self.dy = - self.dy
    if self.sprite.y > self.yMax:
      self.dy = - self.dy
  
  def ballReturn(self, direct):
    self.sprite.x = self.midX
    self.sprite.y = self.midY
    self.dx = self.speed * direct
    self.dy = 200
  
  def drop(self, dy):
    self.dy = dy
    self.dx = self.speed


if __name__ == '__main__':
  g = Game()
  pyglet.app.run()
