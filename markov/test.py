import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from markov import MarkovChain
from markov import ProbMatrix
from markov import create_sequence_list

class TestSequenceList(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['alpha','beta','gamma','delta','alpha','gamma','epsilon'],
                ['alef','bet','gimel','dalet','alef','gimel']
                ]

        self.short_corpus = [
                ['alpha','beta','gamma'],
                ['alef','bet','gimel']
                ]

    def test_sequence_length_one_returns_distinct_words(self):
        sequences = create_sequence_list(self.corpus, 1)
        self.assertEqual(set(sequences), set([(x,) for y in self.corpus for x in y]))
        self.assertEqual(len(sequences), len(set([(x,) for y in self.corpus for x in y])))

    def test_sequence_length_two_returns_distinct_observed_ngrams(self):
        sequences = create_sequence_list(self.short_corpus, 2)
        self.assertEqual(set(sequences), set([
            ('alpha', 'beta'),
            ('beta', 'gamma'),
            ('alef','bet'),
            ('bet','gimel')]))

class TestProbMatrix(unittest.TestCase):

    def test_dimensions(self):
        x = [1, 2, 3]
        y = [4, 5, 6, 99, 1000, 10001]
        p = ProbMatrix(x,y,1)
        self.assertEqual(p.p.shape,(3,6))
        self.assertEqual(p.order,1)
        self.assertEqual(p.x,x)
        self.assertEqual(p.y,y)

class TestMarkovChain(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['alpha','beta','gamma','delta','alpha','gamma','epsilon'],
                ['alef','bet','gimel','dalet','alef','gimel']
                        ]
        self.flattened_corpus = [item for sublist in self.corpus for item in sublist]

    def test_inverse_dictionaries(self):
        """
        Check if the number_to_word and word_to_number dictionaries are
        inverses of each other
        """
        mc = MarkovChain(self.corpus, 1)
        inv_number_to_word = {v: k for k, v in mc.number_to_word.items()}
        inv_word_to_number = {v: k for k, v in mc.word_to_number.items()}
        self.assertEqual(inv_number_to_word, mc.word_to_number)
        self.assertEqual(inv_word_to_number, mc.number_to_word)

    def test_numerified_corpus(self):
        """
        Check if the numerified corpus is the same length and has the same
        number of unique values as the original corpus
        """
        mc = MarkovChain(self.corpus, 1)
        self.assertEqual(len(mc.numerified_corpus),len(self.corpus))
        self.assertEqual(len(set([item for sublist in mc.numerified_corpus for item in sublist])),len(set(self.flattened_corpus)))

    def test_fits_sum_to_one(self):
        mc = MarkovChain(self.corpus, 1)
        mc.fit()
        p = mc.matrix_list[0].p
        self.assertEqual(sum(p[mc.convert_word_to_number('alpha')]),1)
        self.assertEqual(sum(p[mc.convert_word_to_number('beta')]),1)
        self.assertEqual(sum(p[mc.convert_word_to_number('gamma')]),1)
        self.assertEqual(sum(p[mc.convert_word_to_number('delta')]),1)

    def test_finds_highest_order_solution_first(self):
        mc = MarkovChain(self.corpus, 3)
        mc.fit()
        nextw = mc.next_word(['alpha','beta','gamma'])
        self.assertEqual(nextw, 'delta')

    def test_second_best_solution_next(self):
        mc = MarkovChain(self.corpus, 3)
        mc.fit()
        # TODO: Make sure it tests for beta delta together first?
        nextw = mc.next_word(['beta','delta'])
        self.assertEqual(nextw, 'alpha')

    def test_only_observed_ngrams_in_higher_order_matrices(self):
        small_corpus = [['alpha','beta','gamma','delta']]
        mc = MarkovChain(small_corpus, 2)
        # x values should be
        ## [('alpha', 'beta'), ('beta', 'gamma'), ('gamma', 'delta')]
        self.assertEqual(mc.matrix_list[0].p.shape, (3,4))

    def test_probs_stop_across_lines(self):
        mc = MarkovChain(self.corpus, 3)
        mc.fit()
        nextw = mc.next_word(['alpha','epsilon'])
        self.assertEqual(nextw, '\n') # Nothing follows epsilon

if __name__ == '__main__':
    unittest.main()

