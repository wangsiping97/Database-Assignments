import pandas as pd 
import numpy as np 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pylab import mpl
import re 

# 设置默认字体
mpl.rcParams['font.sans-serif'] = ['STHeiti']
mpl.rcParams['axes.unicode_minus'] = False

# 创建绘制直方图的类
class Paint_Hist:
    def __init__(self, fpath, title):
        self.path = fpath
        self.title = title

    def draw_hist(self):
        # 打开文件，取出除表头以外的所有内容
        lines = open(self.path,'r',encoding='utf-8').read().strip().split('\n')[1:]
        # 创建学堂号的集合，用于计算用户个数
        ids = set()
        # 创建视频编号的 list
        vnames = []
        for line in lines:
            try: 
                # 使用正则表达式找出所有学堂号的起始位置
                s = re.search(',[\d]{12},', line).span()[0]
                # 将每一行的字符串进行分割，把用户名的部分去掉
                line = line[s+1:]
                # 进一步分割，将每个项目定位出来
                line = line.split(',')
                # 取学堂号
                id = line[0]
                # 取视频编号
                vname = line[1]
                # 纠错
                if (len(vname) < 32):
                    print(line)
                # 将学堂号加入学堂号的集合中
                ids.add(id)
                # 将视频编号加入视频编号的列表中
                vnames.append(vname)
            except:
                pass
        # 计算全部学生人数
        total_num_of_student = len(ids)
        # 创建字典，key 为视频编号，value 为点击次数
        count_dict = {}
        # 将视频编号加入字典，并count value
        for i in vnames:
            if i not in count_dict:
                count_dict[i] = 0 
            count_dict[i] += 1
        # 创建行 index 为视频编号的 dataframe
        video_df = pd.DataFrame(count_dict, index=['点击次数']).T
        # 将 视频编号按照点击次数排序
        video_df = video_df.sort_values(by='点击次数')
        # 将点击次数改为人均点击次数
        value = np.array(list(video_df['点击次数'])) / total_num_of_student
        value = list(value)
        group = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1]
        # 创建一张图片
        plt.figure()
        # 绘制直方图
        plt.hist(value, group, histtype='bar', edgecolor='black', facecolor='#c0504d', alpha=0.75, rwidth=1)
        # 设置图片格式
        plt.yticks([])
        plt.title(self.title)
        plt.savefig('../pics/hist/'+self.title+'直方图.svg')
        plt.show()
        plt.close()

if __name__ == '__main__':
    title_list = ['2016春季', '2016秋季', '2017春季', '2017秋季', '2018春季', '2018秋季']
    name_list = ['2016T1', '2016T2', '2017T1', '2017T2', '2018T1', '2018T2']
    for i in range(0, 6):
        a = Paint_Hist('../data/'+name_list[i]+'.csv', title_list[i])
        a.draw_hist()