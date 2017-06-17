class Word:

    def __init__(self, word):
        self.id, self.word, self.lang, self.meaning = word

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __str__(self):
        str_ = '{0} {1} {2} {3}'
        return str_.format(self.id, self.word, self.lang, self.meaning)

