import numpy as np
import itertools as it

class ProbMatrix:
    """
        This class holds the probability matrix data crucial to building these models. They take the following form
        where (x_i, y_j) contains the likelihood of word x_i following the words contained in the tuple y_j
            x_0 x_1 ... x_n
        y_0
        y_1
        ...
        y_n
    """
    def __init__(self, x, y, order):
        self.x = x
        self.y = y
        self.order = order
        self.p = np.zeros((len(y), len(x)))
        
class MarkovChain:
    # TODO:
    # To choose the next word in the list, cycle through probability matrixes until you 
    # find one that contains some enty for the word
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
        for i in range(n_order, 0, -1):
            x = range(n_states)
            y = list(it.product(range(n_states), repeat=i))
            p = ProbMatrix(x, y, i)
            self.matrix_list.append(p)

    def fit(self):
        states = self.numerifiedcorpus
        for i in range(0, n_order):
            thisprob = self.matrix_list[i]
            thisorder = thisprob.order
            # Calculate Frequencies
            for j in xrange(thisorder,len(states)):
                xloc = states[j]
                yloc = thisprob.y.index(tuple(states[j-thisorder:j]))
                thisprob.p[yloc][xloc] += 1
            # Normalize
            for j in xrange(0, thisprob.p.shape[0]):
                row = thisprob.p[j]
                t = row.sum()
                if t <> 0:
                    thisprob.p[j] = row/t
        return self.matrix_list

    #def nextWord(self, precendingtext=''):

#corpus = getlyrics('eminem')
corpus = ['a','b','a','b']
mc = MarkovChain(corpus, 2)
mymatlist = mc.fit()
#myp, myd, myc = mc.fit()
#print myc
#print myp
