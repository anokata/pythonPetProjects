import pyglet
window = pyglet.window.Window()
pyglet.gl.glClearColor(0.7,0.5,0.3, 1)
#img pyglet.image.load('')
#pyglet.clock.schedule_interval(fun, 1.0/10)
#spriteOne = pyglet.sprite.Sprite(img)
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
@window.event
def on_draw():
  window.clear()
  label.draw()
  #spriteOne.draw()

pyglet.app.run()
