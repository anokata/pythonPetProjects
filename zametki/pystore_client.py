#!/usr/bin/python3
import requests as req
from pystore_urls import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command', help='one of: load, save')
parser.add_argument('-n', help='name of value')
args = parser.parse_args()
#print(args.command, args.n)

def load(name):
    res = req.post(load_client, {'name': name})
    return res.text

def get_all():
    res = req.get(get_all_client)
    return res.text

def save(name, data):
    #print(save_client)
    res = req.post(save_client, {'data':data, 'name':name})
    return res.text

if __name__=='__main__':
    #print(save('a', 'b'))
    #print(load('a'))
    if args.command == 'load' and args.n != None:
        print(load(args.n))
        exit()
    if args.command == 'save' and args.n != None:
        data = input()
        save(args.n, data)
        exit()
    if args.command == 'all':
        print(get_all())
        exit()
