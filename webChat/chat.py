from bottle import run, route, post, request, default_app
import auth
import chats
from urls import *
users = auth.Users()
users.add('adm', 'asm')
cht = chats.Chats()
#TODO: читать чат может только один из его пользователей авторизованный
# хранить пользователей, чаты
br = '<br>'
br = '\n'
@route(urlHist, method='POST')
def home():
    chat = request.forms.get('chat')
    return getHist(chat)

@route(urlPost, method='POST')
def chatPost():
    msg = request.forms.get('msg')
    user = request.forms.get('name')
    chat = request.forms.get('chat')
    r = addMsg(msg, user, chat)
    return r

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

@route(urlAuth, method='POST')
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
@route(urlGetChats, method='POST')
def webGetUsers():
    chats = cht.getchats()
    print(chats)
    return str(chats)




def addMsg(msg, userId, chatId):
    if users.authed(userId):
        cht.post(chatId, userId, msg) 
        return 'ok add msg'
    else:
        return 'no auth'

def getHist(chat): 
    h = cht.hist(chat)
    return h

def addUser(name, pswd):
    r = users.add(name, pswd)
    return 'User added' if r else 'User exist'

def authUser(name, pswd):
    r = users.auth(name, pswd)
    print(name, pswd, r)
    return r

def addChat(name, users):
    r = cht.add(name, users)
    return 'OK' if r else 'not'

if __name__=='__main__':
    run(host='localhost', port=7000, reloader=True)
    pass
    
applicationChat = default_app()

