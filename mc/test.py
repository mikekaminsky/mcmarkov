import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from mc import MCMarkov

class TestMC(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['alpha','beta','gamma','delta','alpha','gamma','epsilon'],
                ['alef','bet','gimel','dalet','alef','gimel']
                        ]
        self.flattened_corpus = [item for sublist in self.corpus for item in sublist]

    def test_MC_creates_MarkovChain_object(self):
        MC = MCMarkov(self.corpus, 1, True)
        self.assertEqual(hasattr(MC, 'markovchain'), True)

    def test_reverse_list(self):
        MC = MCMarkov(self.corpus, 1, True)
        self.assertEqual(MC.corpus[0],list(reversed(self.corpus[0])))
        self.assertEqual(MC.corpus[1],list(reversed(self.corpus[1])))

    def test_starting_words(self):
        MC = MCMarkov(self.corpus, 1, True)
        self.assertEqual(MC.starting_words,['epsilon','gimel'])


if __name__ == '__main__':
    unittest.main()
