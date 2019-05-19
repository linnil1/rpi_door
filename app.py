from flask import Flask, render_template, redirect
import door
import login
import flask_login


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_NAME'] = 'door'
app.secret_key = '123'
with app.app_context():
    door.db.init_app(app)
    door.db.create_all()
    login.login_manager.init_app(app)
    app.register_blueprint(login.bp, url_prefix='')


@app.route("/")
@flask_login.login_required
def main():
    return render_template('index.html', op_str=door.show())


@app.route("/open", methods=["POST"])
@flask_login.login_required
def doorOpen():
    door.doorOpen()
    door.add('who', 'open')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
