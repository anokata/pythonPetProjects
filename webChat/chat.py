from bottle import run, route, post, request
import auth
import chats
from urls import *
users = auth.Users()
users.add('adm', 'asm')
cht = chats.Chats()

#chatFile = 'chat.txt'
br = '<br>'
br = '\n'
@route('/chat', method='POST')
def home():
    chat = request.forms.get('chat')
    return getHist(chat)

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

@route(urlUserAdd, method='POST')
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

@route(urlGetUsers, method='POST')
def webGetUsers():
    usrs = users.getusers()
    print(usrs)
    return str(usrs)




def addMsg(msg, userId, chatId):
    if users.authed(userId):
        cht.post(chatId, userId, msg) 

def getHist(chat): 
    try:
        h = cht.hist(chat)
    except:
        h = 'no chat'
    return h

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
