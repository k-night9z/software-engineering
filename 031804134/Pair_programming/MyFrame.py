from Qipan import Qipan
import wx
import threading
import time
from PIL import Image

class MyFrame(wx.Frame):
    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id, title='数字华容道', size=(370, 450))
        panel = wx.Panel(self)
        self.qipan = Qipan()
        self.bt_start = wx.Button(panel, size=(80, 45), label='开始')
        self.bt_start.Bind(wx.EVT_BUTTON, self.OnClickStart)
        self.label_step = wx.StaticText(panel, label="0")
        font_lab = wx.Font(18, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        self.label_step.SetFont(font_lab)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.bt_start, proportion=0, flag=wx.RIGHT | wx.ALIGN_CENTER, border=100)
        hsizer.Add(self.label_step, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=20)

        grid_sizer = wx.GridSizer(3, 3, 2, 2)  # 3*3网格，组件边界为2
        base_path = 'D:\Conda_pythonProject\code_of_software\partner\HuarongdaoAI\img\q_'
        self.img_id = []
        self.bmp_qi = []
        for i in range(self.qipan.n):
            img_t = []
            bmp_t = []
            for j in range(self.qipan.n):
                img_t += [wx.Image(base_path + str(i * self.qipan.n + j) + '.png').Rescale(100,100).ConvertToBitmap()]
                bmp_t += [wx.StaticBitmap(panel, -1, img_t[j])]
                grid_sizer.Add(bmp_t[j], 0)
            self.img_id += [img_t]
            self.bmp_qi += [bmp_t]

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER | wx.ALIGN_TOP)
        vsizer.Add(grid_sizer, 0, wx.ALIGN_CENTER)
        panel.SetSizer(vsizer)

    def OnClickStart(self, event):
        if self.qipan.is_finish():  # 开局
            self.qipan.make_qipan()
            self.draw()
            self.label_step.SetLabel(str(self.qipan.step))
            threading.Thread(target=self.demo).start()
            self.bt_start.SetLabel("暂停")
        elif not self.qipan.started:  # 开始
            self.qipan.started = True
            self.bt_start.SetLabel("暂停")    
        else:  # 暂停
            self.qipan.started = False
            self.bt_start.SetLabel("开始")

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
        for k in range(0,9):
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

    def update(self):
        while self.qipan.started == False:
            time.sleep(0.2)
        self.qipan.tips()
        x = (self.qipan.qipan[self.qipan.bk_x_p][self.qipan.bk_y_p] - 1) // self.qipan.n
        y = (self.qipan.qipan[self.qipan.bk_x_p][self.qipan.bk_y_p] - 1) % self.qipan.n
        self.bmp_qi[self.qipan.bk_x_p][self.qipan.bk_y_p].SetBitmap(self.img_id[x][y])
        self.bmp_qi[self.qipan.bk_x][self.qipan.bk_y].SetBitmap(self.img_id[self.qipan.n - 1][self.qipan.n - 1])
        self.label_step.SetLabel(str(self.qipan.step))

    def demo(self):
        while self.qipan.is_finish() == False:
            time.sleep(0.8)
            self.update()
        print("success!")
        print(self.qipan.Ss)
        k = self.get_blank()
        print(k)
        # self.qipan.tips()
        # x = (self.qipan.qipan[self.qipan.bk_x_p][self.qipan.bk_y_p] - 1) // self.qipan.n
        # y = (self.qipan.qipan[self.qipan.bk_x_p][self.qipan.bk_y_p] - 1) % self.qipan.n
        # self.bmp_qi[self.qipan.bk_x_p][self.qipan.bk_y_p].SetBitmap(self.img_id[x][y])
        # self.bmp_qi[self.qipan.bk_x][self.qipan.bk_y].SetBitmap(self.img_id[self.qipan.n - 1][self.qipan.n - 1])
        # self.label_step.SetLabel(str(self.qipan.step))
        self.qipan.started = False
        self.bt_start.SetLabel("开始")

    def draw(self):
        for i in range(self.qipan.n):
            for j in range(self.qipan.n):
                x = (self.qipan.qipan[i][j] - 1) // self.qipan.n
                y = (self.qipan.qipan[i][j] - 1) % self.qipan.n
                self.bmp_qi[i][j].SetBitmap(self.img_id[x][y])

    # def over(self):
    #     for i in range(self.qipan.n):
    #         for j in range(self.qipan.n):
    #             x = 1
    #             y = 0
    #             self.bmp_qi[i][j].SetBitmap(self.img_id[x][y])


app = wx.App()
frame = MyFrame()
img = wx.Image()
frame.Show()
app.MainLoop()