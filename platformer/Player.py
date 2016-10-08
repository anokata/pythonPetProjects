from pygletUtil import *
class Player(HasSprite):
    health = 100
    spd = 300
    moving = False

    def __init__(self):
        self.sprite = cat = makeSprite('cat0.png', 64,64)

    def moveSide(self, dt):
        if self.moving == 1: #right
            self.x += self.spd * dt
        elif self.moving == -1:
            self.x -= self.spd * dt
