from flask import Flask, flash, redirect
from flask import request
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required

app = Flask(__name__)
app.config.from_object('config')

records = {
        'user1': {
            'links': [
                'http://example.com',
                'http://google.com',
                'http://som.com',
            ]
        }
}

class LoginForm(FlaskForm):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + 
              form.openid.data + '", remember_me=' + 
              str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                            title = 'Sign In',
                            form = form)

@app.route("/")
def root():
    return "<h1>x</h1>"

@app.route("/index")
@app.route("/<dir>-<int:num>/", methods=['GET', 'POST'])
def sub_root(dir='', num=''):
    name_arg = request.args.get('dir', 'nodir')
    return render_template('index.html', name=name_arg)

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
