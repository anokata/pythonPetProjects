import urllib.request
from lxml import html
url = "http://178.62.186.103/2016/"
#o = urllib.urlopen
z = urllib.request.urlopen(url)
b = z.read()
p = html.fromstring(b)
u = p.xpath('//a')
for link in u:
  print(url+link.get('href'))
