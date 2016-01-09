#Based on code by Danielle Sucher
#https://github.com/DanielleSucher/Nantucket/blob/master/poetry.py
#Updated by Michael Kaminsky

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import re
import nltk
nltk.data.path = [path.dirname( path.dirname( path.abspath(__file__) ) )]
from curses.ascii import isdigit
from nltk.corpus import cmudict
cmu_dictionary = cmudict.dict()

def approx_nsyl(word):
    digraphs = {"ai", "au", "ay", "ea", "ee", "ei", "ey", "oa", "oe", "oi", "oo", "ou", "oy", "ua", "ue", "ui"}
    # Ambiguous, currently split: ie, io
    # Ambiguous, currently kept together: ui
    count = 0
    array = re.split("[^aeiouy]+", word.lower())
    for i, v in enumerate(array):
        if len(v) > 1 and v not in digraphs:
            count += 1
        if v == '':
            del array[i]
    count += len(array)
    if re.search("(?<=\w)(ion|ious|(?<!t)ed|es|[^lr]e)(?![a-z']+)", word.lower()):
        count -= 1
    if re.search("'ve|n't", word.lower()):
        count += 1
    return count

def nsyl(word):
    # return the min syllable count in the case of multiple pronunciations
    if not word.lower() in cmu_dictionary:
        return approx_nsyl(word)
    return min([len([y for y in x if isdigit(str(y[-1]))]) for x in cmu_dictionary[word.lower()]])

def rhymesyls(word):
    if word.lower() in cmu_dictionary:
        pronunciations = cmu_dictionary[word.lower()]
        rhyming_syllables_list = []
        for pronunciation in pronunciations:
            rhyming_syllables_list.append(rhymesyls_for_pronunciation(pronunciation))
        return list(set(rhyming_syllables_list))
    else:
        return "NORHYME"

def rhymes_with(word1, word2):
    # return true if any of the pronunciations for word1 rhyme with word2
    word1_rhymesyls = rhymesyls(word1)
    word2_rhymesyls = rhymesyls(word2)
    return bool(set(word1_rhymesyls) & set(word2_rhymesyls))

def rhymesyls_for_pronunciation(pronunciation):
    outlist = str()
    i = -1
    while i >= 0 - len(pronunciation):
        if isdigit(str(pronunciation[i][-1])):
            outlist = pronunciation[i][:-1]
            if i != -1:
                outlist = outlist + ' ' + pronunciation[i + 1:][0]
            return outlist
        i -= 1
    return outlist

