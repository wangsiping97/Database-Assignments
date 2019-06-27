import pandas as pd 
import numpy as np 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def count_correct_ratio(fpath):
    # 打开文件
    f = open(fpath, 'r', encoding='utf-8')
    # 用 pandas 中的方法阅读文件，并生成 dataframe
    df = pd.read_csv(f)
    # 提取列
    prob_df = df[['习题题干', '是否正确']]
    res_list = []
    total_list = []
    # 将 "是否正确" 替换为 0/1，并添加进提取后的 df 中，并计算总答题次数
    for i in prob_df['是否正确']:
        if i == '正确':
            res_list.append(1)
            total_list.append(1)
        else:
            res_list.append(0)
            total_list.append(1)
    prob_df['res'] = pd.Series(res_list, index=prob_df.index)
    prob_df['total'] = pd.Series(total_list, index=prob_df.index)
    # 计算正确回答次数
    prob_df = prob_df.drop(['是否正确'], axis=1).groupby('习题题干').sum()
    # 计算正确率
    prob_df['正确率'] = prob_df['res'] / prob_df['total']
    prob_df = prob_df.sort_values(by='正确率').drop(['res', 'total'], axis=1)
    return prob_df