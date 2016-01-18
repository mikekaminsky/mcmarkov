# mcmarkov

MC Markov is a python application for generating new text based on a corpus of observed text (like the ebooks twitter accounts).

The markov chain trainer makes a number of improvements over other out-of-the-box markov-model python applications (at least the ones that I've seen):

1. The markov chain can train higher-order models that look for chains of 2, 3, or 4 words (ngrams) in the corpus
2. The model is built using numpy arrays so it's very fast
3. The probability matrix used for the model only contains observed ngrams, so it's feasible to train high-order models on large corpi.

## TO-DO:
###Efficiency:
3. Parallelize the model-fitting/counting procedure
4. Use [broadcasting](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html?highlight=broadcasting#numpy.doc.broadcasting) for normalizing the numpy array

###UI:
1. Improve handling of mis-formatted arguments (e.g., single list instead of list-of-lists for the corpus)
6. Write documentation!

###New Features
5. Write song-writing module that includes the following components
- [x] Ability to specify the ending word of a line (for rhyming)
- [x] Ability to end the next line with a word that rhymes with the last word of the previous line
   - [x] Create dictionary of rhymes for last-words that are used as 'seeds'
      * How to handle frequency? Should the list be unique, or should it reflect observed frequency?
   - [x] Write a method for choosing a rhyming word that rhymed with the last line but is not the same word
   - [x] Write a method for building raps using couplets
- [x] Ability to specify the syllable count of a line
- [ ] Option to 'clean' the corpus by removing certain punctuation


## Testing:
From the installed directory, run `python -m unittest discover -s . -p 'test.py'`
