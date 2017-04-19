from .main import app
from flask import render_template, g, request, session, flash, redirect, url_for
import sqlite3
from .db import *
from .blog import *

@app.route('/')
def view_all():
    db = get_db()
    cur = db.execute('select name, link from urls')
    urls = cur.fetchall()
    context = {
            "var": "gzd",
            "urls": urls,
            }
    return render_template("pages.html", **context)

@app.route('/addurl', methods=['POST'])
def add_url():
    db = get_db()
    db.execute('insert into urls (name, link) values (?, ?)',
                [request.form['name'], request.form['link']])
    db.commit()
    flash('New link was successfully added')
    return redirect(url_for('view_all'))



if __name__=='__main__':
    app.debug = True
    app.run() # run dev webserver
