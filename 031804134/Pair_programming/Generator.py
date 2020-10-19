import numpy as np


class Generator:
    def __init__(self):
        self.n = 3  # 棋盘阶数
        self.N = self.n * self.n  # 棋盘中棋子个数（包含空格）
        self.dict = {}  # 用于判重
        self.que_qi = []  # 用于广度优先搜索中，辅助队列(存储棋盘)
        self.que_bk = []  # 用于广度优先搜索中，辅助队列（存储空格）
        self.que_lv = []  # 用于广度优先搜索中，辅助队列（存储层数）
        self.deep = 31  # 遍历深度
        self.X = [-1, -self.n, 1, self.n]  # 棋子移动方位
        self.qi_init = ""  # 初始棋盘布局
        for i in range(1, self.N + 1):
            self.qi_init += str(i)

    def move(self, qi, blank, x, level):  # 将空格 blank 移向 x 位置
        if x < 0 or x >= self.N or blank == x:
            return
        if abs(blank % self.n - x % self.n) > 1:
            return
        if blank < x:
            temp = qi[:blank] + qi[x] + qi[blank + 1:x] + qi[blank] + qi[x + 1:]
        else:
            temp = qi[:x] + qi[blank] + qi[x + 1:blank] + qi[x] + qi[blank + 1:]
        if temp in self.dict:
            return
        self.dict[temp] = level + 1
        self.que_qi = [temp] + self.que_qi
        self.que_bk = [x] + self.que_bk
        self.que_lv = [level + 1] + self.que_lv

    def bfs(self):  # 广度优先搜索
        self.que_qi = [self.qi_init] + self.que_qi
        self.que_bk = [self.N - 1] + self.que_bk
        self.que_lv = [0] + self.que_lv
        self.dict[self.qi_init] = 0
        lv = 0
        while lv < self.deep and self.que_qi != []:
            qi = self.que_qi.pop()
            bk = self.que_bk.pop()
            lv = self.que_lv.pop()
            direction = np.random.permutation(4)  # 生成0~3的随机排列
            for i in direction:
                x = bk + self.X[i]
                self.move(qi, bk, x, lv)

    def save_jie3(self):  # 保存样本数据
        num = len(self.dict)
        data = np.zeros((num, self.N))
        label = np.zeros(num)
        i = 0
        for k in self.dict:
            label[i] = self.dict[k]
            for j in range(self.N):
                data[i][j] = float(k[j])
            i += 1
        np.savez("jie3.npz", data=data, label=label)

    def save_q_tab(self):  # 保存Query表
        k = list(self.dict.keys())
        v = list(self.dict.values())
        np.savez("q_tab.npz", k=k, v=v)

    def save_txt(self):  # 保存为TXT文档
        file = open("jie3.txt", 'w')
        s = ""
        for k in self.dict:
            v = self.dict[k]
            for i in range(self.N):
                s += k[i] + ' '
            s += str(v) + '\n'
        file.write(s)
        file.flush()
        file.close()


gen = Generator()
gen.bfs()
gen.save_jie3()
gen.save_q_tab()
gen.save_txt()