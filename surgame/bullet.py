import util
import pygame
import images

bulimg = images.bulletImage 

class Bullet(util.Block):
    spd = 5
    def __init__(self, x, y, dx, dy):
        super().__init__(imgname=bulimg)
        self.dx = dx
        self.dy = dy
        self.rect.x = x
        self.rect.y = y

    def fly(self):
        self.rect.x += self.dx * self.spd
        self.rect.y += self.dy * self.spd
    
    def kill(self, enemies):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                return e # kill self & enemy
        return False

    def smash(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                return True
        return False
