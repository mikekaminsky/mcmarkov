from markov.markov import MarkovChain
import pickle

corpus = pickle.load(open( "eminemcorpus.pickle", "rb" ) )
mc = MarkovChain(corpus, 4)
print "Fitting..."
mc.fit()
print "Fit complete!"

generated_lyrics = []
word = None
print('starting lyric generation!')
for i in range(0,50):
    print i
    if word:
        # NOTE: this argument has to a be a list
        word = mc.next_word([word])
        print word
    else:
        word = mc.next_word()
        print word
    generated_lyrics.append(word)

print(generated_lyrics)
