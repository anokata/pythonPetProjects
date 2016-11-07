import re
import codecs
with open('/home/ksi/pyurl3.txt', 'rt') as fin:
    inp = fin.read()
    inp2 = re.findall('[^A-Z]+[A-Z]{3}([a-z])[A-Z]{3}[^A-Z]+', inp)
    inp3 = re.findall('[A-Z][A-Z][A-Z][a-z][A-Z][A-Z][A-Z]', inp)
    print(len(inp), len(inp2))
    msg = ''.join(inp2)
    print(msg)
    a = ''.join([chr(x) for x in range(ord('a'), ord('z')+1)])
    b = ''.join([chr(x) for x in range(ord('a')+2, ord('z')+1)] + ['a','b'])
    tr = str.maketrans(a,b)

    print(codecs.decode(msg, 'rot-13'))
    print(str.translate(msg, tr))
    print(inp3)
    inp4 = ''
    for k in inp3:
        if k[0] == k[1] == k[2]:
                inp4 += k[3]
                print(k)
    print(inp4)

