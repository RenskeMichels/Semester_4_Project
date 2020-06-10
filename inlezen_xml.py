##########################################################################
# Auteur: David van Eersel
# Datum 5-5-20
# Functie: het inlezen van een xml bestand
# versie: 1.0 : het inlezen van een txt output bestand van blast
# versie: 2.0 : het inlezen van een xml output bestand van blast
# versie: 2.1 : extra parameters toegevoegd
##########################################################################


def lees_bestand():
    try:
        data = list()
        for i in open("BLAST/my_blast.xml"):
            data.append(i.strip())
        return data
    except ValueError:
        print("Geen alignments")


class Reader:
    def __init__(self):
        self.a_name = list()
        self.list = list()
        self.accesie_code = list()
        self.max_score = list()
        self.identities = list()
        self.frame = list()
        self.e_value = list()
        self.positives = list()
        self.data = lees_bestand()

    def get_accessie_code(self):
        return self.set_accessie_code()

    def get_max_score(self):
        return self.set_max_score()

    def get_identities(self):
        return self.set_identities()

    def get_frame(self):
        return self.set_frame()

    def get_e_value(self):
        return self.set_e_value()

    def get_positives(self):
        return self.set_positives()

    def get_a_name(self):
        return self.set_a_name()

    def zoek(self, variable):
        self.list.clear()
        counter = 1
        for i in range(len(self.data)):
            if '<?xml version="1.0"?>' in self.data[i]:
                self.list.append("Blast" + str(counter))
                counter += 1
                counter2 = 1
                for j in range(1, len(self.data)):
                    if counter2 <= 20:
                        if variable in self.data[j]:
                            counter2 += 1
                            self.list.append(
                                self.data[j].replace("<" + variable + ">", "").replace("</" + variable + ">", ''))
                        elif '<?xml version="1.0"?>' in self.data[j]:
                            break
                    else:
                        break
            else:
                pass
        return self.list

    def set_accessie_code(self):
        tussenstap = self.zoek("Hit_accession")
        self.accesie_code = tussenstap.copy()
        return self.accesie_code

    def set_max_score(self):
        tussenstap = self.zoek("Hsp_score")
        self.max_score = tussenstap.copy()
        return self.max_score

    def set_identities(self):
        tussenstap = self.zoek("Hsp_identity")
        self.identities = tussenstap.copy()
        return self.identities

    def set_frame(self):
        tussenstap = self.zoek("Hsp_query-frame")
        self.frame = tussenstap.copy()
        return self.frame

    def set_e_value(self):
        tussenstap = self.zoek("Hsp_evalue")
        self.e_value = tussenstap.copy()
        return self.e_value

    def set_positives(self):
        tussenstap = self.zoek("Hsp_positive")
        self.positives = tussenstap.copy()
        return self.positives

    def set_a_name(self):
        tussenstap = self.zoek("Hit_def")
        self.a_name = tussenstap.copy()
        return self.a_name


if __name__ == '__main__':
    reader = Reader()
