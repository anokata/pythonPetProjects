import random
import tkinter as tk
import requests as rq
from urls import *
host = 'http://anokata.pythonanywhere.com/'
host = 'http://localhost:7000/'
gethistUrl = host + 'chat'
clearUrl =  host + 'chatclear'
postUrl = host + 'chat/post'
userAddUrl = host[:-1] + urlUserAdd
getUsersUrl = host[:-1] + urlGetUsers
#TODO: читать периодически. переделать на другом гуй.
# auth, chat create, user add, list all users & chats
def req(url, param={}):
    h = None
    try:
        res = rq.post(url, param)
        h = res.text
    except:
        pass
    return h

def getHist():
    return req(gethistUrl)

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
    try:
        msg = usernameEntry.get() + '|- ' + userMsg.get()
        r = req(postUrl, {'msg': msg})
    except:
        pass
    chatUpd()

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

random.seed()
root = main
frameHist=tk.Frame(root,bg='#DDD',bd=5)
frameInp=tk.Frame(root,bg='#BBB',bd=5)
frame3=tk.Frame(root,bg='#CCC',bd=5)
frameUser=tk.Frame(root,bg='#FAC',bd=5)

userMsg = tk.Entry(frameInp, width=40)
userMsg.insert(0, "defval")
usernameEntry = tk.Entry(frameInp, width=20)
usernameEntry.insert(0, 'userN' + str(random.randint(500, 1000)))

sendBtn = tk.Button(frameInp, text='Отправить...', width = 20, command=sendmsg)
exitButton = tk.Button(frame3, text='Выйти', width = 20, command=exit)
regetButton = tk.Button(frame3, text='Обновить', width = 20, command=chatUpd)
clearBut = tk.Button(frame3, text='!Очистить!', width = 10, command=clearhist)

chatMsg = tk.Label(frameHist,anchor='nw', text='chat...->', bg="#EEE",
        width = 100, height = '30', font=("Helvetica", 10), justify='left')
chatMsg['text'] = getHist()


usernameAuth = tk.Entry(frameUser, width=40)
usernameAuth.insert(0, "name1")
userpassAuth = tk.Entry(frameUser, width=20)
userpassAuth.insert(0, '****' + str(random.randint(500, 1000)))
adduserBtn = tk.Button(frameUser, text='добавить', width = 10, command=adduser)
authBtn = tk.Button(frameUser, text='Войти', width = 10, command=exit)
usersBtn = tk.Button(frame3, text='USERS', width = 10, command=getusers)

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
frameHist.pack(side=tk.TOP, expand=True,fill='both')
frame3.pack(side=tk.BOTTOM)
frameUser.pack(side=tk.BOTTOM)
frameInp.pack(side=tk.BOTTOM)

userMsg.focus_set()
main.mainloop()
