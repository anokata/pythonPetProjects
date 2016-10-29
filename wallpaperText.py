#!/usr/bin/python3
import subprocess
exc = subprocess.getoutput
from sys import argv
from PIL import Image, ImageDraw, ImageFont
# прога для рисования на изображении текста(из файла, статус системы...) и отображения его на фон, периодически
# args = periodic(secs?) textfile/syscmd to exec, bgimg file, fontcolor
# args img, 
W = 1280
H = 1024
fn = 'wallpaperText.py'
# создать имг или загрузить фон.
fontPath = "/usr/share/fonts/truetype/dejavu/"
f1 = 'DejaVuSansMono.ttf'
f2 = "DejaVuSans.ttf"
fontPath += f1
#fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
fnt = ImageFont.truetype(fontPath, 20)
# нанести текст(файла)
if len(argv)>1:
    imgpath = argv[1]
    txt = Image.open(imgpath)
else:
    txt = Image.new('RGB', (W, H), (0,0,0))
#print(txt, fnt)
d = ImageDraw.Draw(txt)
#d.text((10,10), "Hello", font=fnt, fill=(255,255,255))
text = ''
with open(fn, 'rt') as fin:
    text = ''.join(fin.readlines())
d.multiline_text((20,10), text, fill=None, font=fnt, anchor=None, spacing=5, align="left")
#txt.show()
# сохранить в файл
imgfn = 'walltext.png' 
txt.save(imgfn, 'PNG')
# сделать фоном
exc('qiv -z ' + imgfn)
