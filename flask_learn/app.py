from flask import Flask, flash, redirect, session, url_for, request, g, request, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_openid import OpenID
from config import basedir
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

records = {
        'user1': {
            'links': [
                'http://example.com',
                'http://google.com',
                'http://som.com',
            ]
        }
}

# model
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class LoginForm(FlaskForm):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

# View
@app.route("/login/", methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
                            title = 'Sign In',
                            form = form,
                            providers = app.config['OPENID_PROVIDERS'])

@app.route("/")
@app.route("/index")
@app.route("/<dir>-<int:num>/", methods=['GET', 'POST'])
@login_required
def sub_root(dir='', num=''):
    user = g.user
    name_arg = request.args.get('dir', 'nodir')
    return render_template('index.html', name=user)

@app.route("/template1/", methods=['POST', 'GET'])
@login_required
def templ1():
    if request.method == 'GET':
        num_arg = request.args.get('num', 0)
        return render_template('app1.html', num=num_arg)
    elif request.method == 'POST':
        return render_template('app1.html', name=request.form['username'])
    else:
        return 'no'

@app.route("/blog/")
@login_required
def user_blog():
    user = g.user
    return render_template('blog.html',
                            user=user,
                            links=records[user]['links'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__=='__main__':
        app.run(debug=True)
