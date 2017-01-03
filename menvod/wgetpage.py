import urllib.request
from lxml import html
import requests
def ursl():
    url = "http://178.62.186.103/2016/"
    #o = urllib.urlopen
    z = urllib.request.urlopen(url)
    b = z.read()
    p = html.fromstring(b)
    u = p.xpath('//a')
    for link in u:
      print(url+link.get('href'))

def get_all_links(html, path='//a'):
    link_gen = html.xpath(path)
    for n, link in enumerate(link_gen):
        print(n, link.text, link.get('href'))


def rgoo():
    response = requests.get('http://google.com/search', {'q':'test'})
    page = html.fromstring(response.text)
    get_all_links(page, '//h3/a')
    #print(response.text)

response = requests.get('http://google.com/search', {'q':'test'})
page = html.fromstring(response.text)

rgoo()
