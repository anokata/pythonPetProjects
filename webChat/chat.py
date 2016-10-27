from bottle import run, route, post, request

chatFile = 'chat.txt'
br = '<br>'
br = '\n'
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

@route('/chat/post', method='POST')
def chatPost():
    msg = request.forms.get('msg')
    addMsg(msg)
    return getHist()


run(host='localhost', port=7000, reloader=True)
