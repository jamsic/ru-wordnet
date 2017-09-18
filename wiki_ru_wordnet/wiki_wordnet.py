from .wiki_wordnet_connector import WikiWordnetConnector
from .word import Word
from collections import defaultdict
from .synset import Synset


class WikiWordnet:
    """
    Класс для доступа к Wiki-Wordnet и базе данных.

    Методы:
        get_synsets(lemma): возвращает синсеты, содержащие заданную лемму.

        get_hypernyms(synset): возвращает гиперонимы первого уровня синсета
           synset.

        get_hyponyms(synset): возвращает гипонимы первого уровня синсета
            synset.

        get_common_hypernyms(syn1, syn2, max_level=10): возвращает общие
            гиперонимы синсетов syn1 и syn2 не более max_level уровня.

        get_common_hyponyms(syn1, syn2, max_level=10): возвращает общие
            гипонимы синсетов syn1 и syn2 не более max_level уровня.

        get_lowest_common_hypernyms( synset1, synset2, max_level=10):
            возвращает ближайший общий гипероним синсетов syn1 и syn2
            не более max_level уровня.

        get_lowest_common_hyponyms(synset1, synset2, max_level=10):
            возвращает ближайший общий гипоним синсетов syn1 и syn2
            не более max_level уровня.
    """

    def __init__(self):
        dbcon = WikiWordnetConnector()
        self._load_info(dbcon)

    def _load_info(self, dbcon):
        synsets_db = dbcon.get_synsets()
        hypernyms_db = dbcon.get_hypernyms()
        synsets = self._process_synsets(synsets_db)
        self._synsets_by_sid, self._synsetids_by_lemma = synsets
        hypersids = self._process_hypernyms(hypernyms_db)
        self._hypersids_by_sid, self._hyposids_by_sid = hypersids

    def _process_synsets(self, synsets_db):
        words_by_sid = defaultdict(set)
        synsetids_by_lemma = defaultdict(set)
        for sid, lemma, definition in synsets_db:
            synsetids_by_lemma[lemma].add(sid)
            words_by_sid[sid].add(Word((lemma, definition),))
        synsets = defaultdict(set)
        for sid, words in words_by_sid.items():
            synsets[sid] = Synset(sid, words)
        return dict(synsets), synsetids_by_lemma

    def _process_hypernyms(self, hypernyms_db):
        hyperonyms = defaultdict(set)
        hyponyms = defaultdict(set)
        for sid, hypersid in hypernyms_db:
            hyperonyms[sid].add(hypersid)
            hyponyms[hypersid].add(sid)
        return dict(hyperonyms), dict(hyponyms)

    def _get_common(self, syn1, syn2, max_level, nym_fun):
        nyms1 = nym_fun(syn1._id, 0, max_level)
        nyms2 = nym_fun(syn2._id, 0, max_level)
        nymdct1 = {synset: level for level, synset in nyms1}
        nymdct2 = {synset: level for level, synset in nyms2}
        common_nyms = nymdct1.keys() & nymdct2.keys()
        common_nyms_ = [(self._synsets_by_sid[ch], nymdct1[ch],
                         nymdct2[ch]) for ch in common_nyms]
        return common_nyms_

    # TO DO replace with smth normal
    def _get_nyms_rec(self, synset, cur_level, to_level, nym_fun):
        hyps = {(cur_level, synset)}
        if cur_level < to_level:
            for hypsynset in nym_fun(synset):
                hyps.update(self._get_nyms_rec(hypsynset, cur_level + 1,
                                               to_level, nym_fun))
        return hyps

    def _get_hypersids(self, sid):
        return self._hypersids_by_sid.get(sid, set())

    def _get_hypernyms_rec(self, synset, cur_level, to_level):
        return self._get_nyms_rec(synset, cur_level, to_level,
                                  lambda x: self._get_hypersids(x))

    def _get_hyposids(self, sid):
        return self._hyposids_by_sid.get(sid, set())

    def _get_hyponyms_rec(self, synset, cur_level, to_level):
        return self._get_nyms_rec(synset, cur_level, to_level,
                                  lambda x: self._get_hyposids(x))

    def get_synsets(self, lemma):
        """Возвращает синсеты, содержащие заданную лемму..

        Args:
            lemma: строка, нормализованное слово из русского языка.

        Returns:
            Список синсетов, содержащих заданное слово.
        """
        sids = self._synsetids_by_lemma.get(lemma, set())
        return [self._synsets_by_sid[s] for s in sids]

    def get_hypernyms(self, synset):
        """Возвращает гиперонимы первого уровня синсета synset.
           Гипероним первого уровня -- это самый близкий гипероним.
           Например, в цепочке собака -> млекопитающее ->
                               позвоночное -> животное
           слово "млекопитающее" -- гипероним первого уровня слова "собака",
           слово "позвоночное" -- гипероним второго уровня,
           "животное" -- третьего, и т.д.

        Args:
            synset: объект типа Synset, чьи гиперонимы нужно найти.

        Returns:
            Множество объектов типа Synset.
        """
        sid = synset._id
        return {self._synsets_by_sid[s] for s in self._get_hypersids(sid)}

    def get_hyponyms(self, synset):
        """Возвращает гипонимы первого уровня синсета synset.
           Гипоним первого уровня -- это самый близкий гипоним.
           Например, в цепочке собака -> млекопитающее ->
                               позвоночное -> животное
           слово "позвоночное" -- гипоним первого уровня слова "животное",
           слово "млекопитающее" -- гипоним второго уровня,
           "собака" -- третьего, и т.д.

        Args:
            synset: объект типа Synset, чьи гипонимы нужно найти.

        Returns:
            Множество объектов типа Synset.
        """
        sid = synset._id
        return {self._synsets_by_sid[s] for s in self._get_hyposids(sid)}

    def get_common_hypernyms(self, syn1, syn2, max_level=10):
        """Возвращает общие гиперонимы синсетов syn1 и syn2
           уровня не более чем max_level.

        Args:
            syn1: объект типа Synset, чьи гиперонимы нужно найти.
            syn2: объект типа Synset, чьи гиперонимы нужно найти.
            max_level: int, default=10, максимальный уровень
                поиска гиперонимов.

        Returns:
            Список туплей вида (level1, level2, hyper_synset), в котором
                level1 и level2 -- int, уровни гиперонима по отношению
                    к syn1 и syn2 соответственно,
                hyper_synset -- объект типа Synset, общий гипероним
                    синсетов syn1 и syn2.
        """
        return self._get_common(syn1, syn2, max_level, self._get_hypernyms_rec)

    def get_common_hyponyms(self, syn1, syn2, max_level=10):
        """Возвращает общие гипонимы синсетов syn1 и syn2
           уровня не более чем max_level.

        Args:
            syn1: объект типа Synset, чьи гипонимы нужно найти.
            syn2: объект типа Synset, чьи гипонимы нужно найти.
            max_level: int, default=10, максимальный уровень
                поиска гипонимов.

        Returns:
            Список туплей вида (level1, level2, hypo_synset), в котором
                level1 и level2 -- int, уровни гипонима по отношению
                    к syn1 и syn2 соответственно,
                hypo_synset -- объект типа Synset, общий гипоним
                    синсетов syn1 и syn2.
        """
        return self._get_common(syn1, syn2, max_level, self._get_hyponyms_rec)

    def _get_lowest_common_nyms(self, synset1, synset2, nym_fun, max_level=10):
        common_nyms = nym_fun(synset1, synset2, max_level=max_level)
        min_level = min([a + b for cn, a, b in common_nyms])
        return [cn for cn in common_nyms if cn[1] + cn[2] == min_level]

    def get_lowest_common_hypernyms(self, synset1, synset2, max_level=10):
        """Возвращает ближайший общий гипероним синсетов syn1 и syn2
           уровня не более чем max_level.

        Args:
            syn1: объект типа Synset, чей гипероним нужно найти.
            syn2: объект типа Synset, чей гипероним нужно найти.
            max_level: int, default=10, максимальный уровень
                поиска гиперонимов.

        Returns:
            Список туплей вида (level1, level2, hyper_synset), в котором
                level1 и level2 -- int, уровни гиперонима по отношению
                    к syn1 и syn2 соответственно,
                hyper_synset -- объект типа Synset, общий гипероним
                    синсетов syn1 и syn2.
        """
        return self._get_lowest_common_nyms(synset1, synset2,
                                            self.get_common_hypernyms,
                                            max_level)

    def get_lowest_common_hyponyms(self, synset1, synset2, max_level=10):
        """Возвращает ближайший общий гипоним синсетов syn1 и syn2
           уровня не более чем max_level.

        Args:
            syn1: объект типа Synset, чей гипоним нужно найти.
            syn2: объект типа Synset, чей гипоним нужно найти.
            max_level: int, default=10, максимальный уровень
                поиска гипонимов.

        Returns:
            Список туплей вида (level1, level2, hypo_synset), в котором
                level1 и level2 -- int, уровни гипонима по отношению
                    к syn1 и syn2 соответственно,
                hypo_synset -- объект типа Synset, общий гипоним
                    синсетов syn1 и syn2.
        """
        return self._get_lowest_common_nyms(synset1, synset2,
                                            self.get_common_hyponyms,
                                            max_level)

