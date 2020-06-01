from flask import Flask, render_template, request
import sqlfuncties

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
    return render_template("index.html")


@app.route("/organisme", methods=["GET", "POST"])
def organisme():

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

    resultaten_cursor = ""

    # Alleen resultaten laten zien wanneer een formulier is verzonden en
    # het paginanummer in de url staat.
    if "page" in request.args:
        if not (aantal_per_pagina_org is None):

            resultaten_cursor = sqlfuncties. \
                resultaten_organisme(conn, aantal_per_pagina_org,
                                     percentage_identity_org, pagenummer,
                                     e_value_org, familie, geslacht, soort)

    conn.close()

    if request.method == 'POST':

        pagenummer = 0
        aantal_per_pagina_org = request.form.get("aantalres")

        percentage_identity_org = request.form.get("percentageidentity")
        e_value_org = request.form.get("evalue")
        familie = request.form.get("selfamilie")
        geslacht = request.form.get("selgeslacht")
        soort = request.form.get("selsoort")

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
                           familie_cursor=familie_cursor, geslachten_cursor=
                           geslachten_cursor, soorten_cursor=soorten_cursor,
                           resultaten_cursor=resultaten_cursor)


@app.route("/protein", methods=["GET", "POST"])
def protein():

    global aantal_per_pagina_protein, percentage_identity_protein,\
           e_value_protein, eiwitnaam

    # Haal paginanummer uit url,
    # mocht deze niet url staan dan ben je op de eerste pagina.
    pagenummer = int(request.args.get('page', "0"))

    conn = sqlfuncties.connectie()
    eiwitnamen_cursor = sqlfuncties.alle_eiwitnamen(conn)

    resultaten_cursor = ""

    # Alleen resultaten laten zien wanneer een formulier is verzonden en
    # het paginanummer in de url staat.
    if "page" in request.args:
        if not (aantal_per_pagina_protein is None):

            resultaten_cursor = sqlfuncties. \
                resultaten_protein(conn, aantal_per_pagina_protein,
                                   percentage_identity_protein, pagenummer,
                                   e_value_protein, eiwitnaam)

    conn.close()

    if request.method == 'POST':

        pagenummer = 0
        aantal_per_pagina_protein = request.form.get("aantalres")

        percentage_identity_protein = request.form.get("percentageidentity")
        e_value_protein = request.form.get("evalue")
        eiwitnaam = request.form.get("seleiwitnaam")

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


if __name__ == '__main__':
    app.run()
