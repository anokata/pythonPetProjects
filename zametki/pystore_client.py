import requests as req
from pystore_urls import *
import optparse

p = optparse.OptionParser()
p.add_option('-s', default="")
options, arguments = p.parse_args()

def load(name):
    res = req.post(load_client, {'name': name})
    return res.text

def save(name, data):
    print(save_client)
    res = req.post(save_client, {'data':data, 'name':name})
    return res.text

if __name__=='__main__':
    #print(save('a', 'b'))
    print(load('a'))
    #print(load('xxx'))
