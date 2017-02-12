from flask import Flask, flash, redirect, session, url_for, request, g, request, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, validators, TextAreaField, SelectField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import basedir
import os
import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(24), index = True, unique = False)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

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
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime)
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_from_id=None, user_to_id=None, message=''):
        self.user_from_id = name
        self.user_to_id = user_to_id
        self.message = message
        timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return '<msg %r>' % (self.message)


class ChatForm(FlaskForm):
    message = TextField('message', validators = [
                        Required(),
                        validators.Length(min=1, max=220)
    ])
    chat = TextAreaField()

class LoginForm(FlaskForm):
    name = TextField('name', validators = [
                        Required(),
                        validators.Length(min=3, max=20)
    ])
    password = PasswordField('password', validators = [
                        Required(),
                        validators.DataRequired()
    ])

class RegistrationForm(FlaskForm):
    name = TextField('name', validators = [
                        Required(),
                        validators.Length(min=4, max=20)
    ])
    password = PasswordField('password', validators = [
                        Required(),
                        validators.DataRequired(),
                        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

# V
@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/users', methods=['GET', 'POST'])
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@login_required
@app.route('/chat/<name>', methods=['GET', 'POST'])
def chat(name=None):
    if name == None:
        return render_template('chat.html', form=form)
    form = ChatForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('chat.html', form=form)
    else:
        return render_template('chat.html', form=form, 
                    user_from=current_user.name,
                    user_to=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(form.name.data,
                        form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering')
            return redirect(url_for('login'))
        else:
            flash('That user Name already exist')
            return render_template('register.html', form=form)
    elif request.method == 'POST' and not form.validate():
        flash('Error in input data')
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # get user
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            flash('Not exist, register please.')
            return redirect(url_for('register'))
        # Check user
        if user.password == form.password.data:
            login_user(user)
            flash('Login OK')
            return redirect(url_for('index'))
        else:
            flash('Incorrect password!')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = g.user
    return render_template('index.html', name=user)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__=='__main__':
        app.run(debug=True)
