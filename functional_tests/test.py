import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from markov.markov import MarkovChain
from mc.mc import MCMarkov
from rhymes.rhymes import nsyl, rhymes_with

class TestMC(unittest.TestCase):

    def setUp(self):
        self.corpus = [
                ['a','b','c','a','b','c'],
                ['alef','bet','gimel','alef','bet','gimel']
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

    def test_seed_words(self):
        MC = MCMarkov(self.corpus, 1, False)
        self.assertEqual(MC.starting_words,['a', 'alef'])

    def test_number_of_couplets(self):
        MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        new_song = MC.create_song(couplets=5, syllables=10)
        self.assertEqual(len(new_song),5)

    #def test_number_of_syllables(self):
        #MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        #new_song = MC.create_song(couplets=5, syllables=10)
        #for couplet in new_song:
            #for line in couplet:
                #sylcount = sum(nsyl(word) for word in line)
                #self.assertEqual(sylcount,10)

    def test_couplets_rhyme(self):
        MC = MCMarkov(self.where_the_sidewalk_ends, 1, True)
        new_song = MC.create_song(couplets=5, syllables=10)
        for couplet in new_song:
            endword1 = couplet[0][-1]
            endword2 = couplet[1][-1]
            self.assertTrue(rhymes_with(endword1, endword2))


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
