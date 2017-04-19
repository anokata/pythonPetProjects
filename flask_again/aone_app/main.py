from aone_app import app
import os
from .aone import *

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'aone.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='123',
    DEBUG=True,
))
