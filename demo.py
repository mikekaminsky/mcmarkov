from mc.mc import MCMarkov
import pickle

corpus = pickle.load(open( "eminemcorpus.pickle", "rb" ) )
mc = MCMarkov(corpus, 4, True)
new_song = mc.create_song(couplet_count=10, syllable_count=10)

for couplet in new_song:
    for line in couplet:
        print ' '.join(line)
