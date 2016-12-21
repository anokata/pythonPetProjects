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
parser.add_argument('--command', help='one of: load, save, book, all, books')
parser.add_argument('-n', help='name of value')
parser.add_argument('-s', help='script mode')
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
def exec_cmd(command, name):
    cmd = cmds.get(command, False)
    if cmd:
        cmd(name)
    else:
        print('no that cmd')

def menu():
    print('Avaliable commands')
    for k in cmds.keys():
        print(k, end=',')
    print('\n')
    command = ''
    while command not in cmds.keys():
        command = input('Enter command:')
        cmd = cmds.get(command, False)
        if cmd:
            cmd(None)
        else:
            print('no that cmd')

if __name__=='__main__':
    if args.s:
        exec_cmd(args.command, args.n)
    else:
        menu()
