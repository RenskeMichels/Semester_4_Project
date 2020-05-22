from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/home')
def hello_world():
    return render_template("home.html")


@app.route("/blast", methods=["POST", "GET"])
def blast():
    seq = request.form.get("seq", '')
    return render_template("blast.html")


@app.route("/organisme")
def organisme():
    return render_template("organisme.html")


@app.route("/overons")
def overons():
    return render_template("over ons.html")


@app.route("/proteines")
def proteines():
    return render_template("proteines.html")


if __name__ == '__main__':
    app.run()
