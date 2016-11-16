import caveGenerate

filename = 'data/cavegen.map'

def addObjects():
    o = ''
    o += 'floor\n'
    o += 'ground\n'
    return o

def writeMap(fn, m):
    with open(fn, 'wt') as fout:
        fout.write(m)

def genMap():
    m = ''
    map_str = caveGenerate.drawString(caveGenerate.m)
    map_floor = caveGenerate.drawString(caveGenerate.floor)
    m += '2\n'
    m += map_floor
    m += '\n'
    m += map_str
    m += '\n'
    m += addObjects()
    m += 'endObjectNames'
    m += '\n'
    return m

if __name__ == '__main__':
    m = genMap()
    print(m)
    writeMap('../data/cavegen.map', m) 
