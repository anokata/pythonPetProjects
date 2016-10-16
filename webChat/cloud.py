#import urllib
import requests as req
ur1 = 'https://api.github.com/users/anokata'
res = req.get(ur1)
ur2 = ur1 + '/repos'
#print(res.text)

res = req.get(ur2)
#print(res.text)
rj = res.json()
for x in rj:
    name = x['name']
    print(name)
#print(res.json())
