import numpy as np
from Prediction import Prediction
from PIL import Image

class Qipan:
    def __init__(self):
        self.n = 3
        self.N = self.n * self.n
        self.init = np.arange(1, self.N + 1).reshape(self.n, self.n)
        self.qipan = self.init.copy()
        self.bk_x = self.n - 1
        self.bk_y = self.n - 1
        self.bk_x_p = -1
        self.bk_y_p = -1
        self.pre = Prediction()
        self.started = False  # 标记是否开始
        self.X = [-1, 0, 1, 0]
        self.Y = [0, -1, 0, 1]
        self.Ss = []

    def get_blank(img):
        """
        :param img: 带分割的图片
        :return: 空白格的初始位置
        """
        # save_path = 'text'
        # if not os.path.exists(save_path):
        #     os.mkdir(save_path)
        # else:
        #     row = 3
        #     col = 3
        #     if row > 0 and col > 0:
        #         split_image(img, row, col, save_path)
        #     else:
        #         print('无效的行列切割参数！')
        base_path = 'D:\Conda_pythonProject\code_of_software\partner\HuarongdaoAI\img\q_'
        for k in range(1,10):
            p = 100
            img_i = Image.open('D:\Conda_pythonProject\code_of_software\partner\HuarongdaoAI\img\q_' + str(k) + '.png')
            rgb_im = img_i.convert('RGB')
            for i in range(300):
                for j in range(300):
                    r, g, b = rgb_im.getpixel((i, j))
                    if r + g + b != 255 * 3:
                        p = k
                        break
                if p != 0:
                    break
            if p == 100:
                # print(k)
                return k

    def make_qipan(self):  # 生成随机棋盘
        max_step = 1000  # 随机生成移动棋子步数
        step = 0
        while step < max_step:
            i = np.random.randint(4)
            x = self.bk_x + self.X[i]
            y = self.bk_y + self.Y[i]
            self.move(x, y)
            step += 1
        self.bk_x_p = -1
        self.bk_y_p = -1
        self.step = 0  # 提示计步
        self.started = True  # 标记是否开始

    def move(self, x, y):  # 移动棋子
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            return
        self.qipan[self.bk_x][self.bk_y] = self.qipan[x][y]
        self.qipan[x][y] = self.N
        self.bk_x_p = self.bk_x
        self.bk_y_p = self.bk_y
        self.bk_x = x
        self.bk_y = y

    def is_finish(self):  # 判断游戏是否结束
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j] != self.init[i][j]:
                    return False
        return True

    def show(self):  # 打印当前棋盘状态
        s = ""
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j] == self.N:
                    s += "  "
                else:
                    s += str(self.qipan[i][j]) + " "
            s += "\n"
        print(s)

    def tips(self):  # 提示一步
        i = self.pre.pre_next(self.qipan, self.bk_x, self.bk_y, self.bk_x_p, self.bk_y_p)
        x = self.bk_x + self.X[i]
        y = self.bk_y + self.Y[i]
        self.move(x, y)
        self.step += 1
        print("step", self.step)
        if(self.step!=1):
            if (i == 0):
                print('w')
                self.Ss.append('w')
            if (i == 1):
                print('a')
                self.Ss.append('a')
            if (i == 2):
                print('s')
                self.Ss.append('s')
            if (i == 3):
                print('d')
                self.Ss.append('d')
        self.show()