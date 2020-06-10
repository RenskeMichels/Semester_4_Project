class Reader:
    def __init__(self):
        self.headers = list()
        self.sequenties = list()

        self.ascii_ = list()
        self.ascii_score = list()

    def read(self):
        for i in open("tutor excel.txt"):
            _list = i.split("\t")
            self.headers.append(_list[0])
            self.sequenties.append(_list[1])
            self.ascii_.append(_list[2])
            self.headers.append(_list[3])
            self.sequenties.append(_list[4])
            self.ascii_.append(_list[5])
        return self.sequenties

    def ascii(self):
        for i in range(len(self.ascii_)):
            _ascii = 0
            for j in range(len(self.ascii_[i])):
                _ascii += ord(self.ascii_[i][j])
            self.ascii_score.append(_ascii)
        return self.ascii_score

    def get_seq(self):
        return self.read()

    def get_ascii(self):
        return self.ascii()


    def get_header(self):
        self.read()
        return self.headers


if __name__ == '__main__':
    reader = Reader()
