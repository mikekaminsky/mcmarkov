import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from mc import MCMarkov
from rhymes.rhymes import rhymes_with

class TestMC(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['alpha','beta','gamma','delta','alpha','gamma','epsilon'],
                ['alef','bet','gimel','dalet','alef','gimel']
                        ]

        self.where_the_sidewalk_ends = [
                    ['there', 'is', 'a', 'place', 'where', 'the', 'sidewalk', 'ends'],
                    ['and', 'before', 'the', 'street', 'begins'],
                    ['and', 'there', 'the', 'grass', 'grows', 'soft', 'and', 'white'],
                    ['and', 'there', 'the', 'sun', 'burns', 'crimson', 'bright'],
                    ['and', 'there', 'the', 'moon-bird', 'rests', 'from', 'his', 'flight'],
                    ['to', 'cool', 'in', 'the', 'peppermint', 'wind'],
                    ['let', 'us', 'leave', 'this', 'place', 'where', 'the', 'smoke', 'blows', 'black'],
                    ['and', 'the', 'dark', 'street', 'winds', 'and', 'bends'],
                    ['past', 'the', 'pits', 'where', 'the', 'asphalt', 'flowers', 'grow'],
                    ['we', 'shall', 'walk', 'with', 'a', 'walk', 'that', 'is', 'measured', 'and', 'slow'],
                    ['and', 'watch', 'where', 'the', 'chalk-white', 'arrows', 'go'],
                    ['to', 'the', 'place', 'where', 'the', 'sidewalk', 'ends'],
                    ['yes', "we'll", 'walk', 'with', 'a', 'walk', 'that', 'is', 'measured', 'and', 'slow'],
                    ['and', "we'll", 'go', 'where', 'the', 'chalk-white', 'arrows', 'go'],
                    ['for', 'the', 'children,', 'they', 'mark,', 'and', 'the', 'children,', 'they', 'know'],
                    ['the', 'place', 'where', 'the', 'sidewalk', 'ends']
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
        self.assertEqual(set([item for sublist in rhymedict_values for item in sublist]), set(MC.starting_words))

    def test_starting_word_rhyme_dictionary_can_have_multiple_pronunciations(self):
        MC = MCMarkov([['hated'],['mated']], 1, True)
        rhymedict_values = [item for sublist in MC.rhymedict.values() for item in sublist]
        self.assertGreater(rhymedict_values.count('hated'),1)

    def test_words_to_rhyme_all_have_two_words(self):
        MC = MCMarkov([['hated'],['mated'],['boat']], 1, True)
        self.assertFalse('boat' in [item for sublist in MC.words_to_rhyme.values() for item in sublist])
        self.assertTrue('hated' in [item for sublist in MC.words_to_rhyme.values() for item in sublist])
        self.assertTrue('mated' in [item for sublist in MC.words_to_rhyme.values() for item in sublist])

    def test_song_contains_correct_number_of_couplets(self):
        MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        song = MC.create_song(4, 10)
        self.assertEqual(len(song),4)

    def test_couplets_are_not_empty(self):
        MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        song = MC.create_song(4, 10)
        for couplet in song:
            for line in couplet:
                self.assertGreater(len(line),0)

    def test_rhymes_within_couplet(self):
        MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        song = MC.create_song(4, 10)
        for couplet in song:
            endword1 = couplet[0][-1]
            endword2 = couplet[1][-1]
            self.assertTrue(rhymes_with(endword1, endword2))

    def test_lines_in_couplet_do_not_end_with_same_word(self):
        MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        song = MC.create_song(4, 10)
        for couplet in song:
            endword1 = couplet[0][-1]
            endword2 = couplet[1][-1]
            self.assertNotEqual(endword1, endword2)

    def test_corpus_must_have_at_least_two_rhyming_starting_words(self):
        pass

if __name__ == '__main__':
    unittest.main()
