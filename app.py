from flask import Flask, render_template, redirect
import door


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    door.db.init_app(app)
    door.db.create_all()


@app.route("/")
def main():
    return render_template('index.html', op_str=door.show())


@app.route("/open", methods=["POST"])
def doorOpen():
    door.doorOpen()
    door.add('who', 'open')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
