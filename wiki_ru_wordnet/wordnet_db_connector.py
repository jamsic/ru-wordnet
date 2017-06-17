import sqlite3
import os
from collections import defaultdict


class Wordnet_dbconnector:

    DIRECTORY = 'wordnet'
    DB_NAME = 'wordnet.db'

    def __init__(self, directory=None):
        if not directory:
            directory = self.DIRECTORY
        filename = os.path.join(directory, self.DB_NAME)
        filename = os.path.join(os.path.dirname(__file__), filename)
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''PRAGMA foreign_keys = ON;''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS words(
                            id INTEGER PRIMARY KEY,
                            word TEXT NOT NULL,
                            lang TEXT NOT NULL,
                            meaning TEXT  NOT NULL,
                            UNIQUE(word, lang, meaning)
                            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS hyperonyms(
                            sid INTEGER NOT NULL,
                            hypersid INTEGER  NOT NULL,
                            FOREIGN KEY(sid) REFERENCES synsets(id),
                            FOREIGN KEY(hypersid) REFERENCES synsets(id)
                            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS synsets(
                            id INTEGER PRIMARY KEY
                            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS wordtosynset(
                            word_id INTEGER NOT NULL,
                            synset_id INTEGER  NOT NULL,
                            FOREIGN KEY(word_id) REFERENCES words(id),
                            FOREIGN KEY(synset_id) REFERENCES synsets(id)
                            );''')
        self.db.commit()

    def __del__(self):
        self.db.close()

    def _get_ans(self, query):
        self.cur.execute(*query)
        ans = self.cur.fetchall()
        return ans

    def commit_all(self):
        self.db.commit()

    def get_words_count(self):
        query = 'select count(*) from words',
        return self._get_ans(query)

    def get_synset_count(self):
        query = 'select count(*) from synsets',
        return self._get_ans(query)

    def _get_table(self, tablename):
        query = 'SELECT * FROM {0}'.format(tablename),
        return self._get_ans(query)

    def get_hyperonym_links(self):
        table = 'hyperonyms'
        return self._get_table(table)

    def get_wordtosynset(self):
        table = 'wordtosynset'
        return self._get_table(table)

    def get_words(self):
        table = 'words'
        return self._get_table(table)

    def delete_sid(self, sid):
        query = 'delete from hyperonyms where hypersid=? or sid=?', (sid, sid)
        self.cur.execute(*query)
        query = 'delete from wordtosynset where synset_id=?', (sid,)
        self.cur.execute(*query)
        query = 'delete from synsets where id=?', (sid,)
        self.cur.execute(*query)
        self.commit_all()

    def delete_hyperlinks(self, hyperlinks):
        query = 'delete from hyperonyms where sid=? and hypersid=?'
        self.cur.executemany(query, hyperlinks)
        self.commit_all()

