import util
import pygame
import math
import images

class Particles(util.Block):

    lifetime = 100

    def __init__(self, x, y, n=10, lifetime=10, imgname=images.particleDefault):
        super().__init__(x, y, imgname)
        self.particles_xyd = list() # координаты и скорости частицы (x, y, dx, dy)
        spd = 2
        self.lifetime = lifetime
        self.n = n
        for i in range(n):
            p = {'x': x, 'y': y}
            p['dx'] = spd * (math.cos(i*2*math.pi/n))
            p['dy'] = spd * (math.sin(i*2*math.pi/n))
            self.particles_xyd.append(p)


    def step(self):
        self.lifetime -= 1
        if self.lifetime:
            for p in self.particles_xyd:
                p['x'] += p['dx']
                p['y'] += p['dy']
            return True
        else:
            return False

    def draw(self, cam, screen):
        if self.lifetime:
            for p in self.particles_xyd:
                super().draw(p['x'], p['y'], cam, screen)

