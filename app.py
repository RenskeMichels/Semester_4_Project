# Pieter Verhoef
# 24-5-2020

from flask import Flask, render_template, request
import sqlfuncties
from Bio.Blast import NCBIWWW
import re

# Deze globale variabelen zijn nodig om de waardes te onthouden
# nadat een POST formulier is verzonden, en daarna op de button
# vorige of volgende wordt geklikt, zodat deze opnieuw de BLAST resultaten
# kan ophalen aan de hand van de huidige pagina en deze variabelen.

# ------- Organisme pagina -------------- #
aantal_per_pagina_org = None
percentage_identity_org = None
e_value_org = None
familie = None
geslacht = None
soort = None
# ------ Protein pagina ---------------- #
aantal_per_pagina_protein = None
percentage_identity_protein = None
e_value_protein = None
eiwitnaam = None

app = Flask(__name__)


@app.route("/")
def index():
    """ Home pagina """
    return render_template("index.html")


@app.route("/organisme", methods=["GET", "POST"])
def organisme():
    """
    Pagina om op organisme niveau te kunnen filteren op de BLAST resultaten
    """
    global aantal_per_pagina_org, percentage_identity_org, e_value_org,\
        familie, geslacht, soort

    # Haal paginanummer uit url,
    # mocht deze niet url staan dan ben je op de eerste pagina.
    pagenummer = int(request.args.get('page', "0"))

    # Haal cursors op die nodig zijn voor het bevragen van de mysql database.
    conn = sqlfuncties.connectie()

    familie_cursor = sqlfuncties.alle_families(conn)
    geslachten_cursor = sqlfuncties.alle_geslachten(conn)
    soorten_cursor = sqlfuncties.alle_soorten(conn)

    # Deze resultaten cursor haalt aan de hand van de filters in het formulier
    # de resultaten op.
    resultaten_cursor = ""

    # Alleen resultaten laten zien wanneer een formulier is verzonden of
    # het paginanummer in de url staat.
    if "page" in request.args:
        if not (aantal_per_pagina_org is None):
            # Haal resultaten op.
            resultaten_cursor = sqlfuncties. \
                resultaten_organisme(conn, aantal_per_pagina_org,
                                     percentage_identity_org, pagenummer,
                                     e_value_org, familie, geslacht, soort)

    conn.close()
    # Formulier ingevuld
    if request.method == 'POST':

        pagenummer = 0
        # Haal formulier gegevens op.
        aantal_per_pagina_org = request.form.get("aantalres")

        percentage_identity_org = request.form.get("percentageidentity")
        e_value_org = request.form.get("evalue")
        familie = request.form.get("selfamilie")
        geslacht = request.form.get("selgeslacht")
        soort = request.form.get("selsoort")

        # Gebruik de gegevens van het formulier om de resultaten te bepalen.
        conn = sqlfuncties.connectie()
        resultaten_cursor = sqlfuncties.\
            resultaten_organisme(conn, aantal_per_pagina_org,
                                 percentage_identity_org,
                                 pagenummer, e_value_org, familie, geslacht,
                                 soort)
        conn.close()
        return render_template("organisme.html", pagenummer=pagenummer,
                               familie_cursor=familie_cursor,
                               geslachten_cursor=geslachten_cursor,
                               soorten_cursor=soorten_cursor,
                               resultaten_cursor=resultaten_cursor)

    return render_template("organisme.html", pagenummer=pagenummer,
                           familie_cursor=familie_cursor,
                           geslachten_cursor=geslachten_cursor,
                           soorten_cursor=soorten_cursor,
                           resultaten_cursor=resultaten_cursor)


@app.route("/protein", methods=["GET", "POST"])
def protein():
    """
    Pagina om op protein namen
    te kunnen filteren op de BLAST resultaten
    """
    global aantal_per_pagina_protein, percentage_identity_protein,\
           e_value_protein, eiwitnaam

    # Haal paginanummer uit url,
    # mocht deze niet url staan dan ben je op de eerste pagina.
    pagenummer = int(request.args.get('page', "0"))

    conn = sqlfuncties.connectie()
    eiwitnamen_cursor = sqlfuncties.alle_eiwitnamen(conn)

    # Deze resultaten cursor haalt aan de hand van de filters in het formulier
    # de resultaten op.
    resultaten_cursor = ""

    # Alleen resultaten laten zien wanneer een formulier is verzonden en
    # het paginanummer in de url staat.
    if "page" in request.args:
        if not (aantal_per_pagina_protein is None):
            # Haal resultaten op.
            resultaten_cursor = sqlfuncties. \
                resultaten_protein(conn, aantal_per_pagina_protein,
                                   percentage_identity_protein, pagenummer,
                                   e_value_protein, eiwitnaam)

    conn.close()
    # Formulier verzonden
    if request.method == 'POST':

        pagenummer = 0
        # Haal formulier gegevens op.
        aantal_per_pagina_protein = request.form.get("aantalres")

        percentage_identity_protein = request.form.get("percentageidentity")
        e_value_protein = request.form.get("evalue")
        eiwitnaam = request.form.get("seleiwitnaam")
        # Gebruik de gegevens van het formulier om de resultaten te bepalen.
        conn = sqlfuncties.connectie()
        resultaten_cursor = sqlfuncties.\
            resultaten_protein(conn, aantal_per_pagina_protein,
                               percentage_identity_protein,
                               pagenummer, e_value_protein,
                               eiwitnaam)
        conn.close()
        return render_template("protein.html", pagenummer=pagenummer,
                               eiwitnamen_cursor=eiwitnamen_cursor,
                               resultaten_cursor=resultaten_cursor)

    return render_template("protein.html", pagenummer=pagenummer,
                           eiwitnamen_cursor=eiwitnamen_cursor,
                           resultaten_cursor=resultaten_cursor)


@app.route("/blast", methods=["POST", "GET"])
def blast():
    pagenummer = int(request.args.get('page', "0"))

    if request.method == 'POST':

        seq = request.form.get("blastseq").rstrip().lower()

        dna = is_dna(seq)

        if dna:
            print("before blast")
            blast_to_xml(seq)
            print("after blast")
            resultaten = get_results()
            return render_template("blast.html", pagenummer=pagenummer,
                                   resultaten=resultaten)
        else:
            return render_template("blast.html", pagenummer=pagenummer,
                                   bericht="Voer AUB een DNA sequentie in")

    return render_template("blast.html", pagenummer=pagenummer)


@app.route('/overons')
def overons():
    return render_template("overons.html")


def is_dna(seq):
    return not re.search("[^atcgn]", seq)


def blast_to_xml(seq):
    """
    Sequentie die van de website afkomt wordt geblast tegen de database
    met het blastx algoritme
    :param seq: DNA sequentie vanuit de website
    :return: Het blast bestand
    """
    blast = NCBIWWW.qblast('blastx', 'nr', seq)
    with open("blast.xml", "w") as out_handle:

        out_handle.write(blast.read())
        
    blast.close()


def get_results():
    return ""


if __name__ == '__main__':
    app.run()
