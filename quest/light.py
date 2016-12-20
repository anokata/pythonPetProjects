import math

def _gen_ray(alpha, R):
    r = 0.5
    while r <= R:
        x, y = math.cos(math.radians(alpha))*r, math.sin(math.radians(alpha))*r
        r += 0.5
        yield int(x), int(y)

def get_ray(alpha, R):
    ray = list(_gen_ray(alpha, R))
    sray = list()
    for r in ray:
        if r not in sray:
            sray.append(r)
    return sray

def get_circle_rays(R): #TODO static calc
    rays = list()
    for alpha in range(0, 370, 10):
        rays.append(get_ray(alpha, R))
    return rays

