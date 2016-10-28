from bottle import run, route, post, request
import auth
import chats
urlChatAdd = '/chat/add'
users = auth.Users()
users.add('adm', 'asm')
cht = chats.Chats()

#chatFile = 'chat.txt'
br = '<br>'
br = '\n'
@route('/chat')
def home():
    return getHist()

@route('/chat/<msg>')
def chatMsg(msg):
    addMsg(msg)
    return getHist()

@route('/chat/post', method='POST')
def chatPost():
    msg = request.forms.get('msg')
    user = request.forms.get('user')
    chat = request.forms.get('chat')
    addMsg(msg, user, chat)
    return getHist()

@route('/chatclear') # TODO
def chatClear():
    with open(chatFile, 'wt') as f:
        pass
    return ''

@route('/chat/adduser', method='POST')
def webAddUser():
    name = request.forms.get('name')
    pswd = request.forms.get('pswd')
    res = addUser(name, pswd)
    return res

@route('/chat/auth', method='POST')
def webAddUser():
    name = request.forms.get('name')
    pswd = request.forms.get('pswd')
    res = authUser(name, pswd)
    return res

@route(urlChatAdd, method='POST')
def webAddChat():
    name = request.forms.get('name')
    users = request.forms.get('users')
    users = users.split()
    res = addChat(name, users)
    return res





def addMsg(msg, userId, chatId):
    if users.authed(userId):
        cht.post(chatId, userId, msg) 

def getHist(chat): 
    return cht.hist(chat)

def addUser(name, pswd):
    r = users.add(name, pswd)
    return 'User added' if r else 'User exist'

def authUser(name, pswd):
    r = users.auth(name, pswd)
    return 'OK' if r else 'do not login'

def addChat(name, users):
    r = cht.add(name, users)
    return 'OK' if r else 'not'


run(host='localhost', port=7000, reloader=True)
