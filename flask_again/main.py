from flask import Flask
import os

app = Flask("aone")

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'aone.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='123',
    DEBUG=True,
))
