import requests as req
from pystore_urls import *

def load(name):
    res = req.get(load_client + name)
    return res.text

def save(name, data):
    res = req.post(save_client, {'data':data, 'name':name})
    return res.text

if __name__=='__main__':
    print(save('a', 'b'))
