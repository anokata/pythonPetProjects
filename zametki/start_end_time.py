import os
import datetime
import optparse

log_file = 'start_end.log'
lock_file = '/var/lock/pycuslockfile_for_onestart'
io = 0

def getLog() -> io : # IO<
    if not os.path.exists(log_file):
        with open(log_file, 'wt') as fout:
            fout.write('')

    with open(log_file, 'rt') as fin:
        return fin.read()

def log(string) -> io : # IO>
    with open(log_file, 'at') as fout:
        fout.write(string)
        fout.write('\n')

def getDate() -> io : # IO<
    return datetime.datetime.now().isoformat()

def logStart() -> io : # IO<>
    log('start at: ' + getDate())

def logEnd() -> io : # IO<>
    log('end at: ' + getDate())

def dayStart():
    if lock():
        logStart()

def dayEnd():
    if freeLock():
        logEnd()

def isLock():
    return os.path.exists(lock_file)

def lock():
    if not isLock():
        with open(lock_file, 'w') as f:
            f.write('')
            return True
    else:
        return False

def freeLock():
    if isLock():
        os.remove(lock_file)
        return True
    else:
        return False

if __name__=='__main__':
    dayStart()
    dayEnd()
    print(getLog())
    
