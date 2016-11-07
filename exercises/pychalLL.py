from urllib import request

url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='
n = '12345'
n = '16044'
n = '82682'
#n = '8771'
#n = '72758'


for i in range(401):
    res = request.urlopen(url+n)
    t = res.read().decode('utf8')
    oldn = n
    try:
        n = (t[t.rfind('is ')+3:])
        n = str(int(n))
    except:
        n = oldn
        n = str(int(n) // 2)
    print(t , n)

