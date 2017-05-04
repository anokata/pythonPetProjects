class Duck():
    
    def swim(self):
        print "swimimg"

    def display(self):
        """ abstract """
        pass

    def fly(self):
        self.fb.fly()

    def quack(self):
        self.qb.quack()

class FlyWithWings():
    def fly(self):
        print "wings fly"

class Quack():
    def quack(self):
        print "quack!"

class NormalDuck(Duck):

    def __init__(self):
        self.fb = FlyWithWings()
        self.qb = Quack()

    def display(self):
        print "normal duck"


d = NormalDuck()
d.display()
d.fly()
d.quack()
