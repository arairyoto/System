import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.font_manager import FontProperties

# fp = FontProperties(fname='/Users/ユーザー名/Library/Fonts/ipag.ttf');

plt.rcParams['font.family'] ='IPAPGothic'#使用するフォント
plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
plt.rcParams['font.size'] = 10 #フォントの大きさ
plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ

WIDTH = 7
HEIGHT = 5

class Analysis:
    def __init__(self, file_name):
        # Loading
        with open(file_name, 'r') as f:
            self.lvs = [line.strip() for line in f.readlines()]
        # get lexemes and vectors
        self.lexemes = []
        self.features = np.empty((0,300), int)
        for lv in self.lvs:
            lexeme = lv.split(' ')[0]
            vector = np.array([float(x) for x in lv.split(' ')[1:]])
            self.lexemes.append(lexeme)
            self.features = np.append(self.features, np.array([vector]), axis=0)

        self.words = list(set([l.split(':')[0] for l in self.lexemes]))
        self.categories = list(set([l.split(':')[1] for l in self.lexemes]))

    def plot_all(self, x, y):
        plt.figure(figsize=(WIDTH,HEIGHT))
        pca = PCA(n_components=2)
        pca.fit(self.features)

        l_in_c = {}
        f_in_c = {}
        # initialize
        for c in self.categories:
            l_in_c[c] = []
            f_in_c[c] = np.empty((0,2), int)

        # 分析結果を元にデータセットを主成分に変換する
        transformed = pca.fit_transform(self.features)

        for i, l in enumerate(self.lexemes):
            c = l.split(':')[1]
            l_in_c[c].append(l)
            f_in_c[c] = np.append(f_in_c[c], np.array([transformed[i]]), axis=0)

        for c in self.categories:
            plt.scatter(f_in_c[c][:, 0], f_in_c[c][:, 1], label=c)
            for i, l in enumerate(l_in_c[c]):
                plt.annotate(l, xy=(f_in_c[c][i, 0],f_in_c[c][i, 1]), size=8)

        plt.title('principal component')
        plt.xlabel('principal component 1')
        plt.ylabel('principal component 2')
        plt.legend(loc='upper right')
        plt.grid(color='gray')
        plt.xlim([-x,x])
        plt.ylim([-y,y])
        plt.locator_params(axis='y',nbins=6) #y軸，6個以内．
        plt.tight_layout() #グラフが重ならず，設定した図のサイズ内に収まる．
        plt.savefig('all_'+str(x)+'_'+str(y)+'.pdf', transparent=True)

        # 主成分の次元ごとの寄与率を出力する
        print('各次元の寄与率: {0}'.format(pca.explained_variance_ratio_))
        print('累積寄与率: {0}'.format(sum(pca.explained_variance_ratio_)))

        plt.show()

    def plot_word(self, w, x, y):
        plt.figure(figsize=(WIDTH,HEIGHT))
        lexemesT = []
        featuresT = np.empty((0,300), int)

        for i, l in enumerate(self.lexemes):
            if l.split(':')[0] == w:
                lexemesT.append(l)
                featuresT = np.append(featuresT, np.array([self.features[i]]), axis=0)

        pca = PCA(n_components=2)
        pca.fit(featuresT)
        # 分析結果を元にデータセットを主成分に変換する
        transformed = pca.fit_transform(featuresT)

        plt.scatter(transformed[:, 0], transformed[:, 1])
        for i, l in enumerate(lexemesT):
            plt.annotate(l, xy=(transformed[i, 0],transformed[i, 1]), size=8)

        plt.title('principal component')
        plt.xlabel('principal component 1')
        plt.ylabel('principal component 2')
        plt.legend(loc='upper right')
        plt.grid(color='gray')
        plt.xlim([-x,x])
        plt.ylim([-y,y])
        plt.locator_params(axis='y',nbins=6) #y軸，6個以内．
        plt.tight_layout() #グラフが重ならず，設定した図のサイズ内に収まる．
        plt.savefig(w+'_'+str(x)+'_'+str(y)+'.pdf', transparent=True)

        # 主成分の次元ごとの寄与率を出力する
        print('各次元の寄与率: {0}'.format(pca.explained_variance_ratio_))
        print('累積寄与率: {0}'.format(sum(pca.explained_variance_ratio_)))

        #plt.show()

    def plot_word_(self, w, x, y):
        plt.figure(figsize=(WIDTH,HEIGHT))
        pca = PCA(n_components=2)
        pca.fit(self.features)
        # 分析結果を元にデータセットを主成分に変換する
        transformed = pca.fit_transform(self.features)
        # transformed = self.features

        for i, l in enumerate(self.lexemes):
            if l.split(':')[0] == w:
                plt.scatter(transformed[i, 0], transformed[i, 1])
                plt.annotate(l.split(':')[1], xy=(transformed[i, 0],transformed[i, 1]), size=14)

        plt.title('principal component')
        plt.xlabel('principal component 1')
        plt.ylabel('principal component 2')
        plt.legend(loc='upper right')
        plt.grid(color='gray')
        plt.xlim([-x,x])
        plt.ylim([-y,y])
        plt.locator_params(axis='y',nbins=6) #y軸，6個以内．
        plt.tight_layout() #グラフが重ならず，設定した図のサイズ内に収まる．
        plt.savefig(w+'_'+str(x)+'_'+str(y)+'norm.pdf', transparent=True)

        # 主成分の次元ごとの寄与率を出力する
        print('各次元の寄与率: {0}'.format(pca.explained_variance_ratio_))
        print('累積寄与率: {0}'.format(sum(pca.explained_variance_ratio_)))

    def plot_categ(self, c, x, y):
        plt.figure(figsize=(WIDTH,HEIGHT))
        lexemesT = []
        featuresT = np.empty((0,300), int)

        for i, l in enumerate(self.lexemes):
            if l.split(':')[1] == c:
                lexemesT.append(l)
                featuresT = np.append(featuresT, np.array([self.features[i]]), axis=0)

        pca = PCA(n_components=2)
        pca.fit(featuresT)
        # 分析結果を元にデータセットを主成分に変換する
        transformed = pca.fit_transform(featuresT)

        plt.scatter(transformed[:, 0], transformed[:, 1])
        for i, l in enumerate(lexemesT):
            plt.annotate(l, xy=(transformed[i, 0],transformed[i, 1]), size=14)

        plt.title('principal component')
        plt.xlabel('principal component 1')
        plt.ylabel('principal component 2')
        plt.legend(loc='upper right')
        plt.grid(color='gray')
        plt.xlim([-x,x])
        plt.ylim([-y,y])
        plt.locator_params(axis='y',nbins=6) #y軸，6個以内．
        plt.tight_layout() #グラフが重ならず，設定した図のサイズ内に収まる．
        plt.savefig(c+'_'+str(x)+'_'+str(y)+'.pdf', transparent=True)

        # 主成分の次元ごとの寄与率を出力する
        print('各次元の寄与率: {0}'.format(pca.explained_variance_ratio_))
        print('累積寄与率: {0}'.format(sum(pca.explained_variance_ratio_)))

        #plt.show()

if __name__ == '__main__':
    file_name = 'pca/multicontextual_space_.txt'
    a = Analysis(file_name)
    a.plot_all(0.00075,0.00025)
    # for w in a.words:
    #     a.plot_word_(w, 0.005, 0.005)

    # for c in a.categories:
    #     a.plot_categ(c, 0.005, 0.005)
    # a.plot_categ('jpn', 2, 2)
    # a.plot_categ('jpn', 0.2, 0.2)
