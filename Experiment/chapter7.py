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

if __name__=='__main__':
    model = Chap7()

    ###############################################
    # 曖昧性とトピック関連性を考慮した評価語提案
    ###############################################
    lemma_name = 'beautiful.a.01.beautiful'
    target_lexeme = wn.lemma(lemma_name)

    for t in wn.topics():
        model.suggest_evaluation_word(target_lexeme, t)

    ###############################################
    # 言語横断的な連想語提示
    ###############################################
    target_word = wn.word('面白さ','n','jpn')
    target_lang = 'eng'

    for t in wn.topics():
        model.associative_word(target_word, t, target_lang)

    ###############################################
    # 翻訳語妥当性検証
    ###############################################
    targets = [wn.word('design', 'n', 'eng'), wn.word('conception', 'n', 'fra'), wn.word('設計', 'n', 'jpn')]

    model.validate_translation_word(targets)
