from LearnTHU import loggedSession
import pandas as pd 
import json

# 爬虫部分
try: 
    str_info = open('log.json', 'r').readline(-1)
except:
    sess = loggedSession('','') # 登录网络学堂账号
    res = sess.get('http://learn.tsinghua.edu.cn/f/wlxt/common/courseSearch')
    data = {'aoData': '[]'}
    res = sess.post('http://learn.tsinghua.edu.cn/b/kc/v_wlkc_search/pageList',data=data)
    open('log.json','w').write(res.text)
    str_info = res.text

info_dict = json.loads(str_info) # 生成字典格式的信息
course_info = info_dict['object']['aaData'] # 全部课程的字典列表
course_dict = {'kch': [], 'kxh': [], 'kcm': [], 'jsmc':[], 'jsh':[], 'kkdw':[], 'xss':[]} # 按题目要求初始化空字典

for dict in course_info: # 遍历字典列表中的全部课程，存储需要的信息
    if dict['xnxq'] == '2018-2019-2':
        for key in course_dict.keys():
            course_dict[key].append(dict[key])

df = pd.DataFrame(course_dict) # 将字典转化为 df
columns_dict = {'kch': '课程号', 'kxh': '课序号', 'kcm': '课程名称', 'jsmc':'教师名称', 'jsh': '教师号', 'kkdw': '开课单位', 'xss': '学生数'} # 新列名
df.rename(columns = columns_dict, inplace=True) # 更改列名
df = df.sort_values(by='开课单位' , ascending=True) # 按院系排序
df.set_index(['课程号'], inplace=True) # 将课程号设置为新的索引
df.to_excel('课程信息.xlsx') # 写入 xlsx

# 数据处理部分
sortdf = df.groupby('教师号').sum() # 求每位老师所有课程的学生总人数，为防止重名，以教师号为依据
sortdf = sortdf.sort_values(by = '学生数', ascending=True) # 对学生总人数进行排序
min = sortdf['学生数'][0] # 最少学生数
max = sortdf['学生数'][-1] # 最大学生数
minList = []
maxList = []

for index in sortdf.index: # 遍历所有教师名
    if sortdf.loc[index]['学生数'] == min:
        minList.append(index) # 选出总学生人数最少的教师
    if sortdf.loc[index]['学生数'] == max:
        maxList.append(index) # 选出总学生人数最多的教师

df['课程号'] = df.index.to_series()
df.set_index(['教师号'], inplace=True) # 将教师号设置为新的索引
order = ['教师名称', '课程号', '课序号', '课程名称', '开课单位', '学生数'] # 给 df 的列名排序
df = df[order]
df.loc[minList].to_excel('所有课程总学生人数最少的教师.xlsx') # 写入 xlsx
df.loc[maxList].to_excel('所有课程总学生人数最多的教师.xlsx') # 写入 xlsx