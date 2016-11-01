from objectTypes import *
class Inventory():
    food = {} # (x,y) in cell  = obj/ not (x) in cell = obj а потом преобразуем в коорд x y
    sizes = {} # nameCategory : w, h, w*h, current
    activeCategory = FOOD
    categorys = {}

    def __init__(self):
        self.food = dict()
        self.sizes = dict()
        self.sizes[FOOD] = (2,2, 2*2, 0)
        self.categorys = dict()
        self.categorys[FOOD] = self.food

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

    def add(self, obj):
        if obj.typ == FOOD:
            # find existed

            cellIndex = self.getEmptyCell(FOOD)
            if cellIndex != None:
                self.food[cellIndex] = obj
                return True
        return False
