from objectTypes import *
from collections import namedtuple, defaultdict

Size = namedtuple("InventorySize", "w,h,len,current")

class Inventory():
    food = {} # (x,y) in cell  = obj/ not (x) in cell = obj а потом преобразуем в коорд x y
    sizes = {} # nameCategory : w, h, w*h, current
    activeCategory = FOOD
    categorys = {}

    def __init__(self):
        self.food = dict()
        self.sizes = dict()
        self.sizes[FOOD] = Size(2,2,2*2,0) #(2,2, 2*2, 0)
        self.categorys = dict()
        self.categorys[FOOD] = self.food

    def getActiveIndex(self):
        return self.sizes[self.activeCategory].current

    def next(self):
        cat = self.sizes[self.activeCategory] 
        cat = cat._replace(current=cat.current+1)

    def getTab(self):
        return self.categorys[self.activeCategory]
    def getTabSize(self):
        return self.sizes[self.activeCategory]

    def takeEmptyCell(self, typ):
        w,h,max,count = self.sizes[typ]
        if max == count:
            return None
        self.sizes[typ] = (w,h,max,count+1)
        for x in range(max):
            isBusy = self.categorys[typ].get(x, False)
            if not isBusy:
                break
        if isBusy:
            return None
        return x

    def getStored(self, obj):
        for n, x in self.categorys[obj.typ].items():
            if x and x == obj:
                return x
        return False

    def getFood(self):
        w, h, max, count = self.sizes[FOOD]
        if count != 0:
            for x in range(max):
                food = self.food.get(x, False)
                if food:
                    break
            return food
        return False

    
    def eat(self, food):
        hpGain = food.baseObject.hpGain
        self.drop(food)
        return hpGain

    def drop(self, obj):
        key = self.getKey(obj)
        foodPack = self.categorys[obj.typ].get(key)
        if foodPack.count > 1:
            foodPack.eatOne()
        else:
            self.categorys[obj.typ].pop(key)
            w, h, max, count = self.sizes[obj.typ]
            self.sizes[obj.typ] = Size(w, h, max, count-1)

    def getKey(self, obj):
        cat = self.categorys[obj.typ]
        return list(cat.keys())[list(cat.values()).index(obj)]


    def add(self, obj):
        if obj.typ == FOOD:
            # find existed
            inventoryObj = self.getStored(obj)
            if not inventoryObj:
                cellIndex = self.takeEmptyCell(FOOD)
                if cellIndex != None:
                    self.food[cellIndex] = obj
                    return True
            else:
                inventoryObj.add()
                return True
        return False
