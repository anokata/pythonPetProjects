#TODO namedtuple
class Users():
    users = {} # name:(passhash, id)
    lastId = 0
    authorized = []
    
    def __init__(self):
        self.users = dict()
        self.authorized = list()
        self.load()

    def add(self, name, pswd):
        if name not in self.users:
            self.users[name] = (pswd, self.lastId)
            self.lastId += 1
            self.save()
            return True
        else:
            return False

    def setpass(self, name, paswd):
        if name in self.users:
            _,uid = self.users[name]
            self.users[name] = (pswd, uid)
            self.save()
        else:
            return False

    def delete(self, name):
        if name in self.users:
            del self.users[name]
            self.save()
    
    def getusers(self):
        return users.keys()

    def get(self, name):
        if name in self.users:
            return self.users[name]

    def auth(self, name, pswd):
        if name in self.users:
            spswd = self.users[name]
            ais = spswd == pswd
            if ais:
                self.authorized.append(name)
            return ais

    def authed(self, name):
        return name in self.authorized

    def load(self):
        pass
    def save(self):
        pass

