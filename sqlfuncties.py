# Pieter Verhoef
# 27-5-2020

import mysql.connector


def connectie():
    """
    Deze functie maakt de connectie met de database.
    """
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="piion@hannl-hlo-bioinformatica-mysqlsrv", db="piion",
        password='637476')

    return conn


# ------------- Organisme pagina ------------------------
def alle_families(conn):
    """
    Deze functie haalt alle familienamen op.
    :param conn: De database connectie
    :return: familienamen
    """
    cursor = conn.cursor()
    cursor.execute("select familienaam from familie "
                   "where familienaam != 'onbekend' order by familienaam asc;")
    rijen = cursor.fetchall()
    cursor.close()
    return rijen


def alle_geslachten(conn):
    """
    Deze functie haalt alle geslachten op.
    :param conn: De database connectie
    :return: geslachtsnamen
    """
    cursor = conn.cursor()
    cursor.execute("select geslachtsnaam from geslacht where geslachtsnaam "
                   "!= 'onbekend' order by"
                   " geslachtsnaam asc;")
    rijen = cursor.fetchall()
    cursor.close()

    return rijen


def alle_soorten(conn):
    """
    Deze functie haalt alle soortnamen op.
    :param conn: De database connectie
    :return: soortnamen
    """
    cursor = conn.cursor()
    cursor.execute("select soortnaam from soort where soortnaam != 'onbekend'"
                   "order by soortnaam asc;")
    rijen = cursor.fetchall()
    cursor.close()

    return rijen


def resultaten_organisme(conn, aantal_per_pagina, percentage_identity,
                         pagenummer, e_value, familie, geslacht, soort):
    """
    Deze functie haalt de BLAST resultaten op uit de database.
    Hierbij worden de filter gegevens meegenomen, verder wordt per pagina
    door middel van het paginanummer de specifieke resultaten van die pagina
    getoond.
    :param conn: De connectie
    :param aantal_per_pagina: Het aantal resultaten per pagina
    :param percentage_identity: Het percentage identity
    :param pagenummer: Het  paginanummer
    :param e_value: De evalue
    :param familie: De familie
    :param geslacht: Het geslacht
    :param soort: De soort
    :return: De resultaten
    """

    cursor = conn.cursor()
    start = int(aantal_per_pagina) * int(pagenummer)
    sql = ("select distinct header, familienaam, geslachtsnaam,"
           " soortnaam, max_score, "
           "query_cover, e_value, percentage_identity, positives, "
           "accesie_code from blast_resultaten br join "
           "familie f on br.Familie_id = f.id join geslacht g "
           "on br.Geslacht_id = g.id join soort s on "
           "br.Soort_id = s.id join sequences sq on br.Reads_id = sq.id "
           "where percentage_identity > %s")

    if e_value != "":
        e_value = float(e_value)
        sql += " and e_value < %s" % (e_value, )

    if familie != 'allefamilies':
        sql += " and familienaam = '%s'" % (familie, )

    if geslacht != 'allegeslachten':
        sql += " and geslachtsnaam = '%s'" % (geslacht, )

    if soort != 'allesoorten':
        sql += " and soortnaam = '%s'" % (soort, )

    sql += " limit %s offset %s"

    cursor.execute(sql, (int(percentage_identity), int(aantal_per_pagina),
                         start))

    rijen = cursor.fetchall()
    cursor.close()

    return rijen


# ------------- protein pagina ---------------------------
def alle_eiwitnamen(conn):

    cursor = conn.cursor()
    cursor.execute("select distinct eiwit_naam from blast_resultaten order by"
                   " eiwit_naam asc;")
    rijen = cursor.fetchall()
    cursor.close()

    return rijen


def resultaten_protein(conn, aantal_per_pagina, percentage_identity,
                       pagenummer, e_value, eiwitnaam):
    cursor = conn.cursor()
    start = int(aantal_per_pagina) * int(pagenummer)
    sql = ("select distinct header, eiwit_naam, max_score, "
           "query_cover, e_value, percentage_identity, positives, "
           "accesie_code from blast_resultaten br join sequences sq"
           " on br.Reads_id = sq.id  where percentage_identity > %s")

    if e_value != "":
        e_value = float(e_value)
        sql += " and e_value < %s" % (e_value, )

    if eiwitnaam != "alleeiwitnamen":
        sql += " and eiwit_naam = '%s'" % (eiwitnaam, )

    sql += " limit %s offset %s"

    cursor.execute(sql, (int(percentage_identity),
                         int(aantal_per_pagina), start))

    rijen = cursor.fetchall()
    cursor.close()

    return rijen

