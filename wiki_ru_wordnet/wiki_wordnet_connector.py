import sqlite3
import os


class WikiWordnetConnector:
    
    DIRECTORY = 'database'
    DB_NAME = 'wikiwordnet.db'

    def __init__(self, directory=None):
        if not directory:
            directory = self.DIRECTORY
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, self.DB_NAME)
        filename = os.path.join(os.path.dirname(__file__), filename)
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS synsets(
                            synset_id INTEGER NOT NULL,
                            lemma TEXT NOT NULL,
                            definition TEXT NOT NULL,
                            UNIQUE(synset_id, lemma, definition)
                            );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS hypernyms(
                            sid INTEGER NOT NULL,
                            hypersid INTEGER NOT NULL,
                            UNIQUE(sid, hypersid)
                            );''')
        self.db.commit()

    def __del__(self):
        self.db.close()

    def _get_ans(self, query):
        self.cur.execute(*query)
        ans = self.cur.fetchall()
        return ans
    
    def insert_synsets(self, synsets):
        query = '''insert into synsets(synset_id, lemma, definition) values (?,?,?)'''
        self.cur.executemany(query, synsets)
        
    def insert_hypernyms(self, hypernyms):
        query = '''insert into hypernyms(sid, hypersid) values (?,?)'''
        self.cur.executemany(query, hypernyms)

    def _get_table(self, tablename):
        query = 'SELECT * FROM {0}'.format(tablename),
        return self._get_ans(query)

    def get_hypernyms(self):
        table = 'hypernyms'
        return self._get_table(table)

    def get_synsets(self):
        table = 'synsets'
        return self._get_table(table)

