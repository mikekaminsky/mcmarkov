#test.py
from markov import MarkovChain

corpus = ['a','b','c','a','b','c']
mc = MarkovChain(corpus, 2)
mymatlist = mc.fit()

print(mc.nextWord(['a']))
print(mc.nextWord(['b']))
print(mc.nextWord(['c']))

# It should look for a match to both a & c first, 
# and when it doesn't find anything, should return the match for a
print(mc.nextWord(['a','c']))

