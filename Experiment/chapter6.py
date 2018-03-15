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

if __name__=='__main__':
    words = [wn.word('good' 'a', 'eng'), wn.word('long' 'a', 'eng'), wn.word('hard' 'a', 'eng')]
    topics = wn.topics()
    model = Chap6(words, topics)
    
    model.write_vector_file()
    model.write_relatedness_matrix()
