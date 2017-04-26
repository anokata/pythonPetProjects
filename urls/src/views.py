from flask import render_template, request

from .app import app

@app.route("/", methods=["GET", "POST"])
def root():
    """ Main app view """
    if request.method == 'POST':
        pass

    return render_template("page.html")

