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
        self.starting_words = [line[0] for line in self.corpus]




        # TODO:
        # Create a separate data structure that stores the *first word*
        # in a line from the corpus, then chooses among *those*

