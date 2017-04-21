from flask import render_template

from .app import app
from .currency import *


@app.route("/")
def root():
    ans = "n"
    table, date = load_currency_table()
    return render_template("page.html", 
            ans=ans, 
            date=date, 
            rates=table)

