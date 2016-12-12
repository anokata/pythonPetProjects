
def open_door(door):
    if door.opened:
        door.opened = False
        door.passable= False
        door.char = door.close_char
        return 'Дверь закрыта'
    else:
        door.opened = True
        door.passable= True
        door.char = door.open_char
        return 'Дверь открыта'
