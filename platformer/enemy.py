import player
import random
import pygame

AnimStand = ['objects/poringb.png', 'objects/poringb1.png','objects/poringb2.png']
class Enemy(player.pgPlayer):

    ticks = 0
    maxticks = 30
    spd = 1
    
    def __init__(self, x, y, screen, map):
        super().__init__(x, y, screen, map)
        self.image = pygame.image.load(AnimStand[0]).convert()
        self.AnimStand = self.animLoad(AnimStand) 
        self.changeAnim(self.AnimStand)
        size = self.image.get_rect().size
        self.rect = pygame.Rect(x, y, size[0], size[1])

        self.AnimRight = self.AnimStand
        self.AnimLeft = self.AnimStand
        self.AnimStand = self.AnimStand
        self.AnimUp = self.AnimStand
        self.AnimStandR = self.AnimStand
        self.AnimStandL = self.AnimStand

    def randomMove(self, dt, platforms, enemies):
        self.ticks += 1
        if self.ticks > self.maxticks:
            self.ticks = 0
            self.moving = random.randint(-1,1)
            self.movingud = random.randint(-1,1)
        self.moveSide(0, platforms, [])

