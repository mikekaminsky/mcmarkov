import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import random

from markov.markov import MarkovChain
from rhymes.rhymes import rhymesyls
from rhymes.rhymes import nsyl


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
        self.reverse = reverse
        self.markovchain = MarkovChain(self.corpus, n_order)
        self.markovchain.fit()
        self.starting_words = [line[0] for line in self.corpus]
        self.rhymedict = {}
        for word in self.starting_words:
            keys = rhymesyls(word)
            for key in keys:
                if key in self.rhymedict:
                    self.rhymedict[key].append(word)
                else:
                    self.rhymedict[key] = [word]
        self.words_to_rhyme = {}
        for key in self.rhymedict.keys():
            if len(set(self.rhymedict[key]))>1:
                self.words_to_rhyme[key] = self.rhymedict[key]


    def create_line(self, startingword, syllable_count): # To be changed to syllable count
        line = [startingword]
        remaining_syllable_count = syllable_count - nsyl(startingword)
        i = 0
        while remaining_syllable_count > 0:
            if i == 0:
                word = self.markovchain.next_word([startingword])
            else:
                word = self.markovchain.next_word([word])
            if nsyl(word) <= remaining_syllable_count:
                line.append(word)
                remaining_syllable_count -= nsyl(word)
                i += 1
        if self.reverse:
            line = line[::-1]
        return line

    def create_song(self, couplets, syllable_count):
        song = []
        for i in range(0,couplets):
            rhymewords = set(self.words_to_rhyme[random.choice(self.words_to_rhyme.keys())])
            thisrhymes = random.sample(rhymewords,2)
            startingword1 = thisrhymes[0]
            startingword2 = thisrhymes[1]
            line1 = self.create_line(startingword1, syllable_count)
            line2 = self.create_line(startingword2, syllable_count)
            couplet = [line1, line2]
            song.append(couplet)
        return song
