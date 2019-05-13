from src.calc import *
from src.GUI import *


class Shell(object):
    def __init__(self):   # 构造函数，首先打印出帮助内容
        print("\n输入以下命令执行不同操作：")
        print("? 帮助")
        print("0 退出")
        print("1 录入成绩单")
        print("2 更改成绩单")
        print("3 查询GPA")
        print("4 查询总学分")
        print("5 查询绩点高于GPA的科目\n")

    def parseCommand(self, cmd):   # 用于解析命令的函数
        if (cmd == "0"):   # 退出
            return False
        if (cmd == ""):   # 换行符
            return True
        elif (cmd == "1"):   # 录入成绩单
            self.calc = Calc()   # 创建 Calc 的实例，用于进行后续计算
            root = Tk()
            GUI(root, self.calc, "init")   # 创建一个 init 类的成绩单录入窗口，具体见 GUI.py
            root.mainloop()
            self.calc.makeDictlist()   # 调用 Calc 解析字符串成绩单的函数
            print("\n成绩单已成功保存！请稍等片刻...\n")
        elif (cmd == "2"):   # 更改成绩单内容
            try:   # 若尚未录入成绩单，则报错
                root = Tk()
                GUI(root,self.calc, "edit")   # 创建一个 edit 类的成绩单录入窗口，具体见 GUI.py
                root.mainloop()
                self.calc.makeDictlist()
                print("\n成绩单已成功保存！请稍等片刻...\n")
            except:
                root.destroy()
                print("\n尚未录入成绩或成绩单格式不正确。\n")
        elif (cmd == "3"):   # 查询 GPA
            try:    # 若尚未录入成绩单，则报错
                gpa = self.calc.getGPA()   # 调用 Calc 的 getGPA 函数，具体见 calc.py
                print("\n您的学分绩为：", gpa, "\n")
            except: 
                print("\n尚未录入成绩或成绩单格式不正确。\n")
        elif (cmd == "4"):
            try:    # 若尚未录入成绩单，则报错
                credit = self.calc.countCredit()   # 调用 Calc 的 countCredit 函数，具体见 calc.py
                print("\n您修过的总学分为：", credit, "\n")
            except: 
                print("\n尚未录入成绩或成绩单格式不正确。\n")
        elif (cmd == "5"):
            try:    # 若尚未录入成绩单，则报错
                courseList = self.calc.showHighScoreList()   # 调用 Calc 的 showHighScoreList 函数，具体见 calc.py
                print("\n高于平均学分绩的课程有：\n")
                for course in courseList:   # 分别打印每门课程的名称
                    print(course)
                print("\n")
            except: 
                print("\n尚未录入成绩或成绩单格式不正确。\n")
        elif (cmd == "?"):   # 显示帮助
            print("\n输入以下命令执行不同操作：")
            print("? 帮助")
            print("0 退出")
            print("1 录入成绩单")
            print("2 更改成绩单")
            print("3 查询GPA")
            print("4 查询总学分")
            print("5 查询绩点高于GPA的科目\n")
        else:
            print("\n命令错误。\n")
        return True

    def run(self):
        cmd = ""
        while (self.parseCommand(cmd)):   # 若 parseCommand 函数返回值为 True，则可以一直输入下去，直到输入 0 退出为止
            cmd = input("您的选择（数字）：")
            