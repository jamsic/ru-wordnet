from wordnet_db_connector import Wordnet_dbconnector
from word import Word
from collections import defaultdict
from synset import Synset


class Wordnet:

    def __init__(self):
        self.dbcon = Wordnet_dbconnector()
        self.load_info()

    def load_info(self):
        words_db = self.dbcon.get_words()
        wordtosynset_db = self.dbcon.get_wordtosynset()
        hyperonym_links_db = self.dbcon.get_hyperonym_links()
        self.words, self.wids_by_word = self.process_words(words_db)
        self.synsets, self.sids_by_wid = self.process_wordtosynset(wordtosynset_db)
        self.hyperonyms, self.hyponyms = self.process_hyperonym_links(hyperonym_links_db)

    def process_words(self, words_db):
        words = {}
        for word in words_db:
            words[word[0]] = Word(word)
        wids_by_word = defaultdict(set)
        for wid, word in words.items():
            wids_by_word[word.word].add(wid)
        return words, dict(wids_by_word)

    def process_wordtosynset(self, wordtosynset):
        synsets = defaultdict(set)
        for wid, sid in wordtosynset:
            synsets[sid].add(wid)
        sids_by_wid = {}
        for sid in synsets:
            synsets[sid] = Synset(sid, {self.words[wid] for wid in synsets[sid]})
        for sid in synsets:
            for word in synsets[sid].words:
                sids_by_wid[word.id] = sid
        return dict(synsets), sids_by_wid

    def process_hyperonym_links(self, hyperonym_links):
        hyperonyms = defaultdict(set)
        hyponyms = defaultdict(set)
        for sid, hypersid in hyperonym_links:
            hyperonyms[sid].add(hypersid)
            hyponyms[hypersid].add(sid)
        return dict(hyperonyms), dict(hyponyms)

    def get_bottom_nodes(self):
        return {sid for sid in self.synsets if sid not in self.hyponyms}

    def get_top_nodes(self):
        return {sid for sid in self.synsets if sid not in self.hyperonyms}

    def get_sids(self, word):
        return {self.sids_by_wid[w] for w in self.wids_by_word.get(word, [])}

    def get_words(self, word):
        return {self.words[w] for w in self.wids_by_word.get(word, [])}

    def _get_hyperonyms(self, sid):
        return self.hyperonyms.get(sid, set())

    def _get_hyponyms(self, sid):
        return self.hyponyms.get(sid, set())

    def get_synset_by_id(self, sid):
        return self.synsets.get(sid)

    def get_synsets(self, word):
        sids = self.get_sids(word)
        return [self.get_synset_by_id(s) for s in sids]

    def get_common(self, syn1, syn2, max_level, nym_fun):
        nyms1 = nym_fun(syn1, 0, max_level)
        nyms2 = nym_fun(syn2, 0, max_level)
        nymdct1 = {synset: level for level, synset in nyms1}
        nymdct2 = {synset: level for level, synset in nyms2}
        common_nyms = nymdct1.keys() & nymdct2.keys()
        common_nyms_ = []
        for ch in common_nyms:
            common_nyms_.append((ch, nymdct1[ch], nymdct2[ch]),)
        if common_nyms_:
            min_level = min([a + b for s, a, b in common_nyms_])
            return list(filter(lambda x: x[1] + x[2] == min_level, common_nyms_))

    def get_synwords(self, synset):
        return {w.word for w in synset.words}

    def common_hyperonyms(self, syn1, syn2, max_level=10):
        return self.get_common(syn1, syn2, max_level, self.get_hyperonyms_rec)

    def common_hyponyms(self, syn1, syn2, max_level=10):
        return self.get_common(syn1, syn2, max_level, self.get_hyponyms_rec)

    # TO DO replace with smth normal
    def get_nyms_rec(self, synset, cur_level, to_level, nym_fun):
        hyps = {(cur_level, synset)}
        if cur_level < to_level:
            for hypsynset in nym_fun(synset):
                hyps.update(self.get_nyms_rec(hypsynset, cur_level + 1, to_level, nym_fun))
        return hyps

    def get_hyperonyms_rec(self, synset, cur_level, to_level):
        return self.get_nyms_rec(synset, cur_level, to_level, self.get_hyperonyms)

    def get_hyponyms_rec(self, synset, cur_level, to_level):
        return self.get_nyms_rec(synset, cur_level, to_level, self.get_hyponyms)

    def get_hyperonyms(self, synset):
        sid = synset.id
        return {self.get_synset_by_id(s) for s in self._get_hyperonyms(sid)}

    def get_hyponyms(self, synset):
        sid = synset.id
        return {self.get_synset_by_id(s) for s in self._get_hyponyms(sid)}

