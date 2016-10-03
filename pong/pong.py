import pyglet
from pyglet.window import key
import random

class direction:
  up = 1
  down = 2

class Player:
  isMove = False
  speed = 20
  yMin = 0
  yMax = 0
  sprite = 0
  
  def __init__(self, yMax, img):
    center_image(img)
    self.sprite = pyglet.sprite.Sprite(img, x = 20, y = window.height // 2)
    self.yMin = img.height // 2 - self.speed
    self.yMax = yMax - img.height // 2 + self.speed
  
  def step(self):
    if self.isMove == direction.up:
      if (self.sprite.y + self.speed) < self.yMax:
        self.sprite.y += self.speed
    if self.isMove == direction.down:
      if (self.sprite.y - self.speed) > self.yMin:
        self.sprite.y -= self.speed

def mechanic(dt):
  spriteOne.x += 80 * dt
  spriteOne.rotation += 100 * dt
  spriteOne.y += random.randint(10,50) * dt
  p.step()

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

window = pyglet.window.Window()
pyglet.gl.glClearColor(0.7,0.5,0.3, 1)

ball = pyglet.image.load('ball3.png')
center_image(ball)
spriteOne = pyglet.sprite.Sprite(ball, x = 20, y = 20)

p = Player(window.height, pyglet.image.load('player.png'))

pyglet.clock.schedule_interval(mechanic, 1.0/30)

score_label = pyglet.text.Label(text="Player: 0  Bot: 0", x=window.width // 2, y=window.height - 30, anchor_x='center', anchor_y='center')


@window.event
def on_draw():
  window.clear()
  score_label.draw()
  spriteOne.draw()
  p.sprite.draw()

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
