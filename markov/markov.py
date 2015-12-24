import numpy as np
import itertools as it
import random

class ProbMatrix:
    """
        This class holds the probability matrix data crucial to building these models. They take the following form
        where (x_i, y_j) contains the likelihood of word y_i following the words contained in the tuple x_j
            y_0 y_1 ... y_n
        x_0
        x_1
        ...
        x_n
    """
    def __init__(self, x, y, order):
        self.x = x
        self.y = y
        self.order = order
        self.p = np.zeros((len(x), len(y)))
        
class MarkovChain:
    # TODO:
    # Need to be able to take in an enormous corpus that's broken into lines and create the probability matrices.
    ## To do this, we'll need to have some way of telling it what to do with multiple lines (i.e., don't treat the
    ## first word of the next line as following the last word of the previous line. 
    def __init__(self, corpus, n_order=1):
        self.n_order = n_order

        # Dictionary for numbers -> words (we want to manipulate a list of integers for convenience)
        self.numbertoword = {i: label for i, label in enumerate(set(corpus),0)}
        
        # Dictionary for words -> numbers (we need this to create the numerified corpus
        self.wordtonumber = {v: k for k, v in self.numbertoword.items()}

        # This is integer-only version of the corpus we passed in. May make things faster???
        self.numerifiedcorpus = [self.wordtonumber[word] for word in corpus]

        n_states = len(self.numbertoword) 

        self.matrix_list = [] 
        for i in range(self.n_order, 0, -1):
            x = list(it.product(range(n_states), repeat=i))
            y = range(n_states)
            p = ProbMatrix(x, y, i)
            self.matrix_list.append(p)

    def convertwordtonumber(self, word):
        if word in self.wordtonumber:
            return self.wordtonumber[word]
        else:
            raise ValueError('This word isn''t in the corpus')

    def fit(self):
        states = self.numerifiedcorpus
        for i in range(0, self.n_order):
            thisprob = self.matrix_list[i]
            thisorder = thisprob.order
            # Calculate Frequencies
            for j in xrange(thisorder,len(states)):
                xloc = thisprob.x.index(tuple(states[j-thisorder:j]))
                yloc = states[j]
                thisprob.p[xloc][yloc] += 1
            # Normalize
            for j in xrange(0, thisprob.p.shape[0]):
                row = thisprob.p[j]
                t = row.sum()
                if t <> 0:
                    thisprob.p[j] = row/t
        return self.matrix_list

    def nextWord(self, precendingtext=[]):
        # TODO:
        # Create a separate data structure that stores the *first word* in a line from the corpus, then 
        # Chooses among *those*
        if not precendingtext:
            precendingtext = [random.choice(self.wordtonumber.keys())]
        precedingnumbers = [self.convertwordtonumber(word) for word in precendingtext]

        for i in range(0, self.n_order):
            if self.matrix_list[i].order > len(precedingnumbers):
                continue
            if self.matrix_list[i].order < len(precedingnumbers):
                precedingnumbers = precedingnumbers[-self.matrix_list[i].order:]
            thisprob = self.matrix_list[i]
            thisorder = thisprob.order
            if tuple(precedingnumbers) in thisprob.x:
                probs = thisprob.p[thisprob.x.index(tuple(precedingnumbers)),:]
            else:
                continue
            sample = random.random()
            maxprob = 0.0
            maxprobword = None
            for j in range(0, len(probs)):
                if probs[j] > maxprob:
                    maxprob = probs[j]
                    maxprobword = j
                if sample > probs[j]:
                    sample -= probs[j]
                else:
                    return self.numbertoword[j]
            if maxprobword:
                return self.numbertoword[maxprobword]
        return None
