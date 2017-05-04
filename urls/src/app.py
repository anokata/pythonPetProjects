import os
#from flask import Flask
from flask import Blueprint

app = Blueprint("urls", __name__, 
        template_folder='templates',
        static_folder='static')

#app = Flask(__name__)
app.debug = True
app.config = {}
app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'urls.db'),
    DATABASE='urls.db',
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='123',
    DEBUG=True,
))

from .views import *
