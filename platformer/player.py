import pygame
import pyganim
from itertools import repeat
import gameInventory
from objectTypes import *
# TODO: отдельные ректы для рисования и физики. останавливаться когда бьёт?
import bullet
import particles

class Player():
    health = 100
    spd = 4.0
    spdj = 5.0
    moving = 0
    movingud = 0
    dy = 0
    dx = 0.0
    energy = 100.0
    canPickUp = True

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
    inventory = None

    def __init__(self, x, y, screen, map):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('none.png').convert()
        size = self.image.get_rect().size
        self.rect = pygame.Rect(x, y, size[0], size[1])
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

        self.inventory = gameInventory.GInventory(screen)
        self.screen = screen
        self.map = map
        self.bullets = list()
        self.particles = list()

    def animLoad(self, animlist):
        animlistdelay = list(zip(animlist, list(repeat(AnimDelay, len(animlist)))))
        ranim = pyganim.PygAnimation(animlistdelay)
        ranim.play()
        return ranim

    def changeAnim(self, a):
        self.image.fill(pygame.Color('#000000'))
        a.blit(self.image, (0, 0))
        #self.image.scroll(dy=20)

    def shoot(self):
        dx = 0
        if self.faceat == self.RIGHT:
            dx = 1
        elif self.faceat == self.LEFT:
            dx = -1
        dy = 0
        if self.faceat == self.UP:
            dy = 1
        if self.faceat == self.DOWN:
            dy = -1

        dy -= self.movingud
        dx -= self.moving
        self.bullets.append(bullet.Bullet(self.rect.x, self.rect.y, dx, dy))

    def drawBullets(self, cam):
        for b in self.bullets:
            b.draw(b.rect.x, b.rect.y, cam, self.screen)

    def draw(self, cam):
        self.screen.blit(self.image, self.getRect(cam))
        self.drawBullets(cam)
        self.drawParticles(cam)

    def drawParticles(self, cam):
        for p in self.particles:
            p.draw(cam, self.screen)

    
    def getRect(self, cam):
        return cam.calcXY(self.rectImg.x, self.rectImg.y)

    def kick(self):
        self.kicking = self.AnimKickTicks

    def rectphistoimg(self):
        self.rectImg = pygame.Rect(self.rect.x, self.rect.y - wallInpact, self.rectImg.width, self.rectImg.height)

    def allstep(self, enemies, platforms):
        bullet_to_remove = list()
        enemies_to_wound = list()
        enemies_to_kill = list()
        for b in self.bullets:
            b.fly()
            killed = b.kill(enemies)
            if killed:
                bullet_to_remove.append(b)
                enemies_to_wound.append(killed)
                self.particles.append(particles.Particles(b.rect.x, b.rect.y))

            smashed = b.smash(platforms)
            if smashed:
                bullet_to_remove.append(b)
                self.particles.append(particles.Particles(b.rect.x, b.rect.y))

        for b in bullet_to_remove:
            if b in self.bullets:
                self.bullets.remove(b)
        for e in enemies_to_wound:
            killed = e.wound(1)
            if killed:
                enemies_to_kill.append(e)
        for e in enemies_to_kill:
            if e in enemies:
                enemies.remove(e)

        self.particlesStep()

    def particlesStep(self):
        particles_to_remove = list() ## PATTERN TODO
        for p in self.particles:
            r = p.step()
            if not r:
                particles_to_remove.append(p)

        for p in particles_to_remove:
            if p in self.particles:
                self.particles.remove(p)


    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    def moveSide(self, dt, platforms, enemies):
        self.step()
        self.allstep(enemies, platforms)
        if self.faceat == self.UP or self.faceat == self.DOWN:
            self.changeAnim(self.AnimStand)
        elif self.faceat == self.RIGHT:
            self.changeAnim(self.AnimStandR)
        elif self.faceat == self.LEFT:
            self.changeAnim(self.AnimStandL)

        if self.dx < 0:
            self.changeAnim(self.AnimLeft)
            self.faceat = self.LEFT
        elif self.dx > 0:
            self.changeAnim(self.AnimRight)
            self.faceat = self.RIGHT
        elif self.dy > 0:
            self.faceat = self.UP
            self.changeAnim(self.AnimUp)
        elif self.dy < 0:
            self.faceat = self.DOWN
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
        return self. health > 0

    def collideEnemies(self, enemies):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                self.health -= 1
                self.particles.append(particles.Particles(self.rect.x, self.rect.y, n=3, imgname='objects/particleBlood.png'))

    def collideObject(self, phisObj):
        #print(phisObj.obj.typ)
        if self.canPickUp:
            if phisObj.obj.typ == FOOD:
                if self.inventory.add(phisObj.obj):
                    #надо убрать объект с карты
                    self.map.removeObject(phisObj)

    def collide(self, dx, dy, platforms):
        self.rectphistoimg()
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                self.collideObject(p)
                if p.obj.baseObject.passable:
                    return
                if dx > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо
                if dx < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if dy > 0:                    
                    self.rect.bottom = p.rect.top  

                if dy < 0:                   
                    self.rect.top = p.rect.bottom 
        self.rectphistoimg()


