class Card:
    back = '蓝色方格花纹'
    color_dict = {'C': '梅花', 'D': '方块', 'H': '红桃', 'S': '黑桃'}
    point_dict = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'}
    
    def __init__(self, _color, _point):
        self.color = _color
        self.point = _point
    
    def describe(self):
        print("这是一张花色为 {}, 点数为 {}, 牌背为 {} 的扑克牌。".format(Card.color_dict[self.color], Card.point_dict[self.point], self.back))
    
    def change_back(self, another_back):
        self.back = another_back

class Dealer: 
    pass