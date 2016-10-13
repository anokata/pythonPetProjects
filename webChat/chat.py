from bottle import run, route

chatFile = 'chat.txt'
br = '<br>'
@route('/chat')
def home():
    return getHist()

@route('/chat/<msg>')
def chatMsg(msg):
    addMsg(msg)
    return getHist()

def addMsg(msg):
    msg += '\n'
    with open(chatFile, 'at') as fout:
        fout.write(msg)
        
def getHist():
    h = ''
    with open(chatFile, 'rt') as fin:
        for l in fin:
            h += l + br
    return h


run(host='localhost', port=7000, reloader=True)
