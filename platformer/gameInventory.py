import pygame
import inventory
#TODO отображение. переключение в него, управление.
class GInventory(inventory.Inventory):
    backgroundImg = 'objects/inventoryBG.png'
    cellImg = 'objects/inventoryCell.png'
    x = y = 10
    panx = pany = 10

    def __init__(self, screen):
        super().__init__()
        self.bg = pygame.image.load(self.backgroundImg)
        self.cell = pygame.image.load(self.cellImg)
        self.screen = screen

        self.bgRect = self.bg.get_rect()
        self.bgRect.left = self.x
        self.bgRect.top = self.y

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

