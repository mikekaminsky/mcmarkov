import psycopg2
from collections import defaultdict
from itertools import count
from functools import partial
import numpy as np
import itertools as it

conn_string = "host='localhost' dbname='rhymes' user='michaelkaminsky'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

def getlyrics(artist):
    SQL = "SELECT lyrics from lyrics join songs on lyrics.song_id = songs.id where artist = %s;" # Note: no quotes
    data = (artist, )
    cur.execute(SQL, data)
    lyrics = cur.fetchall()
    return lyrics

class MarkovChain:
    # based on:
    # https://github.com/superbly/markov_chain/blob/master/MarkovChain.py
    def __init__(self, corpus, n_order=1):
        self.n_order = n_order

        # Dictionary for numbers -> words (we want to manipulate a list of integers for convenience)
        self.numbertoword = {i: label for i, label in enumerate(set(corpus),0)}
        
        # Dictionary for words -> numbers (we need this to create the numerified corpus
        self.wordtonumber = {v: k for k, v in self.numbertoword.items()}
        self.numerifiedcorpus = [self.wordtonumber[word] for word in corpus]

        n_states = len(self.numbertoword) 
        if n_order == 1:
            self.x, self.y = range(n_states)
        else:
            self.x = range(n_states)
            self.y = list(it.product(range(n_states), repeat=n_order))
        nx = len(self.x)
        ny = len(self.y)
        self.p = np.zeros((ny, nx))

    def fit(self):
        states = self.numerifiedcorpus
        # Count frequency of different states
        if self.n_order == 1:
            for i in xrange(0,len(states)-1):
                xloc = states[i]
                yloc = states[i+1]
                self.p[yloc][xloc] += 1
        else:
            for i in xrange(n_order,len(states)):
                xloc = states[i]
                yloc = self.y.index(tuple(states[i-n_order:i]))
                self.p[yloc][xloc] += 1
        for i in xrange(0, self.p.shape[0]):
            row = self.p[i]
            t = row.sum()
            if t <> 0:
                self.p[i] = row/t
        return self.p, self.numbertoword, self.numerifiedcorpus

    #def nextWord(self, precendingtext=''):



#corpus = getlyrics('eminem')
corpus = ['a','b','a','a','b','a','b']
mc = MarkovChain(corpus, 2)
myp, myd, myc = mc.fit()
print myc
print myp
