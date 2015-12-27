# mcmarkov

MC Markov is a python application for generating new text based on a corpus of observed text (like the ebooks twitter accounts).

The markov chain trainer makes a number of improvements over other out-of-the-box markov-model python applications (at least the ones that I've seen):
1. The markov chain can train higher-order models that look for chains of 2, 3, or 4 words (ngrams) in the corpus
2. The model is built using numpy arrays so it's very fast
3. The probability matrix used for the model only contains observed ngrams, so it's feasible to train high-order models on large corpi.

## TO-DO:
1. Improve handling of mis-formatted arguments (e.g., single list instead of list-of-lists for the corpus)
2. Create a separate data structure that stores the *first word* of lines entered in the corpus so that these can be used for new song generation/new line start
3. Parallelize the model-fitting/counting procedure
4. Use [broadcasting](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html?highlight=broadcasting#numpy.doc.broadcasting) for normalizing the numpy array
5. Write song-writing module that includes the following components
   * Ability to specify the ending word of a line (for rhyming)
   * Ability to specify the syllable count of a line
6. Write documentation!
