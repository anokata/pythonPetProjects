""" Syti.
TODO:
 вот задача. есть множество параметров(чисел) и в зависимости от множества условий на них, соотвествует
  какому то состоянию. то есть кортеж чисел отобразить в одну из строк(одно число).
     может если их как то обработать(перемножить/сложить) то по диапозонам уже одного числа можно будет определить?
    одни параметры зависят от других? есть главнее? отсеивать сначала по порядку. число -> возможности для других
   словарь - парам1: список словарей-условий для других параметров.
   допустим параметры  a b c, s=(a+b+c). и условия:
        a,b,c<2 & s < 7 -> "1".
        ...
     мне же просто. по одному-3 парам. определяется часть состояния.. голодный, замёрзший...
    у каждого есть модель поведения - изначально случайная. - список действий по порядку?
    могут размножаться (энергия тратится) - модель потомка по 50% от родителей
    можно создавать энергию но это требует времени и энергии.
"""
#World is module
from collections import defaultdict
from time import sleep

def cls():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

class Space:
    energy = 0
    def charForMap(self):
        return '.'
    def step(self):
        pass

worldmap = defaultdict(list)

WorldW, WorldH = 10, 10

def createWorld():
    for x in range(WorldW):
        for y in range(WorldH):
            addObject(Space(), x, y)

def addObject(o, x, y):
    worldmap[(x, y)] += [o]
    return o

def clearDead():
    """ Уберём всё что не содержит энергии """
    for x in range(WorldW):
        for y in range(WorldH):
            worldmap[x,y] = list(filter(lambda o: isinstance(o, Space) or o.energy > 0, worldmap[x,y]))

class Eatable():
    energy = 5.0
    degradation = 0.8

    def step(self):
        """ Еда постепенно портится """
        self.energy -= self.degradation

    def charForMap(self):
        return chr(ord('b') + int(self.energy))

    def __str__(self):
        return "Enrg:%.2f" % (self.energy)

class Person(Eatable):
    """."""
    # Статы
    health = 100.0
    age = 0
    energy = 100.0
    # Траты
    energyAtstep = 10.1
    happyness = 100.0
    # другие показатели
    canEatAtStep = 1.0
    name = 'Person'

    # или сделать таблицу(словарь) какой стат, на что уменьшается как часто?
    #clothe
    def step(self):
        """ Шажок одного человека... """
        self.age += 1
        self.energy -= self.energyAtstep

    def __str__(self):
        return "H:%.2f  Age:%i  Enrg:%.2f" % (self.health, self.age, self.energy)
    __repr__ = __str__

    def eat(self, what):
        if what.energy > self.canEatAtStep:
            self.energy += self.canEatAtStep
        elif what.energy > 0:
            self.energy += what.energy
        what.energy -= self.canEatAtStep

    def charForMap(self):
        return chr(ord('A') + int(self.energy/10))

def printmap():
    cls()
    for x in range(WorldW):
        s = ''
        for y in range(WorldH):
            s +=worldmap[x, y][-1].charForMap()
        print(s)

def worldStep():
    for x in range(WorldW):
        for y in range(WorldH):
            for o in worldmap[x,y]:
                o.step()

def worldSteps(n):
    for x in range(n):
        worldStep()
        clearDead()
    printmap()

def printObjects(objs):
    for o in objs:
        print(o.__class__.__name__, o)

def worldStepsView(n, p, e):
    """ Делает n шагов мира и показывает."""
    for x in range(n):
        worldStep()
        clearDead()
        printmap()
        printObjects(p+e)
        sleep(0.2)

def test():
    import random as r
    createWorld()
    p = [addObject(Person(), r.randint(0,10), r.randint(0,10)) for x in range(0,10)]
    e = [addObject(Eatable(), r.randint(0,10), r.randint(0,10)) for x in range(0,10)]

    #worldSteps(1)
    worldStepsView(100, p, e)
    a = Eatable()
    print(a, a.charForMap())
    a.step()
    print(a, a.charForMap())

test()
