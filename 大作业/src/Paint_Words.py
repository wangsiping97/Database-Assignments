import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import random
import jieba.analyse as getKey
from sklearn.decomposition import PCA
import matplotlib.colors as col
import re

# 设置默认字体
mpl.rcParams['font.sans-serif'] = ['STHeiti']
mpl.rcParams['axes.unicode_minus'] = False
# 设置图片画布大小
mpl.rcParams['figure.figsize'] = [9.216, 4.4856]

class Paint_Words:
    def __init__ (self, fpath, title):
        self.path = fpath
        self.title = title
    
    # 对于每学期的视频名称，获取词向量
    def _getVec(self, dic):
        needSave = False
        try:
            # 从对应原有数据生成的 .iter5 文件中读取数据
            vec_file = open('%s.iter5' % (self.path), 'r')
            line = vec_file.readline().split()
        except:
            needSave = True
            # 从 ChineseWordVector.iter5 中读取数据
            vec_file = open('../data/ChineseWordVector.iter5', 'r')
            line = vec_file.readline().split()
        
        n, d = int(line[0]), int(line[1])
        print(n, d, len(dic))
        self.vec_dic = {}
        for i in range(0, n):
            line_str = vec_file.readline()
            line = line_str.split()
            try:
                key = line[0]
                if key in dic:
                    vec = []
                    for k in range(0, d):
                        vec += [float(line[k + 1])]
                    self.vec_dic[key] = np.array(vec)
            except:
                pass
            if len(self.vec_dic) == len(dic):
                break

        if needSave:
            print('Saving word vectors......')
            out = open('%s.iter5' % (self.path), 'wb')
            out.write((str(len(self.vec_dic)) + ' ' + str(d) + '\n').encode('utf-8'))
            for key in self.vec_dic:
                out.write(key.encode('utf-8'))
                out.write(' '.encode('utf-8'))
                vec = self.vec_dic[key]
                for i in range(0, d):
                    out.write(str(vec[i]).encode('utf-8'))
                    if i < d - 1:
                        out.write(' '.encode('utf-8'))
                    else:
                        out.write('\n'.encode('utf-8'))
            out.close()
    
    # 使用 PCA 方法将 300 的词向量降至 2 维
    def _reduce2D(self):
        pca=PCA(n_components=2)
        keys = [key for key in self.vec_dic]
        x = np.array([self.vec_dic[key] for key in self.vec_dic])
        print(x.shape)
        x2d = pca.fit_transform(x)
        self.vec_dict_2D = {}
        for i, key in enumerate(keys):
            self.vec_dict_2D[key] = x2d[i]
    
    # 获取绘制图片的颜色（动态）
    def _getRGBA(self, v):
        v = np.sqrt(v)
        color_trans = ['#660066', '#660033', '#660000']
        n = len(color_trans)
        i = min(n-1, int(v * float(n)))
        return color_trans[n - 1 -i]
    
    # 整合以上私有函数，绘制图片
    def solve(self, type=0):
        dic = {}
        lines = open(self.path,'r',encoding='utf-8').read().strip().split('\n')[1:]
        print(len(lines))
        for line in lines:
            try:
                s = re.search(',[\d]{12},', line).span()[0]
                line = line[s+1:]
                line = line.split(',')
                vname = line[2]
                vlen = float(line[3])
                sta = float(line[6])
                end = float(line[7])
                value = (end - sta) / vlen
                # 使用 extract_tags 函数截取每个视频名称中的词语
                keys = getKey.extract_tags(vname, topK=5, allowPOS=('n'))
                for key in keys:
                    if key not in dic:
                        dic[key] = 0.
                    dic[key] += value
            except:
                pass

        self._getVec(dic)
        self._reduce2D()

        xs = []
        ys = []
        maxValue = max([dic[key] for key in dic])
        # 画图
        plt.figure(figsize = (9.216, 4.4856))
        for key in self.vec_dict_2D:
            v = dic[key] / maxValue
            c = self._getRGBA(v)
            x = self.vec_dict_2D[key][0]
            y = self.vec_dict_2D[key][1]
            xs += [x]
            ys += [y]
            if type == 1:
                plt.text(x, y, key, color = c, 
                    fontsize=23 * 1.2 * (v ** 0.5), alpha=v ** 0.8)
            if type == 0:
                plt.text(x, y, key, color = c, 
                    fontsize=14 , alpha=0.4)
        plt.xlim(min(xs) - 0.2, max(xs) + 0.7)
        plt.ylim(min(ys) - 0.2, max(ys) + 0.2)
        plt.grid(linestyle=':')
        plt.title(self.title)
        plt.savefig('../pics/word/'+self.title+str(type)+'.svg')
        plt.show()
        plt.close()


if __name__ == '__main__':
    title_list = ['2016春季', '2016秋季', '2017春季', '2017秋季', '2018春季', '2018秋季']
    name_list = ['2016T1', '2016T2', '2017T1', '2017T2', '2018T1', '2018T2']
    for i in range(0, 6):
        a = Paint_Words('../data/'+name_list[i]+'.csv', title_list[i])
        # a.solve(0)
        a.solve(1)