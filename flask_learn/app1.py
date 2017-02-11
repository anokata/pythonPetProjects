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
        name_arg = request.args.get('dir', 'nodir')
        return ' '.join(("<h2> dir:", dir, "_", str(num), 
                         'NAME: ', name_arg,
                         "</h2>"))

@app.route("/template1/")
def templ1(methods=['POST', 'GET']):
    if request.method == 'GET':
        num_arg = request.args.get('num', 0)
        return render_template('app1.html', num=num_arg)
    elif request.method == 'POST':
        return render_template('app1.html', num=num_arg)
    else:
        return 'no'



if __name__=='__main__':
        app.run(debug=True)
