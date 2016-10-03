import pyglet
from pyglet.window import key
import random

class Game:
  playerWins = 0
  botWins = 0

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

def mechanic(dt):
  ball.step(dt)
  p.step()
  bot.randStep()

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

window = pyglet.window.Window()
pyglet.gl.glClearColor(0.7,0.5,0.3, 1)

ball = Ball(pyglet.image.load('ball3.png'), window.width, window.height)
p = Player(window.height, pyglet.image.load('player.png'))
bot = Bot(window.height, pyglet.image.load('player.png'), window.width - 20)

pyglet.clock.schedule_interval(mechanic, 1.0/30)

score_label = pyglet.text.Label(text="Player: 0  Bot: 0", x=window.width // 2, y=window.height - 30, anchor_x='center', anchor_y='center')


@window.event
def on_draw():
  window.clear()
  score_label.draw()
  ball.sprite.draw()
  p.sprite.draw()
  bot.sprite.draw()

@window.event
def on_key_press(symbol, mod):
  if symbol == key.A:
    print('A')
  if symbol == key.LEFT:
    print('left')
  if symbol == key.UP:
    p.isMove = direction.up
  if symbol == key.DOWN:
    p.isMove = direction.down

@window.event
def on_key_release(symbol, mod):
  if symbol == key.UP or symbol == key.DOWN:
    p.isMove = False

#window.push_handlers(pyglet.window.event.WindowEventLogger())


if __name__ == '__main__':
  pyglet.app.run()
