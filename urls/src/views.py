from flask import render_template, request, redirect, url_for

from .db import get_db
from .app import app

@app.route("/", methods=["GET", "POST"])
def root():
    """ Main app view """
    if request.method == 'POST':
        pass

    return render_template("page.html")

@app.route('/urls/<dir_id>', methods=['POST', 'GET']) #TODO Make uniq dir key names
def view_all(dir_id):
    if request.method == 'POST':
        method = request.form["method"]
        dir_id = request.form["dir"]
        if method == "delete":
            pass
        redirect(url_for("view_all", dir_id=dir_id))

    db = get_db()
    dirs = db.execute('select id, name from dirs').fetchall()
    if dir_id == '':
        dir_id = next(iter(dirs))

    urls = db.execute('select name, link, id from urls where dir_id = ?', dir_id).fetchall()

    context = {
            "urls": urls,
            "dirs": dirs,
            "selected": int(dir_id),
            }
    return render_template("page.html", **context)

@app.route('/urls/add', methods=['POST'])
def add_url():
    dir_id = request.form['dir_id']
    db = get_db()
    db.execute('insert into urls (name, link, dir_id) values (?, ?, ?)',
                [request.form['name'], request.form['link'], dir_id])
    db.commit()
    return redirect(url_for('view_all', dir_id=dir_id))

# TODO
@app.route('/urls/del_url', methods=['POST'])
def del_url():
    print("statr del")
    dir_id = request.form['dir_id']
    db = get_db()
    db.execute('delete from urls where id = ?',
                [request.form['id']])
    db.commit()
    print("wnd del")
    return redirect(url_for('view_all', dir_id=dir_id))
