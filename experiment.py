# Python Version of WordNetExtractor.java
import os
import sys

sys.path.append('..')

from collections import defaultdict
import numpy as np
import glob
import pandas as pd
from scipy.stats import spearmanr
#exWordNet
from util.exWordNet import exWordNet
from config import *

# Define exWordNet corpus path
wn = exWordNet(CorpusFolder)

class Chap6:
    def __init__(self, words, topics):
        self._words = words # list of Word Object
        self._topics = topics # list of topics

    def write_vector_file(self, filename='vector.txt'):
        f = open(filename, 'w')
        for t in self._topics:
            for w in self._words:
                vector = w.vector(topic=t)
                vector_line = ' '.join(list(map(str,vector)))
                f.write('%s:%s %s\n' % (w.name(), t, vector_line))
        f.close()

    def write_relatedness_matrix(self, filename='relatedness_matrix.txt'):
        f = open(filename, 'w')

        # HEADER
        for t in self._topics:
            for w in self._words:
                f.write(',%s:%s' % (w.name(), t))
        f.write('\n')

        for t1 in self._topics:
            for w1 in self._words:
                v1 = w1.vector(topic=t1)
                f.write('%s:%s' % (w1.name(), t1))
                for t2 in self._topics:
                    for w2 in self._words:
                        v2 = w2.vector(topic=t2)
                        rel = wn._relatedness(v1,v2)
                        f.write(',%f' % rel)
                f.write('\n')
        f.close()

class Chap7:
    # ALPHA = 0.2

    def suggest_evaluation_word(self, target_lexeme, topic):
        key = target_lexeme._key
        f = open('%s.%s.txt' % (key, topic), 'w')

        for w in wn.all_words():
            rel = wn.relatedness(target_lexeme, w)
            amb = w.ambiguity(topic=topic)
            trel = w.topic_relatedness(topic=topic)
            f.write('%s,%f,%f,%f\n' % (w.name(), rel, amb, trel))

        f.close()

    def associative_word(self, target_word, topic, target_lang):
        f = open('%s.%s.%s.txt' % (target_word.name(), topic, target_lang), 'w')

        for w in wn.all_words(pos=None, lang=target_lang):
            try:
                rel, sp = target_word.association(w, topic=topic)
                f.write('%s,%f,%d' % (w.name(), rel, sp))
            except:
                continue

        f.close()

    def validate_translation_word(self, targets, filename='dependency_matrix.txt'):
        f = open(filename, 'w')

        # HEADER
        for t in targets:
            f.write(',%s' % t._key)
        f.write('\n')

        for t1 in targets:
            f.write(t1._key)
            for t2 in targets:
                rel = wn.relatedness(t1,t2)
                f.write(',%f' % rel)
            f.write('\n')
        f.close()
