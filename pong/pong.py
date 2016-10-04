import pyglet
from pyglet.window import key
import random
import math

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

def objDistance(s1, s2):
  return distance(s1.sprite.x, s1.sprite.y, s2.sprite.x, s2.sprite.y)

def distance(x, y, a, b):
  from math import sqrt
  return sqrt((x-a)*(x-a) + (y-b)*(y-b))

class Particles:
  sprites = []
  speed = 2
  lifeTime = 100
  initLifeTime = 0
  
  def __init__(self, img, n, lifeTime, x, y):
    self.sprites = list()  # Необходимо все неэлемнтарные типы так создавать
    self.lifeTime = 0
    self.initLifeTime = lifeTime
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
  
  def end(self):
    pass
    
  def restart(self, x, y):
    for i in self.sprites:
      i.x = x
      i.y = y
    self.lifeTime = self.initLifeTime

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
  scoreText1 = "Player: "
  scoreText2 = "Bot: "
  difficult = 100
  
  wall = None
  redParticles = None
  blueParticles = None
  
  def __init__(self):
    random.seed()
    self.window = pyglet.window.Window()
    window = self.window
    
    self.ball = Ball(pyglet.image.load('ball3.png'), window.width, window.height)
    self.player = Player(window.height, pyglet.image.load('player.png'))
    self.bot = Bot(window.height, pyglet.image.load('player.png'), window.width - 20)
    
    wallimg = pyglet.image.load('wall.png')
    self.wall = pyglet.sprite.Sprite(wallimg, window.width // 2, - wallimg.height + window.height - 40)
        
    self.score_label = pyglet.text.Label(text=self.getScore(), x=window.width // 2, y=window.height - 30, anchor_x='center', anchor_y='center')
    self.infoLabel = pyglet.text.Label(text=self.getInfo(), x=10, y=10)
    self.labels += [self.infoLabel]
    pyglet.gl.glClearColor(0.7,0.5,0.3, 1)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.clock.schedule_interval(self.mechanic, 1.0/30)
    
    self.redParticles = Particles(pyglet.image.load('redstar18.png'), 15, 14, 300, 100)
    self.blueParticles = Particles(pyglet.image.load('bluestar24.png'), 15, 18, 300, 100)
    
    @window.event
    def on_draw():
      window.clear()
      self.wall.draw()
      self.score_label.draw()
      self.ball.sprite.draw()
      self.player.sprite.draw()
      self.bot.sprite.draw()
      self.blueParticles.draw()
      self.redParticles.draw()
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

    @window.event
    def on_key_release(symbol, mod):
      if symbol == key.UP or symbol == key.DOWN or symbol == key.LEFT or symbol == key.RIGHT:
        g.player.isMove = False

  def mechanic(self, dt):
    self.ball.step(dt)
    self.player.step()
    self.bot.randStep(self.ball.sprite.y, self.ball.sprite.x > self.window.width // 2)
    self.checkBallOut()
    self.isCollision()
    self.updateLabels()
    self.blueParticles.step()
    self.redParticles.step()
    
  def isCollision(self):
    colis = self.collisoinsDetect()
    if colis:
      if abs(self.ball.dx) < self.ball.maxspeed:
        self.ball.dx = abs(self.ball.dx) + self.difficult
      if type(colis) == Player:
        self.ball.dx = abs(self.ball.dx)
        self.redParticles.restart(100,300)
      else:
        self.ball.dx = - abs(self.ball.dx)
        self.redParticles.restart(500,300)
      
      if colis.isMove:
        self.ball.dy += colis.isMove * colis.speed * 2
    
  def getScore(self):
    return self.scoreText1 + ' ' + str(self.playerWins) + '   ' + self.scoreText2 + ' ' + str(self.botWins)
  
  def updateScore(self):
    self.score_label.text = self.getScore()
  
  def updateLabels(self):
    self.infoLabel.text = self.getInfo()
    
  def getInfo(self):
    return "SPD: " + str(abs(self.ball.dx)) + ' | '
    
  def checkBallOut(self):
    isout = self.ball.isOut()
    if 1 == isout:
      self.playerWins += 1
      self.updateScore()
      self.blueParticles.restart(100,200)
    if -1 == isout:
      self.botWins += 1
      self.updateScore()
      self.blueParticles.restart(500,200)
  
  def collisoinsDetect(self):
    faces = [self.player, self.bot]
    for x in faces:
      hei = max(self.ball.top, x.top) - min(self.ball.bottom, x.bottom)
      allheight = self.ball.sprite.height + x.sprite.height
      wid = max(self.ball.leftX, x.left) - min(self.ball.rightX, x.right)
      allwid = self.ball.sprite.width + 0
      
      if hei <= allheight and wid <= allwid:
        return x
    return False


class direction:
  up = 1
  down = 2

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
  
  def __init__(self, height, img, x=20):
    center_image(img)
    self.sprite = pyglet.sprite.Sprite(img, x = x, y = height // 2)
    self.yMin = img.height // 2 - self.speed
    self.yMax = height - img.height // 2 + self.speed
    self.left = x // 2# - self.sprite.width // 2
    self.right = x // 2# + self.sprite.width // 2
  
  def step(self):
    if self.isMove == direction.up:
      if (self.sprite.y + self.speed) < self.yMax:
        self.sprite.y += self.speed
    if self.isMove == direction.down:
      if (self.sprite.y - self.speed) > self.yMin:
        self.sprite.y -= self.speed
    
    self.top = self.sprite.y + self.sprite.height // 2
    self.bottom = self.sprite.y - self.sprite.height // 2

class Bot(Player):
  i = 0
  maxi = 4
  accur = 20
  
  def __init__(self, height, img, x):
    super().__init__(height, img, x)
    self.left = x
    self.right = x
  
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
  speed = 200
  collided = []
  wh = 0
  yMax = 0
  xMax = 0
  midX = 0
  midY = 0
  leftX = 0
  rightX = 0
  top = 0
  bottom = 0
  maxspeed = 1000
  
  def __init__(self, img, width, height):
    center_image(img)
    self.midX = width // 2
    self.midY = height // 2
    self.sprite = pyglet.sprite.Sprite(img, x = width // 2, y = height // 2)
    self.wh = img.width // 2
    self.yMax = height - self.wh
    self.xMax = width - self.wh

  def step(self, dt):
    self.sprite.rotation += 100 * dt
    self.sprite.x += self.dx * dt
    self.sprite.y += self.dy * dt
    self.rightX = self.sprite.x + self.sprite.width // 2
    self.leftX = self.sprite.x - self.sprite.width // 2
    self.top = self.sprite.y + self.sprite.height // 2
    self.bottom = self.sprite.y - self.sprite.height // 2
    self.collisoins()

  def collisoins(self):
    if self.sprite.y < self.wh:
      self.dy = - self.dy
    if self.sprite.y > self.yMax:
      self.dy = - self.dy
      
  def isOut(self):
    if self.sprite.x < self.wh:
      self.ballReturn(1)
      return -1
    if self.sprite.x > self.xMax:
      self.ballReturn(-1)
      return 1
    return 0
  
  def ballReturn(self, direct):
    self.sprite.x = self.midX
    self.sprite.y = self.midY
    self.dx = self.speed * direct
    self.dy = 200


if __name__ == '__main__':
  g = Game()
  pyglet.app.run()
