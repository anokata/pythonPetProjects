#!/usr/bin/python3
import requests as req
import sys
import os
work_dir = sys.path[0]
lib_dir = os.path.join(work_dir, './lib')
sys.path.append(lib_dir)
from pystore_urls import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command', help='one of: load, save')
parser.add_argument('-n', help='name of value')
args = parser.parse_args()

def load(name):
    res = req.post(load_client, {'name': name})
    return res.text

def get_all():
    res = req.get(get_all_client)
    return res.text

def get_books():
    res = req.get(get_books_client)
    return res.text

def save(name, data):
    res = req.post(save_client, {'data':data, 'name':name})
    return res.text

def book(name, page):
    save('book_'+name, 'page_'+page)

def save_cmd(name):
    if name == None:
        name = input('enter name:')
    data = input('enter data:')
    save(name, data)

def load_cmd(name):
    if name == None:
        name = input('enter name:')
    print(load(name))

def all_cmd(_):
    print(get_all())

def books_cmd(_):
    print(get_books())

def book_cmd(name):
    if name == None:
        name = input('enter name:')
    page = input('enter page:')
    book(name, page)

if __name__=='__main__':
    cmds = {
            'save': save_cmd,
            's': save_cmd,
            'store': save_cmd,
            'set': save_cmd,
            'l': load_cmd,
            'load': load_cmd,
            'get': load_cmd,
            'g': load_cmd,
            'all':all_cmd,
            'a':all_cmd,
            'books':books_cmd,
            'bs':books_cmd,
            'b':book_cmd,
            'book':book_cmd,
            }
    cmd = cmds.get(args.command, False)
    if cmd:
        cmd(args.n)
    else:
        print('no that cmd')
