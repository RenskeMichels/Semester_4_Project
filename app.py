from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/blast", methods=["POST", "GET"])
def blast():
    seq = request.form.get("seq", '')
    pagenummer = int(request.args.get('page', "0"))
    return render_template("blast.html", pagenummer=pagenummer)


@app.route("/organisme")
def organisme():
    return render_template("organisme.html")


@app.route("/overons")
def overons():
    return render_template("overons.html")


@app.route("/proteine")
def proteines():
    return render_template("proteines.html")


if __name__ == '__main__':
    app.run()
