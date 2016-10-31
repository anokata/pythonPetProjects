import clientCore as core
import tkinter as tk

class ChatDialog():

    def keyPress(self, k):
        if k.keycode == 1:
            exit()

    def __init__(self, root, username):
        self.root = root 
        self.username = username
        root.bind('<Key>', self.keyPress)
        root.bind('<Escape>', exit)
        frameMain=tk.Frame(root, bg='#DDD',bd=5)
        self.msgLabel = chatMsg = tk.Label(frameMain,anchor='nw', text='chat...->', bg="#EEE",
                width = 80, height = '30', font=("Helvetica", 10), justify='left')
        chatMsg['text'] = '_'
        self.usersListbox = usersList = tk.Listbox(frameMain)
        usersList.insert(tk.END, username)
        self.chatsListbox = chatsList = tk.Listbox(frameMain)
        #chatsList.insert(tk.END, )
        self.addUserBtn = tk.Button(frameMain, text='Добавить', width = 10, command=exit)
        self.delUserBtn = tk.Button(frameMain, text='Удалить', width = 10, command=exit)
        self.addChatBtn = tk.Button(frameMain, text='Создать', width = 10, command=exit)
        self.delChatBtn = tk.Button(frameMain, text='Удалить', width = 10, command=exit)
        userLab = tk.Label(frameMain, anchor='nw', text='Пользователи', bg="#EEE")
        chatLab = tk.Label(frameMain, anchor='nw', text='Беседы', bg="#EEE")

        frameMsg=tk.Frame(root, bg='#DEE',bd=5)
        self.statusLabel = tk.Label(frameMsg, anchor='nw', text='ok', bg="#EEE")
        self.msgBtn = tk.Button(frameMsg, text='Отправить', width = 10, command=exit)
        self.msgEdit = tk.Entry(frameMsg, width=20)
        self.msgEdit.insert(0, 'test msg')


        chatMsg.pack(side=tk.LEFT)
        userLab.pack(side=tk.TOP)
        usersList.pack(side=tk.TOP)
        self.addUserBtn.pack(side=tk.TOP)
        self.delUserBtn.pack(side=tk.TOP)
        chatLab.pack(side=tk.TOP)
        chatsList.pack(side=tk.TOP)
        self.addChatBtn.pack(side=tk.TOP)
        self.delChatBtn.pack(side=tk.TOP)
        frameMain.pack(side=tk.TOP)

        self.msgEdit.pack(side=tk.LEFT)
        self.msgBtn.pack(side=tk.LEFT)
        self.statusLabel.pack(side=tk.BOTTOM)
        frameMsg.pack(side=tk.BOTTOM)

        root.mainloop()

class LoginDialog():

    def keyPress(self, k):
        if k.keycode == 1:
            exit()
        if k.keycode == 36:
            self.auth()

    def __init__(self, root):
        self.root = root 
        root.bind('<Key>', self.keyPress)
        root.bind('<Escape>', exit)
        frameEdit=tk.Frame(root, bg='#DDD',bd=5)

        usernameAuth = self.name = tk.Entry(frameEdit, width=40)
        usernameAuth.insert(0, "a")
        userpassAuth = self.pasw = tk.Entry(frameEdit, width=20)
        userpassAuth.insert(0, 'a')
        self.authBtn = tk.Button(frameEdit, text='Войти', width = 10, command=self.auth)

        usernameAuth.pack(side=tk.LEFT)
        userpassAuth.pack(side=tk.LEFT)
        self.authBtn.pack(side=tk.LEFT)
        frameEdit.pack(side=tk.BOTTOM)

        usernameAuth.focus_set()
        root.mainloop()

    def auth(self):
        name = self.name.get()
        pswd = self.pasw.get()
        r = core.req(core.authUrl, {'name':name, 'pswd':pswd})
        print(r)
        if r == 'ok':
            self.result = name
            self.root.destroy()
            return r
        return r

if __name__=='__main__':
    #root = tk.Tk()
    #l = LoginDialog(root)
    #username = l.result
    username = 'a'
    #print(l.result)
    import time
    #time.sleep(1)
    ChatDialog(tk.Tk(), username)
    time.sleep(1)

