import caveGenerate
import yaml

filename = 'data/cavegen.map'

def addObjects():
    o = list()
    o.append('floor')
    o.append('ground')
    o.append('apple')
    o.append('cherry')
    o.append('enemy_poringp')
    o.append('enemy_poringb')
    return o

def writeMap(fn, m):
    data = yaml.dump(m, default_flow_style=False)
    with open(fn, 'wt') as fout:
        print(data)
        fout.write(data)

def genMap():
    m = dict()
    genmap = caveGenerate.gen(50, 5)
    caveGenerate.addObjectsRandom(genmap, 'A', 16)
    caveGenerate.addObjectsRandom(genmap, 'C', 16)
    caveGenerate.addObjectsRandom(genmap, 'G', 16)
    caveGenerate.addObjectsRandom(genmap, 'B', 16)

    floor = caveGenerate.init_matrix(50, caveGenerate.FLOOR)
    map_str = caveGenerate.drawString(genmap)
    map_floor = caveGenerate.drawString(floor)
    m['layers_count'] = 2
    m['layers'] = list()
    m['layers'].append(map_floor)
    m['layers'].append(map_str)
    m['objects'] = addObjects()
    return m

if __name__ == '__main__':
    m = genMap()
    print(m)
    writeMap('../data/cavegen.yaml', m) 
