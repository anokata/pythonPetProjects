import pygame
import pyganim
from itertools import repeat

class Player():
    health = 100
    spd = 4.0
    spdj = 5.0
    moving = 0
    movingud = 0
    dy = 0
    dx = 0.0
    energy = 100.0

    def __init__(self):
        pass
    
    def step(self):
        self.energy -= 0.01

# Player anim
AnimDelay = 0.1 # скорость смены кадров
AnimRight = ['objects/walkmanR0.png','objects/walkmanR1.png','objects/walkmanR2.png']
AnimLeft = ['objects/walkmanL0.png','objects/walkmanL1.png','objects/walkmanL2.png']
AnimUp = ['objects/walkmanU0.png','objects/walkmanU1.png','objects/walkmanU2.png']
AnimStand = ['objects/stand0.png','objects/stand1.png','objects/stand2.png']
AnimKick = ['objects/kick0.png','objects/kick1.png','objects/kick2.png', 'objects/kick3.png']

class pgPlayer(Player, pygame.sprite.Sprite):
    rect = pygame.Rect(0,0,0,0)
    kicking = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('catwall.png').convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])
        self.rect.height += 0

        self.AnimRight = self.animLoad(AnimRight) 
        self.AnimLeft = self.animLoad(AnimLeft) 
        self.AnimStand = self.animLoad(AnimStand) 
        self.AnimUp = self.animLoad(AnimUp) 

        self.AnimKick = self.animLoad(AnimKick)
        self.AnimKickTicks = 10

        self.changeAnim(self.AnimStand)

    def animLoad(self, animlist):
        animlistdelay = list(zip(animlist, list(repeat(AnimDelay, len(animlist)))))
        ranim = pyganim.PygAnimation(animlistdelay)
        ranim.play()
        return ranim

    def changeAnim(self, a):
        self.image.fill(pygame.Color('#000000'))
        a.blit(self.image, (0, 0))
        #self.image.scroll(dy=20)

    def kick(self):
        self.kicking = self.AnimKickTicks

    def moveSide(self, dt, platforms, enemies):
        self.step()
        if self.dx < 0:
            self.changeAnim(self.AnimLeft)
        elif self.dx > 0:
            self.changeAnim(self.AnimRight)
        elif self.dy > 0 or self.dy < 0:
            self.changeAnim(self.AnimUp)
        else:
            self.changeAnim(self.AnimStand)

        if self.kicking:
            self.changeAnim(self.AnimKick)
            self.kicking -= 1
        
        self.dx = - self.moving * self.spd
        self.dy = - self.movingud * self.spd

        
        self.rect.x += self.dx
        self.collide(self.dx, 0, platforms)

        self.rect.y += self.dy
        self.collide(0, self.dy, platforms)

        self.collideEnemies(enemies)

    def collideEnemies(self, enemies):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                self.dx = -self.dx

    def collide(self, dx, dy, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if dx > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо
                if dx < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if dy > 0:                    
                    self.rect.bottom = p.rect.top  

                if dy < 0:                   
                    self.rect.top = p.rect.bottom 


