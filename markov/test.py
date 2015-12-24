import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from markov import MarkovChain
from markov import ProbMatrix

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


        self.corpus =['alpha','beta','gamma','delta','alpha','gamma']

        #self.corpus = [
                #['alpha','beta','gamma','delta','alpha','gamma'],
                #['alef','bet','gimel','dalet','alef','gimel']
                        #]

    def test_inverse_dictionaries(self):
        """
        Check if the numbertoword and wordtonumber dictionaries are
        inverses of each other
        """
        mc = MarkovChain(self.corpus, 1)
        inv_number_to_word = {v: k for k, v in mc.numbertoword.items()}
        inv_word_to_number = {v: k for k, v in mc.wordtonumber.items()}
        self.assertEqual(inv_number_to_word, mc.wordtonumber)
        self.assertEqual(inv_word_to_number, mc.numbertoword)

    def test_numerified_corpus(self):
        """
        Check if the numerified corpus is the same length and has the same
        number of unique values as the original corpus
        """
        mc = MarkovChain(self.corpus, 1)
        self.assertEqual(len(mc.numerifiedcorpus),len(self.corpus))
        self.assertEqual(len(set(mc.numerifiedcorpus)),len(set(self.corpus)))

    def test_fits_sum_to_one(self):
        mc = MarkovChain(self.corpus, 1)
        mc.fit()
        p = mc.matrix_list[0].p
        self.assertEqual(sum(p[mc.convertwordtonumber('alpha')]),1)
        self.assertEqual(sum(p[mc.convertwordtonumber('beta')]),1)
        self.assertEqual(sum(p[mc.convertwordtonumber('gamma')]),1)
        self.assertEqual(sum(p[mc.convertwordtonumber('delta')]),1)

    def test_finds_highest_order_solution_first(self):
        mc = MarkovChain(self.corpus, 3)
        mc.fit()
        nextw = mc.nextWord(['alpha','beta','gamma'])
        self.assertEqual(nextw, 'delta')

    def test_second_best_solution_next(self):
        mc = MarkovChain(self.corpus, 3)
        mc.fit()
        # TODO: Make sure it tests for beta delta together first?
        nextw = mc.nextWord(['beta','delta'])
        self.assertEqual(nextw, 'alpha')



if __name__ == '__main__':
    unittest.main()

