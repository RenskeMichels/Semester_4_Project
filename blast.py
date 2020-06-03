##########################################################################
# Auteur: David van Eersel
# Datum 31-5-20
# Functie: het blasten van de sequenties met blastx tegen de nr database.
#          De sequentie wordt opgehaald vanaf de site.
# Versie: 1.0
##########################################################################

from Bio.Blast import NCBIWWW
import inlezen_xml
import re

def blast_to_xml(seq):
    """
    Sequentie die van de website afkomt wordt geblast tegen de database
    met het blastx algoritme
    :param seq: DNA sequentie vanuit de website
    :return: Het blast bestand
    """
    blast = NCBIWWW.qblast('blastx', 'nr', seq)
    with open("my_blast.xml", "a") as out_handle:
        out_handle.write(blast.read())

    blast.close()


def data_blast():
    """getting max score, total score, query cover, e value,
    percentage indentity, positives and accession codes from file
    :return max_score, total_score, query_cover, e_value,
    percentage_indentity, positives, accesie_code:
    """
    blast_reader = inlezen_xml.Reader()
    max_scores = blast_reader.get_max_score()
    e_values = blast_reader.get_e_value()
    identities = blast_reader.get_identities()
    positives = blast_reader.get_positives()
    accesie_codes = blast_reader.get_accessie_code()
    a_names = blast_reader.get_a_name()

    return max_scores, e_values, \
        identities, positives, accesie_codes, a_names


def get_results(paginanummer):
    """
    Haal blast resultaten uit xml bestand.
    :param paginanummer: Het paginanummer
    """
    max_scores, e_values, \
    identities, positives, accesie_codes, a_names = data_blast()
    aantal_per_pagina = 10
    resultaten = []
    paginanummer = int(paginanummer)
    start = paginanummer * aantal_per_pagina
    for i in range(start, start+aantal_per_pagina, 1):
        if "Blast" not in max_scores[i]:
            a_name = a_names[i]
            a_name = a_name.replace(re.search(r'\[.+\]', a_name)
                                    .group(), "").rstrip()
            resultaten.append([max_scores[i], e_values[i], identities[i],
                              positives[i], accesie_codes[i], a_name])
    return resultaten
