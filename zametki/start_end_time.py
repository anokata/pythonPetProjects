import os
import datetime
import optparse

log_file = 'start_end.log'
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
    logStart()

def dayEnd():
    logEnd()

if __name__=='__main__':
    #log('t_est')
    #logStart()
    print(getLog())
    
