from tkinter import *
from src.calc import *

class GUI():
    def __init__(self, master, calc_, type="init"):
        self.root = master
        self.root.config()
        self.root.title('GPA Calculator')   # 确定窗口的标题
        self.root.geometry('400x300')   # 确定窗口大小
        self.calc = calc_    # 将 shell 中的 Calc 实例传进来

        self.master = master
        self.master.config(bg='White')   # 放置并设置背景颜色

        self.canvas = Canvas(self.master, width=400, height=270, scrollregion=(0, 0, 400, 363))   # 在 master 上创建一个 canvas 为了后续做滚动条
        self.canvas.place(x=0, y=0)   # 设置 canvas 的位置

        self.frame = Frame(self.canvas)   # 做一个 frame ，为后续做文本框
        self.frame.place(width=400, height=10000)   # 设置 frame 大小，高度设大一些为了能够传送足够长的成绩单

        self.repeatvbar = Scrollbar(self.canvas, orient=VERTICAL)  # 做一个竖直滚动条
        self.repeatvbar.place(x=380, width=20, height=270)   # 确定数值滚动条的形状大小
        self.repeatvbar.configure(command=self.canvas.yview)   # 将数值滚动条放置在 canvas 上
        self.canvas.config(yscrollcommand=self.repeatvbar.set)

        self.canvas.create_window((278, 180), window=self.frame)   # 形成 输入框 + 竖直滚动条的组合

        self.gradeList = Text(self.frame, bg='White')   # 创建文本框
        self.gradeList.tag_config('greencolor', foreground='#008C00')  # 创建 tag
        """
        分两种情况考虑：
        1）用户尚未录入过成绩单，则弹出窗口并告诉用户“在这里粘贴成绩单”；
        2）用户已录入过成绩单但是想更改部分内容，则弹出窗口并显示原先录入过的成绩单。
        """
        self.gradeList.grid()
        if (type == "init"):
            strMsg = "请在这里粘贴成绩单"
            self.gradeList.insert(END, strMsg, 'greencolor')
        else: 
            self.gradeList.insert(END, self.calc.initGrade)
        
        self.frmLB = Frame(self.master, width=400, height=30)   # 制作两一个 frame，用来放置确认按钮
        self.frmLB.place(x=0, y=270, width=400)
        self.frmLB.grid_propagate(0)

        self.btn = Button(self.frmLB, text = '保存', width=8, command=self.save)   # 制作一个按钮，显示为“保存”，用户按下后调用 save 函数
        self.btn.grid()
    
    def save(self):
        strGrade = str(self.gradeList.get(0.0, END))   # 保存用户录入的文本成绩单
        self.calc.getGrade(strGrade)   # 调用 Calc 实例的 getGrade 函数，将文本成绩单传给 calc
        self.master.destroy()   # 关闭窗口
