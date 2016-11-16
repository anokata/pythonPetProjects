import sys
from os.path import join

rootPath = '../'
def getPath(path):
    return join(rootPath, path)

def getPaths(pathList):
    return list(map(getPath, pathList))

def extendSysPath():
    sys.path += [getPath("lib"),'./']

extendSysPath()
