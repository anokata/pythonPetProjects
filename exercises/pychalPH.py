import pickle
from urllib import request
url = 'http://www.pythonchallenge.com/pc/def/banner.p'
res = request.urlopen(url)
a = pickle.loads(res.read())
#a = pickle.load(open(fn, 'rb'))
print(a)
for elt in a:
    print( "".join([e[1] * e[0] for e in elt]))
