from pygletUtil import *
from util import *
import pyglet
from gameTypes import *

class Player(HasSprite):
    isMove = False
    yMin = 0
    yMax = 0
    top = 0
    bottom = 0
    left = 0
    right = 0
    #Stats: Статы
    speed = 20
    STR = 1
    Health = 20
    maxHealth = 22
    Exp = 0
    Lv = 0
    statPoints = 0

    LevelExp = {
        1: 100, 2: 300, 3: 1000 # есть генератор
    }


    #@debugDecor
    def __init__(self, img, x, yMin, yMax):
        center_image(img)
        x = x + img.width//2
        yMin = yMin + img.height // 2
        yMax -= img.height // 2
        self.sprite = Sprite(img, x = x, y = yMin)
        self.yMin = yMin
        self.yMax = yMax
        self.left = x
        self.right = x
        self.LevelExp = dict(enumerate(geomRange(10, 51, 1.2)))
        #print(self.LevelExp)

    def reinit(self):
        self.y = self.yMin

    def step(self):
        if self.isMove == direction.up:
            if (self.y ) < self.yMax:
                self.y += self.speed
        if self.isMove == direction.down:
            if (self.y ) > self.yMin:
                self.y -= self.speed

        self.top = self.y + self.height // 2
        self.bottom = self.y - self.height // 2

    def capture(self, block):
        """ Получение блока и опыта. """
        self.expGain(block.price)
        block.capture()

    def expGain(self, n):
        """ Получение опыта. """
        # смотрим сколько до след уровня
        tonext = self.LevelExp[self.Lv +1] - self.Exp
        if tonext > n: # если недостаточно то просто добавляем и выходим
            self.Exp += n
            return
        self.Exp += tonext # иначе добавляем сколько надо а остаток добавляем рекурсивно
        self.Lv += 1
        self.statPoints += 1
        self.Health = self.maxHealth
        self.expGain(n - tonext)

    def lose(self):
        self.Health = self.maxHealth

    def getStatText(self, stat):
        """ Получение описания и значения стата. """
        stats = {
            PlayerStatIndex.Exp: (self.Exp, 'Exp: '),
            PlayerStatIndex.Lv: (self.Lv, 'Lv '),
            PlayerStatIndex.Speed: (self.speed, 'Spd '),
            PlayerStatIndex.Str: (self.STR, 'Str '),
            PlayerStatIndex.statPoints: (self.statPoints, 'SP: '),
            PlayerStatIndex.Health: (self.Health, 'HP= ')
        }
        val, name = stats[stat]
        return name + str(val)

class Bot(Player):
    i = 0
    maxi = 4
    accur = 20
    #@debugDecor
    def __init__(self, img, x, yMin, yMax):
        x = x - img.width
        super().__init__(img, x, yMin, yMax)
        self.left = x + img.width
        self.right = x
        self.speed = 1 # difficult

    def randStep(self, ballY, inBotArea):
        """ Поведение бота. """
        self.i += 1
        if self.i > self.maxi:
            self.i = 0
            if inBotArea:
                if abs(ballY - self.y) > self.accur:
                    if ballY > self.y:
                        self.isMove = direction.up
                    else:
                        self.isMove = direction.down
                else:
                    self.isMove = False
            else:
                #self.isMove = random.choice([direction.up, direction.down, False])
                self.isMove = False
        self.step()

class Ball(HasSprite):
    dx = 200
    dy = 200
    speed = 400
    collided = []
    wh = 0
    yMax = 0
    xMax = 0
    yMin = 0
    midX = 0
    midY = 0
    left = 0
    right = 0
    top = 0
    bottom = 0
    maxspeed = 1000

    def __init__(self, img, width, height, marginBottom):
        self.collided = list()
        center_image(img)
        self.midX = width // 2
        self.midY = height // 2
        self.sprite = Sprite(img, x = width // 2, y = height // 2)
        self.wh = img.width // 2
        self.yMax = height - self.wh
        self.xMax = width - self.wh
        self.yMin = img.height // 2 + marginBottom

    def step(self, dt):
        self.sprite.rotation += 100 * dt
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.lastdt = dt
        self.recalcCoords()
        self.collisoins()

    def recalcCoords(self):
        """ Пересчёт крайних координат. """
        self.right = self.x + self.width // 2
        self.left = self.x - self.width // 2
        self.top = self.y + self.height // 2
        self.bottom = self.y - self.height // 2

    def stepBack(self, dx, dy):
        """ Шаг назад. (неполный)"""
        dx = (dx-self.x) - self.width
        dy = (dy-self.y) - self.width
        self.x -= self.dx * self.lastdt
        self.y -= self.dy * self.lastdt
        #self.x -= dx * (self.dx/self.dx)
        #self.y -= dy * (self.dy/self.dy)
        self.recalcCoords()

    def bounce(self):
        #self.stepBack()
        self.dx = -self.dx

    def collisoins(self):
        """ Проверка на пересечение и инверт вектора. """
        if self.y < self.yMin:
            self.dy = - self.dy
        if self.y > self.yMax:
            self.dy = - self.dy

    def ballReturn(self, direct):
        """ Возврат. """
        self.x = self.midX
        self.y = self.midY
        self.dx = self.speed * direct
        self.dy = 200

    def drop(self, dy):
        """ Выброс мяча от игрока. """
        self.dy = dy if dy != 0 else random.randint(-50,50)
        self.dx = self.speed

