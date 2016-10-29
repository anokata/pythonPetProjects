import random
import tkinter as tk
import requests as rq
from urls import *
host = 'http://anokata.pythonanywhere.com/'
host = 'http://localhost:7000/'
gethistUrl = host[:-1] + urlHist
clearUrl =  host + 'chatclear'
postUrl = host[:-1] + urlPost
userAddUrl = host[:-1] + urlUserAdd
getUsersUrl = host[:-1] + urlGetUsers
chatAddUrl = host[:-1] + urlChatAdd
getChatsUrl = host[:-1] + urlGetChats
authUrl = host[:-1] + urlAuth
#TODO: читать периодически. переделать на другом гуй.
# auth, chat create, user add, list all users & chats
#TODO: сделать удобный клиент для пользователя и отладочный отдельно (или режим отладки, сообщений окно, и команд)
def req(url, param={}):
    h = None
    try:
        res = rq.post(url, param)
        h = res.text
    except:
        pass
    return h


def clearhist():
    req(clearUrl)
    chatUpd()

main = tk.Tk()
def keyPress(k):
    if k.keycode == 1:
        exit()
main.bind('<Key>', keyPress)
main.bind('<Escape>', exit)

def sendmsg():
    r = ''
    try:
        msg = userMsg.get()
        name = usernameEntry.get()
        chat = chatInput.get()
        r = req(postUrl, {'msg': msg, 'name':name, 'chat':chat})
    except:
        pass
    #chatUpd()
    viewtext(r)

def getHist():
    chat = chatInput.get()
    print(chat)
    return req(gethistUrl, {'chat':chat})

def chatUpd():
    chatMsg['text'] = getHist()

def viewtext(t):
    chatMsg['text'] = t

def adduser():
    name = usernameAuth.get()
    pswd = userpassAuth.get()
    r = req(userAddUrl, {'name':name, 'pswd':pswd})
    viewtext(r)

def getusers():
    viewtext(req(getUsersUrl))
def getchats():
    viewtext(req(getChatsUrl))

def chatAdd():
    name = chatInput.get()
    r = req(chatAddUrl, {'name':name, 'users':''})
    viewtext(r)

def auth():
    name = usernameAuth.get()
    pswd = userpassAuth.get()
    r = req(authUrl, {'name':name, 'pswd':pswd})
    viewtext(r)

random.seed()
root = main
frameHist=tk.Frame(root,bg='#DDD',bd=5)
frameInp=tk.Frame(root,bg='#BBB',bd=5)
frame3=tk.Frame(root,bg='#CCC',bd=5)
frameUser=tk.Frame(root,bg='#FAC',bd=5)
frameChat=tk.Frame(root,bg='#ACF',bd=5)

userMsg = tk.Entry(frameInp, width=40)
userMsg.insert(0, "defval")
usernameEntry = tk.Entry(frameInp, width=20)
usernameEntry.insert(0, 'name1')

sendBtn = tk.Button(frameInp, text='Отправить...', width = 20, command=sendmsg)
exitButton = tk.Button(frame3, text='Выйти', width = 20, command=exit)
regetButton = tk.Button(frame3, text='Обновить', width = 20, command=chatUpd)
clearBut = tk.Button(frame3, text='!Очистить!', width = 10, command=clearhist)

chatMsg = tk.Label(frameHist,anchor='nw', text='chat...->', bg="#EEE",
        width = 100, height = '30', font=("Helvetica", 10), justify='left')
chatMsg['text'] = '_'

usernameAuth = tk.Entry(frameUser, width=40)
usernameAuth.insert(0, "name1")
userpassAuth = tk.Entry(frameUser, width=20)
userpassAuth.insert(0, '****' + str(random.randint(500, 1000)))
adduserBtn = tk.Button(frameUser, text='добавить', width = 10, command=adduser)
authBtn = tk.Button(frameUser, text='Войти', width = 10, command=auth)
usersBtn = tk.Button(frame3, text='USERS', width = 10, command=getusers)
chatInput = tk.Entry(frameChat, width=40)
chatInput.insert(0, "chatname1")
chatBtn = tk.Button(frameChat, text='Добавить чат', width = 10, command=chatAdd)
chatsBtn = tk.Button(frameChat, text='CHATS', width = 10, command=getchats)

usernameEntry.pack(side=tk.LEFT)
userMsg.pack(side=tk.LEFT)
sendBtn.pack(side=tk.LEFT)
exitButton.pack(side=tk.LEFT)
regetButton.pack(side=tk.LEFT)
clearBut.pack(side=tk.LEFT)
chatMsg.pack(side=tk.LEFT)
usernameAuth.pack(side=tk.LEFT)
userpassAuth.pack(side=tk.LEFT)
adduserBtn.pack(side=tk.LEFT)
authBtn.pack(side=tk.LEFT)
usersBtn.pack(side=tk.LEFT)
chatInput.pack(side=tk.LEFT)
chatBtn.pack(side=tk.LEFT)
chatsBtn.pack(side=tk.LEFT)
frameHist.pack(side=tk.TOP, expand=True,fill='both')
frame3.pack(side=tk.BOTTOM)
frameUser.pack(side=tk.BOTTOM)
frameChat.pack(side=tk.BOTTOM)
frameInp.pack(side=tk.BOTTOM)

userMsg.focus_set()
main.mainloop()
