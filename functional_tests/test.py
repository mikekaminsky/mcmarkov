import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from markov.markov import MarkovChain


class TestMarkov(unittest.TestCase):

    def setUp(self):
        self.corpus = ['a','b','c','a','b','c']

    def test_no_word(self):
        # If no word is passed, markov should return something
        # TODO: Test this is actually random?
        mc = MarkovChain(self.corpus, 1)
        mymatlist = mc.fit()
        self.assertNotEqual(mc.nextWord([]),None)

    def test_no_match(self):
        #TODO: Make it so the markov chain always generates something?
        mc = MarkovChain(self.corpus, 1)
        mymatlist = mc.fit()
        self.assertRaises(ValueError, mc.nextWord, ['d'])

    def test_single_word(self):
        mc = MarkovChain(self.corpus, 1)
        mymatlist = mc.fit()
        self.assertEqual(mc.nextWord(['a']),'b')
        self.assertEqual(mc.nextWord(['b']),'c')
        self.assertEqual(mc.nextWord(['c']),'a')

    def test_double_word_found(self):
        # It should look for a match to both a & b first, 
        mc = MarkovChain(self.corpus, 2)
        mymatlist = mc.fit()
        self.assertEqual(mc.nextWord(['a','b']),'c')
        self.assertEqual(mc.nextWord(['b','c']),'a')

    def test_double_word_not_found(self):
        # It should look for a match to both a & c first, 
        # and when it doesn't find anything, should return the match for c
        mc = MarkovChain(self.corpus, 2)
        mymatlist = mc.fit()
        self.assertEqual(mc.nextWord(['a','c']),'a')

if __name__ == '__main__':
    unittest.main()
