import player
import random
import pygame
import yaml
import datafiles

class Enemy(player.pgPlayer):

    ticks = 0
    maxticks = 30
    spd = 1
    health = 2
    canPickUp = False
    
    def __init__(self, x, y, screen, map, load=True):
        super().__init__(x, y, screen, map)
        if load:
            self.load(x, y)

    def load(self, x, y):
        AnimStand = self.animStand
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

    def wound(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

class EnemyFactory():
    enemiesFileName = datafiles.enemies 

    def __init__(self, screen, map):
        self.screen = screen
        self.map = map
        self.load()

    def load(self):
        self.prototypes = yaml.load(open(self.enemiesFileName))

    def create(self, name, x, y):
        e = False
        if name in self.prototypes:
            objectModel = self.prototypes[name]
            e = Enemy(0,0, self.screen, self.map, load=False)
            for propname, propvalue in objectModel.items():
                setattr(e, propname, propvalue)
            e.load(x, y)
        return e


