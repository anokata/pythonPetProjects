from flask import Flask
from src.app import app as app1

app = Flask(__name__)
app.register_blueprint(app1, url_prefix='/urlapp')

app.run()
