from flask import Flask
from Bio.Seq import Seq

app = Flask(__name__)

@app.route("/")
def hello():
    my_seq = Seq("AGTACACTGGT")
    return "Hello World! test4"
