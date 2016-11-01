import pygame
from util import Font

class MenuList():
    items = []
    selected = 0

    def __init__(self, layer, id, x=20, y=10):
        self.layer = layer
        self.items = list()
        self.id = id
        self.rect = pygame.Rect(0,0,0,0)
        self.font = Font(32, (100, 100, 5), (180, 160, 100))
        self.selfont = Font(32, (180, 160, 30), (100, 80, 50))
        self.x = x
        self.y = y

    def rend(self):
        self.layer[self.id] = list()
        y = self.y
        for x in self.items:
            if self.items.index(x) == self.selected:
                t = self.selfont.render(x)
            else:
                t = self.font.render(x)
            self.rect = t.get_rect()
            self.rect.top = y
            self.rect.left = self.x
            y += self.font.h // 1.5
            self.layer[self.id].append((t, self.rect))

    def addItem(self, text):
        self.items.append(text)
        self.rend()

    def pred(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1
        self.rend()

    def next(self):
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0
        self.rend()


