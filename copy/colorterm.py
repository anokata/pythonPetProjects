fred = 31
fgreen = 32
fyellow =33
fblue = 34
fpurpl = 35
fcyan = 36
fwhite = 37
styleEnd = '\x1b[0m'

def ctextB(text, f):
  print('\x1b[1;' + str(f) + ';40m' + text + styleEnd)
def ctext(text, f):
  print('\x1b[0;' + str(f) + ';40m' + text + styleEnd)

def gtextB(text, f):
  return '\x1b[1;' + str(f) + ';40m' + text + styleEnd
def gtext(text, f):
  return '\x1b[0;' + str(f) + ';40m' + text + styleEnd

#get str
def gtextbr(t):
  return gtextB(t, fred)
def gtextbg(t):
  return gtextB(t, fgreen)
def gtextby(t):
  return gtextB(t, fyellow)
def gtextbb(t):
  return gtextB(t, fblue)
def gtextbp(t):
  return gtextB(t, fpurpl)
def gtextbc(t):
  return gtextB(t, fcyan)
def gtextbw(t):
  return gtextB(t, fwhite)

def gtextr(t):
  return gtext(t, fred)
def gtextg(t):
  return gtext(t, fgreen)
def gtexty(t):
  return gtext(t, fyellow)
def gtextb(t):
  return gtext(t, fblue)
def gtextp(t):
  return gtext(t, fpurpl)
def gtextc(t):
  return gtext(t, fcyan)
def gtextw(t):
  return gtext(t, fwhite)

#print
def ctextbr(t):
  ctextB(t, fred)
def ctextbg(t):
  ctextB(t, fgreen)
def ctextby(t):
  ctextB(t, fyellow)
def ctextbb(t):
  ctextB(t, fblue)
def ctextbp(t):
  ctextB(t, fpurpl)
def ctextbc(t):
  ctextB(t, fcyan)
def ctextbw(t):
  ctextB(t, fwhite)

def ctextr(t):
  ctext(t, fred)
def ctextg(t):
  ctext(t, fgreen)
def ctexty(t):
  ctext(t, fyellow)
def ctextb(t):
  ctext(t, fblue)
def ctextp(t):
  ctext(t, fpurpl)
def ctextc(t):
  ctext(t, fcyan)
def ctextw(t):
  ctext(t, fwhite)
