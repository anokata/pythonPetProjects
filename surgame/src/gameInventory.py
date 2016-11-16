import pygame
import inventory
import images
from util import Font
import util
#TODO отображение. переключение в него, управление.
class GInventory(inventory.Inventory):
    backgroundImg = images.inventoryBG 
    cellImg = images.cellImg 
    x = y = 10
    panx = pany = 10

    def __init__(self, screen):
        super().__init__()
        self.bg = util.imgLoad(self.backgroundImg)
        self.cell = util.imgLoad(self.cellImg)
        self.screen = screen

        self.bgRect = self.bg.get_rect()
        self.bgRect.left = self.x
        self.bgRect.top = self.y
        self.font = Font(22, (100, 255, 255))
        self.cellRect = self.cell.get_rect()

    #TODO
    def refactored_draw(self):
        self._draw_bg()
        w,h, *_ = self.getTabSize()
        for x in range(w):
            for y in range(h):
                self._draw_cell(x, y)

    def _draw_bg(self):
        self.screen.blit(self.bg, self.bgRect)

    def _draw_cell(self, x, y):
        self.screen.blit(self.cell, self._calc_cell_rect(x, y))
        pass



    def draw(self):
        self.screen.blit(self.bg, self.bgRect)
        w,h, *_ = self.getTabSize()
        tab = self.getTab()
        cellRect = self.cell.get_rect()
        cellRect.top = self.y + self.pany
        cellRect.left = self.x + self.panx
        for x in range(w):
            for y in range(h):
                cellRect.left = self.x + (self.panx + cellRect.width) * x + self.panx
                cellRect.top = self.y + (self.pany + cellRect.height) * y + self.pany
                self.screen.blit(self.cell, cellRect)
                index = y*w + x
                if index in tab:
                    obj = tab[y*w+x]
                    objw, objh = obj.image.get_rect().size
                    cellRect.left += (cellRect.width - objw)//2
                    cellRect.top += (cellRect.height - objh)//2
                    self.screen.blit(obj.image, cellRect)
                    # text count of objects
                    text = self.font.render(str(obj.count))
                    cellRect.left = self.x + (self.panx + cellRect.width) * x + self.panx*3
                    cellRect.top = self.y + (self.pany + cellRect.height) * y + self.pany*3
                    self.screen.blit(text, cellRect)
                    if y*w+x == self.getActiveIndex:
                        pass


