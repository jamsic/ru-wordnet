class Synset:

    def __init__(self, sid, words):
        self.words = words
        self.id = sid

    def __eq__(self, other):
        return self.id == self.other and self.words == other.words

    def __hash__(self):
        return self.id

