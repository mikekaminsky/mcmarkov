import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from markov.markov import MarkovChain

class MCMarkov():

    def __init__(self, corpus, n_order=1, reverse=True):
        if reverse:
            self.corpus = [line[::-1] for line in corpus]
        else:
            self.corpus = corpus
        self.markovchain = MarkovChain(self.corpus, n_order)
        self.markovchain.fit()
