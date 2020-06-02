# Author: Femke Spaans
# Date : 11-05-2020
# Name : tutor sequenties
# Version : 1

import inlezen
import mysql.connector


def main():
    sequences, headers = add_sequences()
    read = reads(headers)
    add_to_database(sequences, headers, read)



def add_sequences():
    """
    getting sequences and headers from inlezen.py
    :return sequences, headers:
    """
    sequences = inlezen.Reader().get_seq()
    headers = inlezen.Reader().get_header()
    return sequences, headers


def add_to_database(sequentie, header, read):
    """
    connecting to database, inserting into sequences table; read,
    header and sequentie.
    :param sequentie, header, read:
    """
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="piion@hannl-hlo-bioinformatica-mysqlsrv",
        database="piion",
        password="637476")
    cursor = conn.cursor()
    for i in range(len(read)):
        cursor.execute(
            "INSERT INTO sequences(`read`, header, sequentie) values(" + read[i] +
        ", '" + header[i].replace("_", "-") +
        "', '" + sequentie[i] +
        "') ")
    conn.commit()
    cursor.close()
    conn.close()

def reads(header):
    """
    making a list called read, iterating over the length of header,
    taking the last element out of each header, putting this in list read
    :param header:
    :return read:
    """
    read = []
    for i in range(len(header)):
        length = len(header[i])
        read.append(header[i][length - 1])
    return  read


main()


