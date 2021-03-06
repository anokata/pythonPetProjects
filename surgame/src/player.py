import pygame
import sys
sys.path += ["lib",'./']
import gameInventory
from objectTypes import *
# TODO: отдельные ректы для рисования и физики. останавливаться когда бьёт?
import bullet
import particles
import images
import eventSystem
import path

import datafiles
import yaml
import inspect
import util
class Stats():
    exp = 0
    health = 10
    maxHealth = 100
    dmg = 1
    lv = 0


class Player(eventSystem.Publisher):
    moving = 0
    movingud = 0
    dy = 0
    dx = 0.0
    canPickUp = True

    spd = 4.0
    stats = None

    def __init__(self):
        super().__init__()
        self.stats = Stats()

    def step(self):
        pass

    def load(self):
        data = yaml.load(open(path.getPath(datafiles.playerStats)))
        print(data)
        self.setStatDict(data)

    def setStatDict(self, data):
        self.stats = Stats()
        for name, value in data.items():
            setattr(self.stats, name, value)

    def getStatDict(self):
        d = dict()
        for (name, value) in inspect.getmembers(self.stats):
            if not name.startswith('_'):
                d[name] = value
        return d

    def save(self):
        data = self.getStatDict()
        # TODO inventory save
        with open(path.getPath(datafiles.playerStats), 'w') as fout:
                yaml.dump(data, fout, default_flow_style=True)

    def getHealth(self):
        return self.stats.health

    def addHealth(self, amount):
        if self.stats.health + amount > self.stats.maxHealth:
            self.stats.health = self.stats.maxHealth
        else:
            self.stats.health += amount

    def expGain(self, amount):
        self.stats.exp += amount

wallInpact = 15
class pgPlayer(Player, pygame.sprite.Sprite):
    rect = pygame.Rect(0,0,0,0)
    rectImg = pygame.Rect(0,0,0,0)
    kicking = 0
    faceat = 0 # UP LEFT RIGHT
    inventory = None
    shootSpd = 10
    bulletSpd = 3
    shootTick = 0
    shootInterval = 100000

    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    MOVEUP = -1
    MOVEDOWN = 1
    MOVERIGHT = 1
    MOVELEFT = -1

    def __init__(self, x, y, screen, map):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = util.imgLoadN(images.playerAnimRight[0])
        self.image.set_colorkey((0,0,0))
        size = self.image.get_rect().size
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.rect.height -= wallInpact
        self.rect.top += wallInpact
        self.rectImg = pygame.Rect(x, y, self.image.get_rect().size[0],
                         self.image.get_rect().size[1])

        self.AnimRight = util.animLoad(images.playerAnimRight) 
        self.AnimLeft = util.animLoad(images.playerAnimLeft) 
        self.AnimStand = util.animLoad(images.playerAnimStand) 
        self.AnimUp = util.animLoad(images.playerAnimUp) 
        self.AnimStandR = util.animLoad(images.playerAnimStandR) 
        self.AnimStandL = util.animLoad(images.playerAnimStandL) 

        self.AnimKickL = util.animLoad(images.playerAnimKickL)
        self.AnimKickR = util.animLoad(images.playerAnimKickR)
        self.AnimKickTicks = 10

        self.changeAnim(self.AnimStand)

        self.inventory = gameInventory.GInventory(screen)
        self.screen = screen
        self.map = map
        self.bullets = list()
        self.particles = list()

    def changeAnim(self, a):
        self.anim = a

    def drawAnim(self):
        self.image.fill(pygame.Color('#000000'))
        self.anim.blit(self.image, (0, 0))

    def eat(self):
        food = self.inventory.getFood()
        if food:
            hpGain = self.inventory.eat(food)
            self.addHealth(hpGain)

    def startShoot(self):
        self.shootTick = self.shootInterval
        self.send('shoot', 'P')
        self.shoot()
    
    def stopShoot(self):
        self.shootTick = 0

    def shooting(self):
        if self.shootTick != 0:
            self.shootTick -= 1
            if self.shootTick % self.shootSpd == 0:
                self.shoot()

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
        
        dx *= self.bulletSpd
        dy *= self.bulletSpd
        #dy += self.movingud
        #dx += self.moving
        self.bullets.append(bullet.Bullet(self.rect.x, self.rect.y, dx, dy))
        self.send('shoot', 'P')

    def draw(self, cam):
        self.drawAnim()
        self.screen.blit(self.image, self.getRect(cam))
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
                self.send('bullet', 'wall')

        for b in bullet_to_remove:
            if b in self.bullets:
                self.bullets.remove(b)

        for e in enemies_to_wound:
            killed = e.wound(self.stats.dmg)
            if killed:
                enemies_to_kill.append(e)
                self.expGain(killed)
                self.send('killed', 'P')
        for e in enemies_to_kill:
            if e in enemies:
                enemies.remove(e)

        self.particlesStep()
        self.shooting()

    def particlesStep(self):
        particles_to_remove = list() ## PATTERN TODO filter it!
        for p in self.particles:
            r = p.step()
            if not r:
                particles_to_remove.append(p)

        for p in particles_to_remove:
            if p in self.particles:
                self.particles.remove(p)

    def movingUp(self):
        self.movingud = self.MOVEUP

    def movingDown(self):
        self.movingud = self.MOVEDOWN

    def movingLeft(self):
        self.moving = self.MOVELEFT

    def movingRight(self):
        self.moving = self.MOVERIGHT

    def stop(self, mix=None):
        if mix:
            self.moving = 0
        elif not mix:
            self.movingud = 0
        else:
            self.movingud = 0
            self.moving = 0

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
        
        self.dx = self.moving * self.spd
        self.dy = self.movingud * self.spd

        
        self.rect.x += self.dx
        self.rect.x = int(self.rect.x)
        self.collide(self.dx, 0, platforms)

        self.rect.y += self.dy
        self.rect.y = int(self.rect.y)
        self.collide(0, self.dy, platforms)

        self.collideEnemies(enemies)
        return self.stats.health >= 0

    def collideEnemies(self, enemies):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                self.wound()
                self.particles.append(particles.Particles(self.rect.x, self.rect.y, n=3, imgname=images.particleBlood))
        self.handleDead()

    def handleDead(self):
        if self.stats.health < 0:
            self.stats.health = 0
            self.send('die', 0)
            self.stats.health = self.stats.maxHealth

    def wound(self):
        self.addHealth(-1)

    def collide_platforms(self, p, dx, dy):
        if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
            #self.collideObject(p)
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


    def collide(self, dx, dy, platforms):
        self.rectphistoimg()
        px = self.rect.x // self.map.w
        py = self.rect.y // self.map.w
        k = platforms.keys()
        area = 3
        pls = util.getListNearFromDict(platforms, self)
        for p in pls:
            self.collide_platforms(p, dx, dy)
        self.rectphistoimg()


