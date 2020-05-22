from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/organisme", methods=["GET", "POST"])
def organisme():

    return render_template("organisme.html")


@app.route("/protein", methods=["GET", "POST"])
def protein():

    return render_template("protein.html")


if __name__ == '__main__':
    app.run()
