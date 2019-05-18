from flask import Flask, render_template, redirect
import door


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/open", methods=["POST"])
def doorOpen():
    door.doorOpen()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
