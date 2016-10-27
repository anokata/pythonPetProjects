import random
import tkinter as tk
import requests as rq
host = 'http://anokata.pythonanywhere.com/'
host = 'http://localhost:7000/'
gethistUrl = host + 'chat'
clearUrl =  host + 'chatclear'
postUrl = host + 'chat/post'
#TODO: читать периодически. переделать на другом гуй.

def req(url):
    h = None
    try:
        res = rq.get(url)
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
        rq.post(postUrl, {'msg': msg})
    except:
        pass
    chatUpd()

def chatUpd():
    chatMsg['text'] = getHist()

random.seed()
root = main
frameHist=tk.Frame(root,bg='#DDD',bd=5)
frameInp=tk.Frame(root,bg='#BBB',bd=5)
frame3=tk.Frame(root,bg='#CCC',bd=5)

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

usernameEntry.pack(side=tk.LEFT)
userMsg.pack(side=tk.LEFT)
sendBtn.pack(side=tk.LEFT)
exitButton.pack(side=tk.LEFT)
regetButton.pack(side=tk.LEFT)
clearBut.pack(side=tk.LEFT)
chatMsg.pack(side=tk.LEFT)
frameHist.pack(side=tk.TOP, expand=True,fill='both')
frame3.pack(side=tk.BOTTOM)
frameInp.pack(side=tk.BOTTOM)

userMsg.focus_set()
main.mainloop()
