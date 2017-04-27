from flask import render_template, request, redirect, url_for

from .db import get_db
from .app import app
#TODO: two panels two dirs

@app.route("/", methods=["GET", "POST"])
def root():
    """ Main app view """
    if request.method == 'POST':
        pass

    return render_template("page.html")

def load_dirs():
    db = get_db()
    return db.execute('select id, name from dirs').fetchall()

def load_urls(dir_id):
    db = get_db()
    return db.execute('select name, link, id from urls where dir_id = ?', [dir_id]).fetchall()


@app.route('/urls/<dir_id>', methods=['POST', 'GET']) #TODO Make uniq dir key names
def view_all(dir_id):
    dir_id = ''
    if request.method == 'POST':
        dir_id = request.form["dir"]
        redirect(url_for("view_all", dir_id=dir_id))

    dirs = load_dirs()
    if dir_id == '':
        dir_id = next(iter(dirs))['id']
    urls = load_urls(dir_id)

    context = {
            "urls": urls,
            "dirs": dirs,
            "selected": int(dir_id),
            }
    return render_template("view_urls.html", **context)

@app.route('/urls/edit/<dir_id>', methods=['POST', 'GET']) 
def view_edit(dir_id=''):
    if request.method == 'POST':
        method = request.form["method"]
        dir_id = request.form["dir_id"]
        if method == "delete":
            pass

    dirs = load_dirs()
    if dir_id == '':
        dir_id = next(iter(dirs))['id']
    urls = load_urls(dir_id)

    context = {
            "urls": urls,
            "dirs": dirs,
            "selected": int(dir_id),
            }
    return render_template("edit.html", **context)

@app.route('/urls/add', methods=['POST'])
def add_url():
    dir_id = request.form['dir_id']
    db = get_db()
    db.execute('insert into urls (name, link, dir_id) values (?, ?, ?)',
                [request.form['name'], request.form['link'], dir_id])
    db.commit()
    return redirect(url_for('view_edit', dir_id=dir_id))

@app.route('/urls/add_dir', methods=['POST'])
def add_dir():
    dir_id = request.form['dir_id']
    db = get_db()
    db.execute('insert into dirs (name) values (?)',
                [request.form['name']])
    db.commit()
    return redirect(url_for('view_edit', dir_id=dir_id))

@app.route('/urls/del_url', methods=['POST'])
def del_url():
    db = get_db()
    dir_id = request.form['dir_id']
    db.execute('delete from urls where id = ?',
                [request.form['id']])
    db.commit()
    return redirect(url_for('view_edit', dir_id=dir_id))
