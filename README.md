# mcmarkov

MC Markov is a python application for generating new text based on a corpus of observed text (like the ebooks twitter accounts).

The markov chain trainer makes a number of improvements over other out-of-the-box markov-model python applications (at least that I've seen):
1. The markov chain can train higher-order models that look for chains of 2, 3, or 4 words (ngrams) in the corpus
2. The model is trained using numpy, arrays so it's very fast
3. The probability matrix used for the model only contains observed ngrams, so it's feasible to train high-order models on large corpi.

## TO-DO:
1. Improve handling of mis-formatted arguments (e.g., single list instead of list-of-lists for the corpus)
2.
