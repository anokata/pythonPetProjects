import pyglet
from pyglet.window import key
import random

def mechanic(dt):
  spriteOne.x += 80 * dt
  spriteOne.rotation += 100 * dt
  spriteOne.y += random.randint(10,50) * dt

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

window = pyglet.window.Window()
pyglet.gl.glClearColor(0.7,0.5,0.3, 1)

ball = pyglet.image.load('ball3.png')
center_image(ball)
spriteOne = pyglet.sprite.Sprite(ball, x = 20, y = 20)

player = pyglet.image.load('player.png')
center_image(player)
spritePlayer = pyglet.sprite.Sprite(player, x = 20, y = window.height // 2)
playerSpeed = 10
pyglet.clock.schedule_interval(mechanic, 1.0/30)


score_label = pyglet.text.Label(text="Player: 0  Bot: 0", x=window.width // 2, y=window.height - 30, anchor_x='center', anchor_y='center')


@window.event
def on_draw():
  window.clear()
  score_label.draw()
  spriteOne.draw()
  spritePlayer.draw()

@window.event
def on_key_press(symbol, mod):
  if symbol == key.A:
    print('A')
  if symbol == key.LEFT:
    print('left')
  if symbol == key.UP:
    spritePlayer.y += playerSpeed
  if symbol == key.DOWN:
    spritePlayer.y -= playerSpeed
#window.push_handlers(pyglet.window.event.WindowEventLogger())


if __name__ == '__main__':
  pyglet.app.run()
