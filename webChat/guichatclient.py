import tkinter as tk
import requests as rq
gethistUrl = 'http://localhost:7000/chat'
putmsgUrl = 'http://localhost:7000/chat/'
clearUrl =  'http://localhost:7000/chatclear'

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

main = tk.Tk()
def keyPress(k):
    if k.keycode == 1:
        exit()
main.bind('<Key>', keyPress)
main.bind('<Escape>', exit)

def sendmsg():
    try:
        res = rq.get(putmsgUrl + e.get())
    except:
        pass
    chatUpd()

def chatUpd():
    l['text'] = getHist()

e = tk.Entry(main)
e.insert(0, "defval")
#e.get()
b = tk.Button(main, text='Отправить...', width = 20, command=sendmsg)

exitButton = tk.Button(main, text='Выйти', width = 20, command=exit)
regetButton = tk.Button(main, text='Обновить', width = 20, command=chatUpd)
clearBut = tk.Button(main, text='!Очистить!', width = 20, command=clearhist)
b.pack()
exitButton.pack()
regetButton.pack()
clearBut.pack()

e.pack()
l = tk.Label(main, text='chat...->', width = 100, height = 300)
l['text'] = getHist()


l.pack()

e.focus_set()
main.mainloop()
