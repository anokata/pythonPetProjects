from bottle import run, route, post, request, default_app
from pystore_urls import *
import pickle
import os

st = dict()
pickle_file = 'db.pkl'

if not os.path.exists(pickle_file):
    pickle.dump(st, open(pickle_file, 'wb'))

st = pickle.load(open(pickle_file, 'rb'))

@route(save, method='POST')
def store():
    data = request.forms.get('data')
    name = request.forms.get('name')
    st[name] = data
    pickle.dump(st, open(pickle_file, 'wb'))
    return 'ok store ' + name

@route(load, method='POST')
def get():
    name = request.forms.get('name')
    try:
        res = st[name]
    except:
        res = 'no'
    return res

application = default_app()

if __name__=='__main__':
    run(host='localhost', port=8888, reloader=True)
    pass
