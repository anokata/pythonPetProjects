from objectTypes import *
from collections import namedtuple

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

    def getEmptyCell(self, typ):
        w,h,max,count = self.sizes[typ]
        if max == count:
            return None
        self.sizes[typ] = (w,h,max,count+1)
        return count

    def getStored(self, obj):
        for n, x in self.categorys[obj.typ].items():
            if x.obj == obj:
                return x
        return False

    def add(self, obj):
        if obj.typ == FOOD:
            # find existed
            inventoryObj = self.getStored(obj)
            if not inventoryObj:
                cellIndex = self.getEmptyCell(FOOD)
                if cellIndex != None:
                    self.food[cellIndex] = obj.pack()
                    return True
            else:
                inventoryObj.add()
                return True
        return False
