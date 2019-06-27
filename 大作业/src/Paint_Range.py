import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import re

# 设置默认字体
mpl.rcParams['font.sans-serif'] = ['STHeiti']
mpl.rcParams['axes.unicode_minus'] = False

# 创建绘制慕课曲线的类
class Paint_Range:
	def __init__(self, fpath, title):
		self.path = fpath
		self.title = title

	# 获取每个视频每千分点时刻的点击次数
	def getRange(self, lst):
		vlen = lst[0][0]
		x = []
		y = []
		for i in range(1, 1000):
			# 取视频的第 i 个千分点
			t = float(i) / 1000. * vlen
			cnt = 0.
			for _, sta, end in lst:
				if sta <= t and t <= end:
					cnt += 1.
			x += [i]
			y += [cnt]
		return np.array(x), np.array(y)

	# 绘制图片
	def plot(self, xs, ys, name):
		plt.plot(xs,ys, color='#4bacc6', linestyle='-', linewidth=2.)
		plt.title(self.title + ' ' + name)
		plt.grid(linestyle=':')
		# plt.savefig('../pics/range/'+self.title+'.svg')
		plt.show()

	# 整合以上功能的函数
	def solve(self, type=0):
		dic = {}
		# 打开文件，取出除表头以外的所有内容
		lines = open(self.path,'r',encoding='utf-8').read().strip().split('\n')[1:]
		for line in lines:
			try:
				# 使用正则表达式找出所有学堂号的起始位置
				s = re.search(',[\d]{12},', line).span()[0]
				# 将每一行的字符串进行分割，把用户名的部分去掉
				line = line[s+1:]
				# 进一步分割，将每个项目定位出来
				line = line.split(',')
				# 取视频名称
				vname = line[2]
				# 取视频时长
				vlen = float(line[3])
				# 取开始时间
				sta = float(line[6])
				# 取结束时间
				end = float(line[7])
				# 创建字典 dic
				if vname not in dic:
					dic[vname] = []
				dic[vname] += [(vlen, sta, end)]
			except:
				pass

		yys = []
		if type == 1:
			for key in dic:
				# 将点击量超过 1000 次的视频的“慕课曲线”绘制出
				if len(dic[key]) > 1000:
					print(key)
					xs, ys = self.getRange(dic[key])
					yys.append(ys)
					self.plot(xs, ys, key)

		if type == 0:
			# 将该学期视频的平均观看情况的“慕课曲线”绘制出
			for key in dic:
				if len(dic[key]) > 1:
					xs, ys = self.getRange(dic[key])
					yys.append(ys)
			yys = np.array(yys)
			yys = yys.mean(axis=0)
			self.plot(xs, yys, 'Average')

if __name__ == '__main__':
	title_list = ['2016春季', '2016秋季', '2017春季', '2017秋季', '2018春季', '2018秋季']
	name_list = ['2016T1', '2016T2', '2017T1', '2017T2', '2018T1', '2018T2']
	for i in range(0, 6):
		a = Paint_Range('../data/'+name_list[i]+'.csv', title_list[i])
		a.solve(1)