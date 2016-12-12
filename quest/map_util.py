
def object_at(x, y, objects): # Выделить точку, и карту с объктами вместе
    for o in objects:
        if o.x == x and o.y == y:
            return o
    return False

def can_be_there(x, y, amap, objects):
    obj = object_at(x, y, objects)
    if not obj:
        return True
    return obj.passable
