import pygame
import pyganim
from itertools import repeat
# TODO: отдельные ректы для рисования и физики. останавливаться когда бьёт?

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
AnimStandR = ['objects/standR0.png','objects/standR1.png']
AnimStandL = ['objects/standL0.png','objects/standL1.png']
AnimKickL = ['objects/kick0.png','objects/kick1.png','objects/kick2.png', 'objects/kick3.png']
AnimKickR = ['objects/kickR0.png','objects/kickR1.png','objects/kickR2.png', 'objects/kickR3.png']
wallInpact = 15

class pgPlayer(Player, pygame.sprite.Sprite):
    rect = pygame.Rect(0,0,0,0)
    rectImg = pygame.Rect(0,0,0,0)
    kicking = 0
    faceat = 0 # UP LEFT RIGHT

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('catwall.png').convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])
        self.rect.height -= wallInpact
        self.rect.top += wallInpact
        self.rectImg = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])

        self.AnimRight = self.animLoad(AnimRight) 
        self.AnimLeft = self.animLoad(AnimLeft) 
        self.AnimStand = self.animLoad(AnimStand) 
        self.AnimUp = self.animLoad(AnimUp) 
        self.AnimStandR = self.animLoad(AnimStandR) 
        self.AnimStandL = self.animLoad(AnimStandL) 

        self.AnimKickL = self.animLoad(AnimKickL)
        self.AnimKickR = self.animLoad(AnimKickR)
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
    
    def getRect(self, cam):
        return cam.calcXY(self.rectImg.x, self.rectImg.y)

    def kick(self):
        self.kicking = self.AnimKickTicks

    def rectphistoimg(self):
        self.rectImg = pygame.Rect(self.rect.x, self.rect.y - wallInpact, self.rectImg.width, self.rectImg.height)

    def moveSide(self, dt, platforms, enemies):
        self.step()
        if self.faceat == 0:
            self.changeAnim(self.AnimStand)
        elif self.faceat == 1:
            self.changeAnim(self.AnimStandR)
        elif self.faceat == 2:
            self.changeAnim(self.AnimStandL)

        if self.dx < 0:
            self.changeAnim(self.AnimLeft)
            self.faceat = 2
        elif self.dx > 0:
            self.changeAnim(self.AnimRight)
            self.faceat = 1
        elif self.dy > 0 or self.dy < 0:
            self.faceat = 0
            self.changeAnim(self.AnimUp)

        if self.kicking:
            if self.faceat == 1:
                self.changeAnim(self.AnimKickR)
            else:
                self.changeAnim(self.AnimKickL)
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
        self.rectphistoimg()
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
        self.rectphistoimg()


