import caveGenerate

filename = 'data/cavegen.map'
map_str = caveGenerate.drawString(caveGenerate.m)

def write_objects(f):
    f.write('floor\n')
    f.write('ground\n')

with open(filename, 'wt') as fout:
        fout.write('1\n')
        fout.write(map_str)
        fout.write('\n')
        write_objects(fout)
        fout.write('endObjectNames')
        fout.write('\n')
