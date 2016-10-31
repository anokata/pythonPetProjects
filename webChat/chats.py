import pickle
import os
import datetime
chatname = 'chats.cht'
class Chats():
    #chat = users, file, name
    chats = {} #name:..

    def __init__(self):
        self.chats = dict()
        self.load()

    def save(self):
        with open(chatname, 'wb') as fout:
            fout.write(pickle.dumps(self.chats))

    def load(self):
        if not os.path.exists(chatname):
            return False
        with open(chatname, 'rb') as fin:
            data = pickle.loads(fin.read())
            self.chats = data

    def add(self, name, users):
        if name not in self.chats:
            self.chats[name] = (users, self.genfilename(name, users))
            self.save()
            return True
        else:
            return False

    def genfilename(self, name, users):
        fn = 'cht_'
        fn += name 
        for u in users:
            fn += '_' + u
        return fn

    def adduser(self, chatname, user):
        pass

    def getchats(self):
        r = ''
        for c in self.chats.keys():
            r += c + '\n' #+ str(self.chats[c])
        return r

    def post(self, chatname, user, msg):
        #msg += '\n'
        #msg += user + '> ' # date TODO
        timestamp = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        msg = '\n' + timestamp + ' ' + user + '> ' + msg
        _, chatFile = self.chats[chatname]
        with open(chatFile, 'at') as fout:
            fout.write(msg)


    def hist(self, chatname):
        h = ''
        if chatname not in self.chats:
            return 'no such chat'
        _, chatFile = self.chats[chatname]
        if not os.path.exists(chatFile):
            return 'no chatfile'
        with open(chatFile, 'rt') as fin:
            for l in fin:
                h += l
        return h
                
                
                
                
                
                
                
                
