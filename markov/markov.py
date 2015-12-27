import numpy as np
import itertools as it
import random

# TODO:
## Check that arguments are correct (e.g., list of lists instead of lists) to prevent
## stupid programming errors

def create_sequence_list(lines, order):
    """
    Returns a list of tuples that reflect the distinct ngrams
    (where n is the order) obsvered in the lines (list of lists).
    """
    answer = set()
    for line in lines:
        for i in xrange(order,len(line)+1):
            answer.add(tuple(line[i-order:i]))
    return list(answer)

class ProbMatrix:
    """
        This class holds the probability matrix data crucial to building
        these models. They take the following form where (x_i, y_j) contains
        the likelihood of word y_i following the words contained in the
        tuple x_j

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
    def __init__(self, corpus, n_order=1):
        # corpus is a list of lists
        self.n_order = n_order
        # Dictionary for numbers -> words (we want to manipulate a list of integers for calculation speed)
        self.number_to_word = {i: label for i, label in enumerate(set([item for sublist in corpus for item in sublist]),0)}
        # Dictionary for words -> numbers (we need this to create the numerified corpus
        self.word_to_number = {v: k for k, v in self.number_to_word.items()}
        # This is integer-only version of the corpus we passed in. May make things faster???
        self.numerified_corpus = [[self.word_to_number[word] for word in line] for line in corpus]
        self.matrix_list = []
        self.observed_sequence_lists = []

        for i in range(self.n_order, 0, -1):
            this_sequence_list = create_sequence_list(self.numerified_corpus,i)
            x = range(len(this_sequence_list))
            y = range(len(self.number_to_word))
            p = ProbMatrix(x, y, i)

            self.observed_sequence_lists.append(this_sequence_list)
            self.matrix_list.append(p)

    def convert_word_to_number(self, word):
        if word in self.word_to_number:
            return self.word_to_number[word]
        else:
            print word
            raise ValueError('This word ("'+word+'") isn\'t in the corpus')

    def fit(self):
        """
        This is definitely the most computationally intensive piece of this
        application.
            TODO:
                * Parallelize?
                * Split out frequency calculation from normalization?
        """
        for i in range(0, self.n_order):
            this_prob = self.matrix_list[i]
            this_order = this_prob.order
            this_sequence_list = self.observed_sequence_lists[i]
            # Calculate Frequencies
            for j in xrange(0,len(self.numerified_corpus)):
                this_list = self.numerified_corpus[j]
                for k in xrange(this_order,len(this_list)):
                    xloc = this_sequence_list.index(tuple(this_list[k-this_order:k]))
                    yloc = this_list[k]
                    this_prob.p[xloc][yloc] += 1
            # Normalize
            for j in xrange(0, this_prob.p.shape[0]):
                row = this_prob.p[j]
                t = row.sum()
                if t <> 0:
                    this_prob.p[j] = row/t
        return self.matrix_list

    def next_word(self, preceding_text=[]):
        # TODO:
        # Create a separate data structure that stores the *first word*
        # in a line from the corpus, then chooses among *those*
        if (not preceding_text) or (preceding_text == ['\n']):
            preceding_text = [random.choice(self.word_to_number.keys())]
        preceding_numbers = [self.convert_word_to_number(word) for word in preceding_text]

        for i in range(0, self.n_order):
            this_sequence_list = self.observed_sequence_lists[i]
            if self.matrix_list[i].order > len(preceding_numbers):
                continue
            if self.matrix_list[i].order < len(preceding_numbers):
                preceding_numbers = preceding_numbers[-self.matrix_list[i].order:]
            this_prob = self.matrix_list[i]
            this_order = this_prob.order
            if tuple(preceding_numbers) in this_sequence_list:
                probs = this_prob.p[this_sequence_list.index(tuple(preceding_numbers)),:]
            else:
                continue
            sample = random.random()
            max_prob = 0.0
            max_prob_word = None
            for j in range(0, len(probs)):
                if probs[j] > max_prob:
                    max_prob = probs[j]
                    max_prob_word = j
                if sample > probs[j]:
                    sample -= probs[j]
                else:
                    return self.number_to_word[j]
            if max_prob_word:
                return self.number_to_word[max_prob_word]
        return '\n' # We get to here when we get to a word where we never observe any following words (e.g., if the last word in the line only appears last)
