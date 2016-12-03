from bottle import run, route, post, request, default_app
from pystore_urls import *

@route(save, method='POST')
def store():
    data = request.forms.get('data')
    name = request.forms.get('name')
    #save
    return 'ok store' + data + name

@route(load, method='POST')
def get():
    return 'ok get'

application = default_app()

if __name__=='__main__':
    run(host='localhost', port=8888, reloader=True)
    pass
