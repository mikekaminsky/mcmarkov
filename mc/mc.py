import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from markov.markov import MarkovChain


# TODO:
#  [ ] Ability to end the next line with a word that rhymes with the last word of the previosu line
#     [ ] Create dictionary of rhymes for last-words that are used as 'seeds'
#         * How to handle frequency? Should the list be unique, or should it reflect observed frequency?
#     [ ] Write a method for choosing a rhyming word that rhymed with the last line but is not the same word
#     [ ] Write a method for building raps using couplets
#  [ ] Ability to specify the syllable count of a line
#  [ ] Option to 'clean' the corpus by removing certain punctuation

class MCMarkov():

    def __init__(self, corpus, n_order=1, reverse=True):
        if reverse:
            self.corpus = [line[::-1] for line in corpus]
        else:
            self.corpus = corpus
        self.markovchain = MarkovChain(self.corpus, n_order)
        self.markovchain.fit()
        self.starting_words = [line[0] for line in self.corpus]
        self.rhymedict = {}



    def create_song(self, couplets, syllables):
        pass
