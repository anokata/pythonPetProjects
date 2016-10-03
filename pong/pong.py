import pyglet
from pyglet.window import key
import random

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

class Game:
  playerWins = 0
  botWins = 0
  ball = None
  player = None
  bot = None
  
  window = None
  score_label = None
  
  def __init__(self):
    self.window = pyglet.window.Window()
    window = self.window
    
    self.ball = Ball(pyglet.image.load('ball3.png'), window.width, window.height)
    self.player = Player(window.height, pyglet.image.load('player.png'))
    self.bot = Bot(window.height, pyglet.image.load('player.png'), window.width - 20)
    
    self.score_label = pyglet.text.Label(text="Player: 0  Bot: 0", x=window.width // 2, y=window.height - 30, anchor_x='center', anchor_y='center')
    pyglet.gl.glClearColor(0.7,0.5,0.3, 1)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.clock.schedule_interval(self.mechanic, 1.0/30)
    
    @window.event
    def on_draw():
      window.clear()
      g.score_label.draw()
      g.ball.sprite.draw()
      g.player.sprite.draw()
      g.bot.sprite.draw()

    @window.event
    def on_key_press(symbol, mod):
      if symbol == key.A:
        print('A')
      if symbol == key.LEFT:
        print('left')
      if symbol == key.UP:
        g.player.isMove = direction.up
      if symbol == key.DOWN:
        g.player.isMove = direction.down

    @window.event
    def on_key_release(symbol, mod):
      if symbol == key.UP or symbol == key.DOWN:
        g.player.isMove = False

  def mechanic(self, dt):
    self.ball.step(dt)
    self.player.step()
    self.bot.randStep()

class direction:
  up = 1
  down = 2

class Player:
  isMove = False
  speed = 20
  yMin = 0
  yMax = 0
  sprite = 0
  
  def __init__(self, height, img, x=20):
    center_image(img)
    self.sprite = pyglet.sprite.Sprite(img, x = x, y = height // 2)
    self.yMin = img.height // 2 - self.speed
    self.yMax = height - img.height // 2 + self.speed
  
  def step(self):
    if self.isMove == direction.up:
      if (self.sprite.y + self.speed) < self.yMax:
        self.sprite.y += self.speed
    if self.isMove == direction.down:
      if (self.sprite.y - self.speed) > self.yMin:
        self.sprite.y -= self.speed

class Bot(Player):
  i = 0
  maxi = 4
  
  def randStep(self):
    self.i += 1
    if self.i > self.maxi:
      self.i = 0
      self.isMove = random.choice([direction.up, direction.down, False])
    self.step()

class Ball():
  sprite = None
  dx = 10
  dy = 100
  collided = []
  wh = 0
  yMax = 0
  
  def __init__(self, img, width, height):
    center_image(img)
    self.sprite = pyglet.sprite.Sprite(img, x = width // 2, y = height // 2)
    self.wh = img.width // 2
    self.yMax = height - self.wh

  def step(self, dt):
    self.sprite.rotation += 100 * dt
    self.sprite.x += self.dx * dt
    self.sprite.y += self.dy * dt
    self.collisoins()

  def collisoins(self):
    if self.sprite.y < self.wh:
      self.dy = - self.dy
    if self.sprite.y > self.yMax:
      self.dy = - self.dy


if __name__ == '__main__':
  g = Game()
  pyglet.app.run()
