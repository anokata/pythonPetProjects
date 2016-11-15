import unittest
import inventory
import gameObjects
import objectTypes
import pygame

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inv = inv = inventory.Inventory()
        pygame.init()
        screen = pygame.display.set_mode((100,100))
        self.ob1 = ob1 = gameObjects.GObject('apple')
        inv.add(ob1)

    def testEat(self):
        f = self.inv.getFood()
        self.assertEqual(f.obj, self.ob1)
        self.inv.eat(f)
        f = self.inv.getFood()
        self.assertEqual(f, False)

        self.inv.add(self.ob1)
        f = self.inv.getFood()
        key = self.inv.getKey(f)
        self.assertEqual(key, 0)
        self.ob2 = gameObjects.GObject('apple')
        self.inv.add(self.ob2)
        f = self.inv.getFood()
        self.inv.eat(f)
        f = self.inv.getFood()
        self.inv.eat(f)
        f = self.inv.getFood()
        self.assertEqual(f, False)

        #print(self.inv.food)
        self.inv.add(self.ob2)
        self.inv.add(self.ob1)
        self.inv.add(self.ob1)
        self.inv.add(self.ob1)
        f = self.inv.getFood()
        self.inv.eat(f)
        f = self.inv.getFood()
        self.inv.eat(f)
        self.inv.eat(f)
        self.inv.add(self.ob1)
        f = self.inv.getFood()
        self.inv.eat(f)
        self.inv.eat(f)
        f = self.inv.getFood()
        self.assertEqual(f, False)

    def testGetKey(self):
        pass


if __name__=='__main__':
    unittest.main()
