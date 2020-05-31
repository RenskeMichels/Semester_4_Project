# Author: Femke Spaans & David van Eersel
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
                            percentage_identity, positives, accesie_code,
                            a_name):
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
    blast = 0
    for i in range(len(frame)):
        if "Blast" in frame[i]:
            blast = frame[i].replace("Blast", "").strip()
        elif "Blast" not in frame[i]:
            print(i, "van de", len(frame)-200)
            print("-"*80)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO BLAST_resultaten("
                           "max_score"
                           ", frame"
                           ", e_value"
                           ", percentage_identity"
                           ", positives"
                           ", accesie_code"
                           ", eiwit_naam"
                           ", Reads_id)"
                           "values('" + max_score[i] +
                            "','"      + frame[i] +
                            "','"      + e_value[i] +
                            "','"      + percentage_identity[i] +
                            "','"      + positives[i] +
                            "','"      + accesie_code[i] +
                            "','"      + a_name[i] +
                            "','"      + str(blast) + "') ")
    conn.commit()
    cursor.close()
    conn.close()


main()
