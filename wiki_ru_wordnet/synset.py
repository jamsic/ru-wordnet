class Synset:
    """Синсет, объединяющий слова, имеющие общее значение.

    Методы:
        get_words (): возвращает множество объектов типа Word,
        которые являются синонимами.
    """

    def __init__(self, sid, words):
        self._words = words
        self._id = sid

    def get_words(self):
        return self._words

    def __eq__(self, other):
        return self._id == other._id and self._words == other._words

    def __hash__(self):
        return self._id

