# Author: Femke Spaans
# Date : 12-05-2020
# Name : tutor blast
# Version : 1

import inlezen_xml
import mysql.connector


def main():
    max_score, frame, e_value, identities, positives, \
    accesie_code, a_name = data()
    add_results_to_database(max_score, frame, e_value,
           identities, positives, accesie_code, a_name)


def data():
    """getting max score, total score, query cover, e value,
    percentage indentity, positives and accession codes from file
    :return max_score, total_score, query_cover, e_value,
    percentage_indentity, positives, accesie_code:
    """
    max_score = inlezen_xml.Reader().get_max_score()
    frame = inlezen_xml.Reader().get_frame()
    e_value = inlezen_xml.Reader().get_e_value()
    identities = inlezen_xml.Reader().get_identities()
    positives = inlezen_xml.Reader().get_positives()
    accesie_code = inlezen_xml.Reader().get_accessie_code()
    a_name = inlezen_xml.Reader().get_a_name()
    return max_score, frame, e_value, \
           identities, positives, accesie_code, a_name


def add_results_to_database(max_score, frame, e_value,
           percentage_identity, positives, accesie_code, a_name):
    """  connecting to database, inserting into BLAST resultaten table; max score,
    total score, query cover, e value, percentage identity, positives
    and accesie code.
    :param max_score, total_score, query_cover, e_value,
           percentage_identity, positives, accesie_code:
    """
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="piion@hannl-hlo-bioinformatica-mysqlsrv",
        database="piion",
        password="637476")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO BLAST_resultaten(max_score, frame,"
                   " query_cover, e_value, percentage_identity, "
                   "postives, acessie_code, eiwit_naam) "
                   "values(" + max_score + ","
                    " " + frame + ","
                    " " + e_value + ", " + percentage_identity + ","
                    " " + positives + ", '" + accesie_code + "', " + a_name + ") ")
    conn.commit()
    cursor.close()
    conn.close()


main()
