import random
import math

class Card: # Card 类，题中要求
    back = '蓝色方格花纹'
    color_dict = {'C': '梅花', 'D': '方块', 'H': '红桃', 'S': '黑桃'}
    point_dict = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', \
                  7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    
    def __init__(self, _color, _point):
        self.color = _color
        self.point = _point
    
    def describe(self):
        # print("这是一张花色为 {}, 点数为 {}, 牌背为 {} 的扑克牌。".format(Card.color_dict[self.color], Card.point_dict[self.point], self.back))
        return Card.color_dict[self.color] + Card.point_dict[self.point] # 返回单个牌牌型
    
    def change_back(self, another_back):
        self.back = another_back

class Dealer: 
    def __init__(self):
        self.cardList = []
        for i in range(2, 15):
            self.cardList.append(Card('C', i))
            self.cardList.append(Card('D', i))
            self.cardList.append(Card('H', i))
            self.cardList.append(Card('S', i)) # 生成一副牌的list，每张牌对应0-51的一个位置

        self.permutation = []
        for i in range(52):
            self.permutation.append(i) # 生成一个0-51的顺序排列

        self.hepai = []
        self.player1 = []
        self.player2 = []
        self.score1 = 0
        self.score2 = 0

    def shuffle(self):
        random.shuffle(self.permutation) # 生成0-51的随机排列
    
    def deal(self):
        for i in range(5):
            self.hepai.append(self.cardList[self.permutation[i]]) # 排列的前五张为河牌
        for i in range(5, 7):
            self.player1.append(self.cardList[self.permutation[i]]) # 后两张为玩家1的底牌
        for i in range(7, 9):
            self.player2.append(self.cardList[self.permutation[i]]) # 再后两张为玩家2的底牌
        for card in self.hepai:
            self.player1.append(card) # 生成玩家1的七张牌
            self.player2.append(card) # 生成玩家2的七张牌
        
        print("玩家1的手牌为",self.player1[0].describe(), "和", self.player1[1].describe())
        print("玩家2的手牌为",self.player2[0].describe(), "和", self.player2[1].describe())
        print("河牌为[", self.hepai[0].describe(), self.hepai[1].describe(), self.hepai[2].describe(), self.hepai[3].describe(), self.hepai[4].describe(), "]")
    
    def scoring(self, _list): # 传五张牌，采用16进制计分方法，分不同类型讨论
        pList = [card.point for card in _list]
        cList = [card.color for card in _list]
        pList.sort()
        cList.sort()
        if pList == [2, 3, 4, 5, 14]: # A2345 的情况
            pList = [1, 2, 3, 4, 5] # A2345 最小
        hexPoint = pList[4] * pow(16, 4) + pList[3] * pow(16, 3) + pList[2] * pow(16, 2) + pList[1] * pow(16, 1) + pList[0] * pow(16, 0)
        if (pList[4] - pList[3] == 1) and (pList[3] - pList[2] == 1) and (pList[2] - pList[1] == 1) and (pList[1] - pList[0] == 1): # 顺子
            if cList[-1] == cList[0]: # 同花顺
                return 9 * pow(16, 5) + hexPoint, '同花顺[' + Card.point_dict[pList[4]] + ']'
            else: # 顺子
                return 5 * pow(16, 5) + hexPoint, '顺子[' + Card.point_dict[pList[4]] + ']'
        elif pList[-1] == pList[1]: # 四条1
            return 8 * pow(16, 5) + hexPoint, '四条[' + Card.point_dict[pList[1]] + '带' + Card.point_dict[pList[0]] + ']'
        elif pList[-2] == pList[0]: # 四条2
            return 8 * pow(16, 5) + hexPoint, '四条[' + Card.point_dict[pList[0]] + '带' + Card.point_dict[pList[4]] + ']'
        elif pList[0] == pList[2] and pList[3] == pList[4]: # 葫芦1
            return 7 * pow(16, 5) + hexPoint, '葫芦[' + Card.point_dict[pList[0]] + '带' + Card.point_dict[pList[4]] + ']'
        elif pList[2] == pList[4] and pList[0] == pList[1]: # 葫芦2
            return 7 * pow(16, 5) + hexPoint, '葫芦[' + Card.point_dict[pList[2]] + '带' + Card.point_dict[pList[0]] + ']'
        elif cList[0] == cList[4]: # 同花
            return 6 * pow(16, 5) + hexPoint, '同花[' + Card.color_dict[cList[0]] + ']'
        elif (pList[0] == pList[2]): # 三条1
            return 4 * pow(16, 5) + hexPoint, '三条[' + Card.point_dict[pList[0]] + ']'
        elif (pList[2] == pList[4]): # 三条2
            return 4 * pow(16, 5) + hexPoint, '三条[' + Card.point_dict[pList[2]] + ']'
        elif (pList[0] == pList[1] and pList[2] == pList[3]): # 两对1
            return 3 * pow(16, 5) + hexPoint, '两对[' + Card.point_dict[pList[0]] + '和' + Card.point_dict[pList[2]] + ']'
        elif (pList[0] == pList[1] and pList[3] == pList[4]): # 两对2
            return 3 * pow(16, 5) + hexPoint, '两对[' + Card.point_dict[pList[0]] + '和' + Card.point_dict[pList[3]] + ']'
        elif (pList[1] == pList[2] and pList[3] == pList[4]): # 两对3
            return 3 * pow(16, 5) + hexPoint, '两对[' + Card.point_dict[pList[1]] + '和' + Card.point_dict[pList[3]] + ']'
        elif (pList[0] == pList[1]) or (pList[1] == pList[2]): # 一对
            return 2 * pow(16, 5) + hexPoint, '一对[' + Card.point_dict[pList[1]] + ']'
        elif (pList[2] == pList[3]) or (pList[3] == pList[4]): # 一对
            return 2 * pow(16, 5) + hexPoint, '一对[' + Card.point_dict[pList[3]] + ']'
        else:
            return 1 * pow(16, 5) + hexPoint, '高牌[' + Card.point_dict[pList[4]] + ']'

    def judge(self):
        maxScore1 = 0
        paixing1 = ''
        maxScore2 = 0
        paixing2 = ''
        
        for i in range(7):
            for j in range(i + 1, 7):
                temp = self.player1.copy()
                temp.remove(self.player1[i])
                temp.remove(self.player1[j]) # 删去玩家1全部牌中的两张不同的牌
                score, paixing = self.scoring(temp) # 计分
                if score > maxScore1: # 存下最大的
                    maxScore1 = score
                    paixing1 = paixing
        for i in range(7):
            for j in range(i + 1, 7):
                temp = self.player2.copy()
                temp.remove(self.player2[i])
                temp.remove(self.player2[j]) # 删去玩家2全部牌中的两张不同的牌
                score, paixing = self.scoring(temp) # 计分
                if score > maxScore2: # 存下最大的
                    maxScore2 = score
                    paixing2 = paixing

        print('玩家1的最终牌型：', paixing1)
        print('玩家2的最终牌型：', paixing2)

        if maxScore1 > maxScore2: # 判断获胜方
            print('玩家1胜出')
        elif maxScore2 > maxScore1:
            print('玩家2胜出')
        else: 
            print('平局')
    
    def new_game(self):
        self.shuffle()
        self.deal()
        self.judge()

if __name__ == '__main__': 
    d = Dealer()
    d.new_game()
