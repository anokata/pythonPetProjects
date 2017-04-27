from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware
from currency.currency.app import app as curapp
from urls.src.app import app as urlsapp
from werkzeug.serving import run_simple

application = Flask(__name__)

application = DispatcherMiddleware(application,
        { '/u' : urlsapp , 
         '/c' : curapp }, 
        )

run_simple('localhost', 5000, application, use_reloader=True)
