##########################################################################
# Auteur: David van Eersel
# Datum 31-5-20
# Functie: het blasten van de sequenties met blastx tegen de nr database.
#          De sequentie wordt opgehaald vanaf de site.
# Versie: 1.0
##########################################################################

from Bio.Blast import NCBIWWW


def blast(seq):
    """ Sequentie die van de website afkomt wordt geblast tegen de database met het blastx algoritme
    :param seq: DNA sequentie vanuit de website
    :return: Het blast bestand
    """
    blast = NCBIWWW.qblast('blastx', 'nr', seq)
    with open("my_blast.xml", "a") as out_handle:
        out_handle.write(blast.read())
