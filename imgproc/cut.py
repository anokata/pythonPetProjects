from PIL import Image
from sys import argv

def fngen(i,j, fn, fe):
    return fn + '_' + str(i) + '_' + str(j) + fe

def crop(w=20, h=30, wn=1, hn=3, fn='', fe=''):
    fn = 'princess'
    fe = '.png'
    filen = fn + fe
    img = Image.open(filen)
    for i in range(wn):
        for j in range(hn):
            x = i * w
            y = j * h
            a = x + w
            b = y + h
            print(x,y,a,b)
            croped = img.crop((x, y, a, b))
            print(fngen(j,i,fn,fe))
            croped.save(fngen(j,i, fn, fe), "PNG")
            #croped.show()

if __name__ == '__main__':
    if len(argv) < 5:
        print('call cut w h wn hn file')
        exit(0)
    w = int(argv[1])
    h = int(argv[2])
    wn = int(argv[3])
    hn = int(argv[4])
    fn = (argv[5])
    print(fn, w, h, wn, hn)
    crop(w, h, wn, hn, fn, '.png')
