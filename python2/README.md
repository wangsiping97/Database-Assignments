<center>
  经56 王思萍 2015012527
</center>

# 德州扑克模拟器

能够模拟德州扑克（两位玩家）的小程序。

本文将从以下几个方面介绍这个程序的设计思路和整体结构：

- 使用方法
- 主要功能
- 整体架构与模块介绍
- 不足和改进

## 使用方法

### 需求

- python 3.X

- random

- math

- terminal（OS X 或 Linux）/ cmd （windows）

### 运行

在 `终端` （OS X 或 Linux）或 `命令行` （windows）下，进入文件所在目录，然后输入：

```bash
python Poker.py
```

即可运行程序。

## 主要功能

1. 随机洗混52张牌

2. 向两位玩家发出底牌，并发出五张河牌

3. 以德州扑克规则判断赢家

4. 输出初始牌型、最终牌型与游戏结果

## 整体架构与模块介绍

本程序主要分为两个模块，分别是 `Card` 类和 `Dealer` 类，它们是 **依次包含关系** 。

- `Card` 模块是扑克牌类，主要用于确定每张牌的点数和花色。
- `Dealer` 模块是整个模拟器功能的实现。其功能包括：
  - **洗牌方法shuffle，随机洗混的52张牌。**实现方法为：使用 `random` 模块中的 `shuffle` 函数形成一个0-51的随机排列，由于每一个数字对应唯一的一张牌在`cardList` 中的位置，因此直接可以达到洗牌的结果。
  - **发牌方法deal，随机发出一定数量的牌。**实现方法为：取前面生成的随机排列中的前9个数。其中前5个数所对应的牌为河牌，第6、7个数所对应的牌为玩家1的底牌，第8、9个数所对应的牌为玩家2的底牌。
  - **计分方法scoring，以德州扑克规则判断牌型并给予分数。**实现方法为：首先对于传进来的参数(一个有五个 `Card` 类对象的 list)，对点数和花色分别排序。再针对排序结果进行分类讨论，判断参数属于的牌型。在积分方面采用 `16进制` 给分的方法。最高位是牌型，从同花顺~高牌依次按9~1赋值；次高位至最低位分别为排序后的最大点数至最小点数。通过比较不同的16进制数的大小，即可达到比较牌型的效果。
  - **裁判方法judge，发完5张公共牌和代表两个玩家的各2张底牌后，以德州扑克 (Poker) 规则判断赢家。**实现方法为：首先，枚举两位玩家7选5中被删除的牌，从而达到枚举7选5的效果。第二步，对于每一次枚举的7选5情况，调用 `scoring` 函数计算牌型和分值。保留每位玩家最高得分与该分数所对应的牌型，并输出牌型。第三步，比较两位玩家的分数，确定获胜者。
  - **开局方法new_game，新开一局并依次执行(1)(2)(3)。**

## 不足和改进

1. 不支持自选玩家数量的模拟。
  
   - 可能的解决方案：实现多玩家模拟功能。
2. 不同类型的牌判断方式不美观，仍基于传统的if-else形式。
  - 可能的解决方案：学习python高级语法，实现更美观的代码。
