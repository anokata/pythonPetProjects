#!/usr/bin/python3
# Подсчёт строк кода. игнорируя пустые строки и комментарии. средняя длинна строки кода, количество коментов, кол-во символов.
import os
import glob

def getlines(fn):
    """ Получает содержимое файла как список строк """
    lines = list()
    with open(fn, 'rt') as fin:
       lines = fin.readlines()
    return lines

pwd = os.path.abspath(os.curdir)
print('Search in {}'.format(pwd))
# Получим список всех файлов 
files = glob.glob('**', recursive=True)
# Отфильтруем только питоновские
files = list(filter(lambda n: n.endswith('.py'), files))
fileCount = len(files)
# Получим их содержимое
contents = list()
for fn in files:
    contents += getlines(fn)

# Отфильтруем пустые и комментарии. И вычислим общую длинну.
chars = 0
comments = 0
emptylines = 0
codelines = list()
for l in contents:
    l = l.strip()
    if l == '':
        emptylines += 1
        continue
    if l[0] == '#':
        comments += 1
        continue
    
    chars += len(l)
    codelines.append(l)

LOC = len(codelines)
print('Строк кода (LOC):', LOC)
print('Символов всего:', chars)
print('Средняя длинна строки кода:', int(chars/LOC), 'символов')
print('Комментариев строк:', comments)
print('Пустых строк:', emptylines)
print('Всего файлов:', fileCount)
print('Средняя длинна файла:', int(LOC/fileCount), 'строк')


import random
#print(random.choice(codelines))
