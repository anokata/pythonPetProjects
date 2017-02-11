from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>x</h1>"

@app.route("/<dir>-<int:num>/", methods=['GET', 'POST'])
def sub_root(dir, num):
    if request.method == 'POST':
        return 'POST'
    else:
        return ' '.join(("<h2> dir:", dir, "_", 
                         str(num), "</h2>"))

@app.route("/template1/<arg>")
def templ1(arg=None):
    return render_template('app1.html', name=arg)


if __name__=='__main__':
        app.run(debug=True)
