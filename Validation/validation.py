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

class Model:
    def __init__(self, folder, langs):
        self._folder = folder
        self._files = [os.path.basename(r) for r in glob.glob('%s/*.csv' % self._folder)]
        self._langs = langs
        self._methods = ['simWord', 'simMaxS', 'simAveS', 'simMaxL', 'simAveL']
        try:
            os.mkdir('%s/experiment' % self._folder)
        except:
            print('Already exists experimental folder\n')

    def test(self, test_file, output_file, langs, progress_per=100):
        df = pd.read_csv(test_file, encoding='utf-8')
        N = len(df['word1'])

        lang1 = langs[0]
        lang2 = langs[1]

        res = {}
        for m in self._methods:
            res[m] = []

        for i in range(N):
            if i % progress_per == 0:
                logger.info('SIMILARITY TEST : %i/%i DONE', i ,N )

            word1 = df['word1'][i].strip()
            word2 = df['word2'][i].strip()

            SimList = self.test_segment(word1, word2, lang1, lang2)

            for i in range(self._methods):
                res[self._methods[i]].append(SimList[i])

        for m in self._methods:
            df[m] = res[m]

        df.to_csv(output_file, encoding="utf-8")
        logger.info('TEST DONE')

    def test_segment(self, word1, word2, lang1, lang2):
        S1s = []
        L1s = []
        S2s = []
        L2s = []

        try:
            w1 = wn.words(word1, lang=lang1)[0].vector()
            w2 = wn.words(word2, lang=lang2)[0].vector()
        except:
            w1 = 0
            w2 = 0

        S1s, L1s = self.build_synset_and_lexeme_vector_array(word1, lang1)
        S2s, L2s = self.build_synset_and_lexeme_vector_array(word2, lang2)

        return [self.relatedness(w1,w2), self.simMax(S1s, S2s), self.simAve(S1s, S2s), self.simMax(L1s, L2s), self.simAve(L1s, L2s)]

    def build_synset_and_lexeme_vector_array(self, word, lang):
        Synsets = []
        Lexemes = []

        for s in wn.synsets(word, lang=lang):
            try:
                synset_vector = wn.vector(s)
                Synsets.append(synset_vector)
            except:
                continue

            try:
                for _l in s.lemmas():
                    if _l.name() == word:
                        l = _l

                lexeme_vector = wn.vector(l)
                Lexemes.append(lexeme_vector)
            except:
                continue

        return Synsets, Lexemes


    def relatedness(self, o1, o2):
        try:
            return sum(o1*o2)/np.sqrt(sum(o1*o1)*sum(o2*o2))
        except:
            return -1

    def simMax(self, O1s, O2s):
        result = []
        for o1 in O1s:
            for o2 in O2s:
                result.append(self.relatedness(o1,o2))
        if len(result)==0:
            return -1
        else:
            return max(result)

    def simAve(self, O1s, O2s):
        result = []
        for o1 in O1s:
            for o2 in O2s:
                result.append(self.relatedness(o1,o2))
        try:
            result.remove(-1)
        except:
            result = result

        if len(result)==0:
            return -1
        else:
            return sum(result)/len(result)

    def test_main(self):
        self._outputs = []

        for fl in self._files:
            input_file = '%s/%s' % (self._folder, fl)
            output_file = '%s/experiment/%s' % (self._folder, fl)

            self.test(input_file, output_file, self._langs)

            self._outputs.append(output_file)

    def evaluation_segment(self, output_file):
        df = pd.read_csv(output_file ,encoding="utf-8")
        results = {}
        valid_indices = {}
        coverage = {}
        correlation = {}

        human_result = np.array(df['human'])
        for m in self.methods:
            valid_indices[m] = []
            results[m] = np.array(df[m])
            for i,r in enumerate(results[m]):
                if -1<r and r<1:
                    valid_indices[m].append(i)
                else:
                    continue
            coverage[m] = len(valid_indices[m])/len(results[m])
            correlation[m] = spearmanr(results[m][valid_indices[m]], human_result[valid_indices[m]])[0]

        return coverage, correlation

    def evaluation(self):
        f_cov = open('%s/experiment/coverage.txt' % self._folder, 'w')
        f_cor = open('%s/experiment/correlation.txt' % self._folder, 'w')
        # header
        for m in self.methods:
            f_cov.write(',%s' % m)
            f_cor.write(',%s' % m)
        f_cov.write('\n')
        f_cor.write('\n')

        for output_file in self._outputs:
            cov, cor = self.evaluation_segment(output_file)
            f_cov.write(output_file)
            f_cor.write(output_file)
            for m in self.methods:
                f_cov.write(',%f' % cov[m])
                f_cor.write(',%f' % cor[m])
            f_cov.write('\n')
            f_cor.write('\n')

    def main(self):
        self.test_main()
        self.evaluation()

if __name__=='__main__':
    folder = sys.argv[1]
    lang1 = sys.argv[2]
    lang2 = sys.argv[3]
    langs = [lang1, lang2]

    model = Model(folder, langs)
    model.main()
