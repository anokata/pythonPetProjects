from flask import render_template, request

from .app import app
from .currency import load_currency_table, calculate_query


@app.route("/currency", methods=["GET", "POST"])
def root():
    ans = ""
    descripton = ""
    if request.method == 'POST':
        query = request.form["query"]
        ans, descripton = calculate_query(query)

    table, date = load_currency_table()
    return render_template("page.html", 
            ans=ans, 
            descripton=descripton,
            date=date, 
            rates=table)

