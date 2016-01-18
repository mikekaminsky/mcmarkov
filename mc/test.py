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

    def test_starting_word_rhyme_dictionary_contains_all_first_words(self):
        MC = MCMarkov(self.corpus, 1, True)
        rhymedict_values = MC.rhymedict.values()
        self.assertEqual(set([item for sublist in rhymedict_values for item in sublist]), set([item for sublist in self.corpus for item in sublist]))

    def test_starting_word_rhyme_dictionary_can_have_multiple_pronunciations(self):
        MC = MCMarkov([['hated'],['mated']], 1, True)
        rhymedict_values = [item for sublist in MC.rhymedict.values() for item in sublist]
        self.assertGreater(rhymedict_values.count('hated'),1)

    def test_chooses_random_starting_rhyme_with_at_least_two_words(self):
        pass

    def test_chooses_random_starting_word_from_rhyme_group(self):
        pass

    def test_rhymes_within_couplet(self):
        pass

    def test_same_word_does_not_end_adjacent_lines(self):
        pass

    def test_corpus_must_have_at_least_two_rhyming_starting_words(self):
        pass

    def test_all_words_in_corpus_have_syllable_count(self):
        pass


if __name__ == '__main__':
    unittest.main()
