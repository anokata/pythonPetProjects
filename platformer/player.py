import pygame
import pyganim

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
AnimGoRight = ['objects/walkmanR0.png','objects/walkmanR1.png','objects/walkmanR2.png']
AnimGoLeft = ['objects/walkmanL0.png','objects/walkmanL1.png','objects/walkmanL2.png']
AnimGoUp = ['objects/walkmanU0.png','objects/walkmanU1.png','objects/walkmanU2.png']
AnimJumpLeft = ['objects/walkmanS.png', 'objects/walkmanS.png']
AnimJumpRight = ['objects/walkmanS.png','objects/walkmanS.png']
AnimJump = ['objects/walkmanS.png']
AnimStand = ['objects/walkmanS.png']

class pgPlayer(Player, pygame.sprite.Sprite):
    rect = pygame.Rect(0,0,0,0)

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('catwall.png').convert()
        self.rect = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])
        self.rect.height += 0

        from itertools import repeat
        Anim = list(zip(AnimGoRight, list(repeat(AnimDelay, len(AnimGoRight)))))
        self.AnimRight = pyganim.PygAnimation(Anim)
        self.AnimRight.play()

        Anim = list(zip(AnimGoLeft, list(repeat(AnimDelay, len(AnimGoLeft)))))
        self.AnimLeft = pyganim.PygAnimation(Anim)
        self.AnimLeft.play()

        Anim = list(zip(AnimJumpLeft, list(repeat(AnimDelay, len(AnimJumpLeft)))))
        self.AnimJumpLeft = pyganim.PygAnimation(Anim)
        self.AnimJumpLeft.play()

        Anim = list(zip(AnimJumpRight, list(repeat(AnimDelay, len(AnimJumpRight)))))
        self.AnimJumpRight = pyganim.PygAnimation(Anim)
        self.AnimJumpRight.play()

        Anim = list(zip(AnimStand, list(repeat(AnimDelay, len(AnimStand)))))
        self.AnimStand = pyganim.PygAnimation(Anim)
        self.AnimStand.play()

        Anim = list(zip(AnimGoUp, list(repeat(AnimDelay, len(AnimGoUp)))))
        self.AnimUp = pyganim.PygAnimation(Anim)
        self.AnimUp.play()

        self.changeAnim(self.AnimStand)

    def changeAnim(self, a):
        self.image.fill(pygame.Color('#000000'))
        a.blit(self.image, (0, 0))
        #self.image.scroll(dy=20)

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


