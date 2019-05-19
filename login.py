import time
from flask import (Blueprint, request,
                   render_template, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
import flask_login
import passlib.hash


db = SQLAlchemy()
login_manager = flask_login.LoginManager()
bp = Blueprint(__name__, 'home')
login_manager.login_view = 'login.login'


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __str__(self):
        return '<User {}>'.format(self.name)

    def checkPassword(self, password):
        return passlib.hash.sha512_crypt.verify(password, self.password)

    def setPassword(self, password):
        self.password = passlib.hash.sha512_crypt.hash(password)
        db.session.commit()


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


def add_user(name, passwd=''):
    u = User.query.filter_by(name=name).first()
    assert(not u)
    u = User(name=name)
    u.setPassword(passwd)
    db.session.add(u)
    db.session.commit()
    return name


def requestParse(request):
    name = request.form.get('username')
    password = request.form.get('password')
    name = (name or '')
    if not name or not password:
        return name, False

    u = User.query.filter_by(name=name).first()
    if not u:
        return name, False
    if not u.checkPassword(password):
        return name, False
    flask_login.login_user(user_loader(u.id))
    return name, True


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.login_fresh():
            return redirect(url_for('main'))
        else:
            return render_template('Login.html')
    else:
        name, ok = requestParse(request)
        if ok:
            nexturl = request.args.get('next')
            return redirect(nexturl or url_for('main'))
        else:
            return render_template('Login.html', error='Fail to Login')


@bp.route('/logout')
@flask_login.login_required
def logout():
    now_user = flask_login.current_user
    flask_login.logout_user()
    return redirect(url_for('main'))
