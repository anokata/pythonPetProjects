def debugDecor(fn):
    """ Декоратор отладки. """
    def wrap(*args):
        print(args)
        return fn(*args)
    return wrap

def center_image(image):
    """ Центрирование якорной точки изображения. """
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def objDistance(s1, s2):
    """ расстояние между объектами. """
    return distance(s1.x, s1.y, s2.x, s2.y)

def distance(x, y, a, b):
    """ Вычисление расстояния между двумя точками. """
    from math import sqrt
    return sqrt((x-a)*(x-a) + (y-b)*(y-b))

def geomRange(start, count, coeff):
    """ Генератор геометрической прогрессии. """
    x = start
    c = 0
    while c < count:
        x = x * coeff
        c += 1
        yield int(x)
