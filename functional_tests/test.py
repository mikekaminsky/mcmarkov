import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from markov.markov import MarkovChain
from mc.mc import MCMarkov

class TestMC(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['a','b','c','a','b','c'],
                ['alef','bet','gimel','alef','bet','gimel']
                    ]

    def test_reverse_lines(self):
        MC = MCMarkov(self.corpus, 1, True)
        mc = MC.markovchain
        # First line
        self.assertEqual(mc.next_word(['b']),'a')
        self.assertEqual(mc.next_word(['c']),'b')
        self.assertEqual(mc.next_word(['a']),'c')

        # Second line
        self.assertEqual(mc.next_word(['bet']),'alef')
        self.assertEqual(mc.next_word(['gimel']),'bet')
        self.assertEqual(mc.next_word(['alef']),'gimel')

class TestMarkov(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['a','b','c','a','b','c'],
                ['alef','bet','gimel','alef','bet','gimel']
                    ]

    def test_no_word(self):
        # If no word is passed, markov should return something
        # TODO: Test this is actually random?
        mc = MarkovChain(self.corpus, 1)
        mc.fit()
        self.assertNotEqual(mc.next_word([]),None)

    def test_no_match(self):
        #TODO: Make it so the markov chain always generates something?
        mc = MarkovChain(self.corpus, 1)
        mc.fit()
        self.assertRaises(ValueError, mc.next_word, ['d'])

    def test_single_word(self):
        mc = MarkovChain(self.corpus, 1)
        mc.fit()

        # First line
        self.assertEqual(mc.next_word(['a']),'b')
        self.assertEqual(mc.next_word(['b']),'c')
        self.assertEqual(mc.next_word(['c']),'a')

        # Second line
        self.assertEqual(mc.next_word(['alef']),'bet')
        self.assertEqual(mc.next_word(['bet']),'gimel')
        self.assertEqual(mc.next_word(['gimel']),'alef')


    def test_double_word_found(self):
        # It should look for a match to both a & b first,
        mc = MarkovChain(self.corpus, 2)
        mc.fit()
        self.assertEqual(mc.next_word(['a','b']),'c')
        self.assertEqual(mc.next_word(['b','c']),'a')
        self.assertEqual(mc.next_word(['alef','bet']),'gimel')
        self.assertEqual(mc.next_word(['bet','gimel']),'alef')

    def test_double_word_not_found(self):
        # It should look for a match to both a & c first,
        # and when it doesn't find anything, should return the match for c
        mc = MarkovChain(self.corpus, 2)
        mc.fit()
        self.assertEqual(mc.next_word(['a','c']),'a')
        self.assertEqual(mc.next_word(['alef','gimel']),'alef')

if __name__ == '__main__':
    unittest.main()
