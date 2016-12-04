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

@route(get_all_url, method='GET')
def get_all():
    al = str()
    for k, v in st.items():
        al += (str(k) + ' : ' + str(v) + '\n<br>')
    return al

@route(get_books, method='GET')
def get_bks():
    al = str()
    for k, v in st.items():
        k = str(k)
        if k.startswith('book_'):
            try:
                al += (str(k).split('_', 1)[1] + ' : ' + str(v).split('_', 1)[1] + '\n<br>')
            except:
                pass
    return al

application_store = default_app()

if __name__=='__main__':
    run(host='localhost', port=8888, reloader=True)
    pass
