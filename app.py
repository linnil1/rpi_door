from flask import Flask, render_template, redirect
import door
import login
import flask_login
from flask_socketio import SocketIO, disconnect
import functools
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_NAME'] = 'door'
app.config['SECRET_KEY'] = '123'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.register_blueprint(login.bp, url_prefix='')
socketio = SocketIO(app)
login.login_manager.init_app(app)
with app.app_context():
    door.db.init_app(app)
    door.db.create_all()


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@app.route('/')
@flask_login.login_required
def main():
    return render_template('index.html', op_str=door.show())


@socketio.on('connect', namespace='/')
@authenticated_only
def connect(data={}):
    print('connect', flask_login.current_user.name)
    socketio.emit('state', {
        'onoff': door.state == 'on'})


@socketio.on('open', namespace='/')
@authenticated_only
def doorOpen(data={}):
    if door.add(flask_login.current_user.name, 'open'):
        socketio.emit('history', {
            'history': [str(d) for d in door.show(limit=5)]})


@socketio.on('onoff', namespace='/')
@authenticated_only
def doorOnOff(data):
    method = 'on' if data['onoff'] else 'off'
    if door.add(flask_login.current_user.name, method):
        socketio.emit('state', {
            'onoff': door.state == 'on'})
        socketio.emit('history', {
            'history': [str(d) for d in door.show(limit=5)]})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
