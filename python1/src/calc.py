class Calc(object):
    def getGrade(self, str):   # 存入成绩单字符串
        self.initGrade = str
    
    def makeDictlist(self):   # 将成绩单字符串制作成字典列表
        self.list = list()
        templist = self.initGrade.split('\n')   # 先按照换行符分割
        for courseInfo in templist:
            courseList = courseInfo.split(' ')   # 再按照空格分割
            if (len(courseList) < 3):   # 删去尾部不符合格式的空格
                continue
            tempDict = {'课程名':{},'学分':{},'绩点':{}}   # 为每一门课创建字典
            tempDict['课程名'] = courseList[0]
            tempDict['学分'] = courseList[1]
            tempDict['绩点'] = courseList[2]
            self.list.append(tempDict)   # 将字典加入字典列表中
    
    def countCredit(self):   # 计算所修学分
        self.sumCredit = 0
        for course in self.list:
            if (course['绩点'] != "F" and course['绩点'] != "I" and course['绩点'] != "W"):   # 刨去 挂科、未完成与退课的课程
                self.sumCredit += int(course['学分'])
        return self.sumCredit
    
    def getGPA(self):   # 计算平均学分绩
        self.gpaSum = 0
        self.sumGrade = 0
        for course in self.list:
            try:    # 将所有绩点显示为字母（即无法转换为 float 类型）的课程全部刨去
                self.sumGrade += float(course['绩点']) * int(course['学分'])
                self.gpaSum += int(course['学分'])
            except:
                continue
        self.GPA = self.sumGrade / self.gpaSum
        return round(self.GPA, 2)   # 返回保留两位小数的平均学分绩
    
    def showHighScoreList(self):   # 显示高于均绩的课程名称
        self.getGPA()
        highList = list()   # 创建用于存储课程名称的空列表
        for course in self.list:
            try:   # 将所有绩点显示为字母（即无法转换为 float 类型）的课程全部刨去
                if float(course['绩点']) > self.GPA:
                    highList.append(course['课程名'])   # 将筛选后的课程名加入列表中
            except:
                continue
        return highList   # 返回列表