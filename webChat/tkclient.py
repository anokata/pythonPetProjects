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


        chatMsg.pack(side=tk.LEFT)
        usersList.pack(side=tk.TOP)
        chatsList.pack(side=tk.TOP)
        frameMain.pack(side=tk.TOP)


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

