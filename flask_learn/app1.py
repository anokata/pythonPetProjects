from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

records = {
        'user1': {
            'links': [
                'http://example.com',
                'http://google.com',
                'http://som.com',
            ]
        }
}

@app.route("/")
def root():
    return "<h1>x</h1>"

@app.route("/index")
@app.route("/<dir>-<int:num>/", methods=['GET', 'POST'])
def sub_root(dir, num):
    if request.method == 'POST':
        return 'POST'
    else:
        name_arg = request.args.get('dir', 'nodir')
        return ' '.join(("<h2> dir:", dir, "_", str(num), 
                         'NAME: ', name_arg,
                         "</h2>"))

@app.route("/template1/", methods=['POST', 'GET'])
def templ1():
    if request.method == 'GET':
        num_arg = request.args.get('num', 0)
        return render_template('app1.html', num=num_arg)
    elif request.method == 'POST':
        return render_template('app1.html', name=request.form['username'])
    else:
        return 'no'

@app.route("/<user>/blog/")
def user_blog(user='user1'):
    return render_template('blog.html',
                            user=user,
                            links=records[user]['links'])


if __name__=='__main__':
        app.run(debug=True)
