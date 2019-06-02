from LearnTHU import loggedSession
import pandas as pd 
import json

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
columns_dict = {'kch': '课程号', 'kxh': '课序号', 'kcm': '课程名', 'jsmc':'教师名称', 'jsh': '教师号', 'kkdw': '开课单位', 'xss': '学生数'} # 新列名

df.rename(columns = columns_dict, inplace=True) # 更改列名
df = df.sort_values(by='开课单位' , ascending=True) # 按院系排序

df.set_index(['课程号'], inplace=True) # 将课程号设置为新的索引

open('课程信息.xlsx','w')
df.to_excel('课程信息.xlsx') # 写入 xlsx

sortdf = df.groupby('教师名称').sum() # 求每位老师所有课程的学生总人数
sortdf = sortdf.sort_values(by = '学生数', ascending=True) # 对学生总人数进行排序

print('所有课程总学生人数最多的教师是:', sortdf.index[-1]) # 汤彬
print('所有课程总学生人数最少的教师是:', sortdf.index[0]) # 许斌