""" Main class module. """
import cocos
import sys
sys.path += ["../modules", "../"]
from makeAnimation import makeAnimObj
#http://python.cocos2d.org/doc/programming_guide/quickstart.html
# пока как то не впечатляет. сложно.
# Есть сцены(состояния почти не нужны) + слои. Есть система событий.
class Game(cocos.layer.Layer):
    """ Main class """
    is_event_handler = True

    def __init__(self):
        """ Init."""
        super(Game, self).__init__()
        label = cocos.text.Label("HW!@#$%^&*()",
                font_size=30, position=(200, 200))
        self.add(label)
        bGround0 = cocos.sprite.Sprite('ground0.png',position=(0,200))
        bGround0.x = bGround0.width
        bGround0.scale = 3
        self.add(bGround0, z=1)

        self.cat = cat = cocos.sprite.Sprite('cat0.png')
        cat.x = cat.width +10
        cat.y = 200
        cat.scale = 3
        self.add(cat, z=1)

        #self.a = makeAnimObj('../pong/block6anim/pearl', 100, 100, 8, 0.1)
        #self.add(self.a)

    def on_key_press (self, key, modifiers):
        self.cat.x += 10
        #print(key)
    def on_key_release (self, key, modifiers):
        pass

    def run(self):
        """ Run the game. IO -> IO"""
        pass

def test():
    """ Test module fun. """
    pass

if __name__ == "__main__":
    test()
