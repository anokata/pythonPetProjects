import yaml
class AnObject():
    otype = 0
    objectsFilename = 'objects.gy'

    def __init__(self, typ):
        self.otype = typ

class Objects():

    def load(self):
        objDict = yaml.load(open(self.objectsFilename))

