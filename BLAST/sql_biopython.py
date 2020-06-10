##########################################################################
# Auteur: David van Eersel
# Datum 5-13-20
# Functie: het blasten van de sequenties met blastx tegen de nr database.
#          Daarbij worden de sequenties uit de database gehaald
# versie: 2.0
# (versie 1.0 was het vorige biopythonscript)
##########################################################################

from Bio.Blast import NCBIWWW
import mysql.connector
import time


def getal():
    """
    hier wordt er verbinding gemaakt met de database. er wordt dan geteld hoeveel sequenties in de datbase staan om
    deze later weer te kunnen gebruiken in een for loop
    :return: het aantal sequenties die in de database staan
    """
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="piion@hannl-hlo-bioinformatica-mysqlsrv", db="piion",
        password='637476')

    cursur = conn.cursor()
    cursur.execute("select count(sequentie) from sequences")
    getal = cursur.fetchall()
    cursur.close()
    conn.close()
    return getal


def blast(getal):
    """ hier worden de de sequenties geblast. deze worden opgehaald uit de database. dit wordt gedaan met de id nummers
    :param getal: aantal sequenties
    :return: een bestand waar de blast resultaten inzitten
    """
    #with open("my_blast.xml", "w") as out_handle:  # maakt het bestand leeg als hier nog wat in staat
        #out_handle.write("")
    idn = 186  # het id nummer
    for i in range(185, int(getal[0][0])):  # de connectie wordt elke keer verbroken omdat het programma anders te lange
        # tijd zonder wat te doen verbonden is aan de database
        idn += 1
        seq = list()
        conn = mysql.connector.connect(
            host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
            user="piion@hannl-hlo-bioinformatica-mysqlsrv", db="piion",
            password='637476')
        cursur = conn.cursor()
        cursur.execute("select sequentie from sequences where id =" + str(idn) + ";")
        rows = cursur.fetchall()
        seq.append(rows[0][0])
        cursur.close()
        conn.close()
        print(seq[0])
        blast = NCBIWWW.qblast('blastx', 'nr', seq[0])
        with open("my_blast.xml", "a") as out_handle:
            out_handle.write(blast.read())
        time.sleep(600)  # seconde


if __name__ == '__main__':
    g1 = getal()
    blast(g1)
