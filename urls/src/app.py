import os
from flask import Flask

app = Flask(__name__)
app.debug = True
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'urls.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='123',
    DEBUG=True,
))

from .views import *
