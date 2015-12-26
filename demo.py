from markov.markov import MarkovChain
import pickle

corpus = pickle.load(open( "eminemcorpus.pickle", "rb" ) )
mc = MarkovChain(corpus, 2)
print "Fitting..."
mc.fit()
print "Fit complete!"

generated_lyrics = []
word = None
for i in range(0,10):
    if word:
        # NOTE: this argument has to a be a list
        word = mc.next_word([word])
    else:
        word = mc.next_word()
    print word
    generated_lyrics.append(word)
