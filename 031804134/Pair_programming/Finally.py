# -*- coding: utf-8 -*-
import requests
import base64
import io
from PIL import Image
import os
import pygame
from pygame.locals import *
from sys import exit
import random

g_dict_layouts = {}
g_dict_layouts_deep = {}
g_dict_layouts_fn = {}
#每个位置可交换的位置集合
g_dict_shifts = {0:[1, 3], 1:[0, 2, 4], 2:[1, 5],
                 3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
                 6:[3,7],  7:[4,6,8], 8:[5,7]}
step_count = []
imgMap = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]
bg_color = (135, 206, 235)  # 设置背景色，天青蓝
STARTBOOL = True
RUNBOOL = False

def swap_chr(a, i, j, deep, destLayout):
    if i > j:
        i, j = j, i
    #得到ij交换后的数组
    b = a[:i] + a[j] + a[i+1:j] + a[i] + a[j+1:]
    #存储fn,A*算法
    fn = cal_dislocation_sum(b, destLayout)+deep
    # print(b)
    return b, fn
# 返回错码和正确码距离之和
def cal_dislocation_sum(srcLayout,destLayout):
    sum=0
    a= srcLayout.index("0")
    for i in range(0,9):
        if i!=a:
            sum=sum+abs(i-destLayout.index(srcLayout[i]))
            # print('sum:',sum)
            # print(destLayout.index(srcLayout[i]))
    return sum

def solvePuzzle_A(srcLayout, destLayout):
    #先进行判断srcLayout和destLayout逆序值是否同是奇数或偶数
    src=0;dest=0
    for i in range(1,9):
        fist=0
        for j in range(0,i):
          if srcLayout[j]>srcLayout[i] and srcLayout[i]!='0':#0是false,'0'才是数字
              fist=fist+1
              # print('fist',fist)
        src=src+fist
        # print(src)
    for i in range(1,9):
        fist=0
        for j in range(0,i):
          if destLayout[j]>destLayout[i] and destLayout[i]!='0':
              fist=fist+1
        dest=dest+fist
    if (src%2)!=(dest%2):#一个奇数一个偶数，不可达
        return -1, None
    g_dict_layouts[srcLayout] = -1
    g_dict_layouts_deep[srcLayout]= 1
    g_dict_layouts_fn[srcLayout] = 1 + cal_dislocation_sum(srcLayout, destLayout)
    stack_layouts = []
    gn=0#深度值
    stack_layouts.append(srcLayout)#当前状态存入列表
    while len(stack_layouts) > 0:
        curLayout = min(g_dict_layouts_fn, key=g_dict_layouts_fn.get)
        del g_dict_layouts_fn[curLayout]
        stack_layouts.remove(curLayout)#找到最小fn，并移除
        # curLayout = stack_layouts.pop()
        if curLayout == destLayout:#判断当前状态是否为目标状态
            break
        # 寻找0 的位置。
        ind_slide = curLayout.index("0")
        lst_shifts = g_dict_shifts[ind_slide]#当前可进行交换的位置集合
        for nShift in lst_shifts:
            newLayout, fn = swap_chr(curLayout, nShift, ind_slide, g_dict_layouts_deep[curLayout] + 1, destLayout)
            if g_dict_layouts.get(newLayout) == None:#判断交换后的状态是否已经查询过
                g_dict_layouts_deep[newLayout] = g_dict_layouts_deep[curLayout] + 1#存入深度
                g_dict_layouts_fn[newLayout] = fn#存入fn
                g_dict_layouts[newLayout] = curLayout#定义前驱结点
                stack_layouts.append(newLayout)#存入集合
    lst_steps = []
    lst_steps.append(curLayout)
    while g_dict_layouts[curLayout] != -1:#存入路径
        curLayout = g_dict_layouts[curLayout]
        lst_steps.append(curLayout)
    lst_steps.reverse()
    return 0, lst_steps

def get_json(url):
    """
    :param url: 获取json数据的URL
    :return: 图片，强制交换的步数，强制交换的格子，题目编号
    """
    html = requests.get(url)  # 获取json文件
    html_json = html.json()
    img_str = html_json['img']
    step = html_json['step']
    swap = html_json['swap']
    uuid = html_json['uuid']
    img_b64decode = base64.b64decode(img_str)  # base64解码
    file = open('test.jpg', 'wb')
    file.write(img_b64decode)
    file.close()
    # img_array = np.fromstring(img_b64decode, np.uint8)  # 转换np序列
    # img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式
    # print(img.size)
    # cv2.imshow("img", img)
    # cv2.waitkeyey()
    image = io.BytesIO(img_b64decode)
    img = Image.open(image)
    return img, step, swap, uuid

def split_image(img, row_num, col_num, save_path):  # 图片的分割保存
    """
    :param img: 带分割的图片
    :param row_num: 分割的行数
    :param col_num: 分割的列数
    :param save_path: 图片存放文件夹
    :return: None
    """
    w, h = img.size  # 图片大小
    if row_num <= h and col_num <= w:
        print('original image info:%sx%s,%s,%s' % (w, h, img.format, img.mode))
        print('开始处理图片切割，请稍候-')
        ext = 'jpg'
        num = 0
        rowheight = h//row_num
        colwidth = w//col_num
        for r in range(row_num):
            for c in range(col_num):
                box = (c*colwidth, r*rowheight, (c+1)*colwidth, (r+1)*rowheight)
                img.crop(box).save(os.path.join(save_path, str(num) + '.' + ext))
                num = num + 1
        print('图片切割完毕，共生成%s张小图片。' % num)
    else:
        print('不合法的行列切割参数！')

def get_blank(img):
    """
    :param img: 带分割的图片
    :return: 空白格的初始位置
    """
    save_path = 'ori_split'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    row = 3
    col = 3
    if row > 0 and col > 0:
        split_image(img, row, col, save_path)
    else:
        print('无效的行列切割参数！')
    for k in range(9):
        p = 100
        img_i = Image.open(save_path + '//' + str(k) + '.jpg')
        rgb_im = img_i.convert('RGB')
        for i in range(300):
            for j in range(300):
                r, g, b = rgb_im.getpixel((i, j))
                if r + g + b != 255 * 3:  # 白色(255,255,255)
                    p = k
                    break
            if p != 0:
                break
        if p == 100:
            print(k)
            return k

def move(x, y, step_sum, event):  # 实现空白格移动
    """
    :param x: imgMap行坐标
    :param y: imgMap列坐标
    :param event: 键盘事件
    :return: 更新的imgMap行，列坐标
    """
    if event.type == KEYDOWN:   # 键盘有按下？
        if (event.key == K_a) and y != 0:
            # 左移
            imgMap[x][y], imgMap[x][y - 1] = imgMap[x][y - 1], imgMap[x][y]
            y = y - 1
            step_sum += 1
        elif ( event.key == K_d) and y != 2:
            # 右移
            imgMap[x][y], imgMap[x][y + 1] = imgMap[x][y + 1], imgMap[x][y]
            y = y + 1
            step_sum += 1
        elif (event.key == K_w) and x != 0:
            # 上移
            imgMap[x][y], imgMap[x - 1][y] = imgMap[x - 1][y], imgMap[x][y]
            x = x - 1
            step_sum += 1
        elif ( event.key == K_s) and x != 2:
            # 下移
            imgMap[x][y], imgMap[x + 1][y] = imgMap[x + 1][y], imgMap[x][y]
            x = x + 1
            step_sum += 1

    return x, y, step_sum

def move_char(x, y, step_sum, ch):  # 实现空白格移动
    """
    :param x: imgMap行坐标
    :param y: imgMap列坐标
    :param event: 键盘事件
    :return: 更新的imgMap行，列坐标
    """
    if ch == 'a' and y != 0:
        # 左移
        imgMap[x][y], imgMap[x][y - 1] = imgMap[x][y - 1], imgMap[x][y]
        y = y - 1
        step_sum += 1
    elif ch == 'd' and y != 2:
        # 右移
        imgMap[x][y], imgMap[x][y + 1] = imgMap[x][y + 1], imgMap[x][y]
        y = y + 1
        step_sum += 1
    elif ch == 'w' and x != 0:
        # 上移
        imgMap[x][y], imgMap[x - 1][y] = imgMap[x - 1][y], imgMap[x][y]
        x = x - 1
        step_sum += 1
    elif ch == 's' and x != 2:
        # 下移
        imgMap[x][y], imgMap[x + 1][y] = imgMap[x + 1][y], imgMap[x][y]
        x = x + 1
        step_sum += 1
    return x, y, step_sum

def count_sum(img_i):
    count_up, count_down, count_left, count_right = 0, 0, 0, 0
    count_list = []
    start_list = []
    rgb_im = img_i.convert('RGB')
    t = 0
    for i in range(300):  # 上侧(i,0)
        r, g, b = rgb_im.getpixel((i, 0))
        if r + g + b == 255*3:
            count_up += 1
        if count_up != 0 and t == 0:
            start_list.append(i)
            t += 1
    count_list.append(count_up)
    if count_up == 0:
        start_list.append(999)
    t = 0
    for i in range(300):  # 下侧(i,299)
        r, g, b = rgb_im.getpixel((i, 299))
        if r + g + b == 255*3:
            count_down += 1
        if count_down != 0 and t == 0:
            start_list.append(i)
            t += 1
    count_list.append(count_down)
    if count_down == 0:
        start_list.append(999)
    t = 0
    for i in range(300):  # 左侧(0,i)
        r, g, b = rgb_im.getpixel((0, i))
        if r + g + b == 255*3:
            count_left += 1
        if count_left != 0 and t == 0:
            start_list.append(i)
            t += 1
    count_list.append(count_left)
    if count_left == 0:
        start_list.append(999)
    t = 0
    for i in range(300):  # 右侧(299,i)
        r, g, b = rgb_im.getpixel((299, i))
        if r + g + b == 255*3:
            count_right += 1
        if count_right != 0 and t == 0:
            start_list.append(i)
            t += 1
    count_list.append(count_right)
    if count_right == 0:
        start_list.append(999)

    return count_list, start_list

def first_find():
    IMAGES_PATH = 'ori_split'
    IMAGES_FORMAT = ['.jpg']
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]
    IMAGES_PATH2 = 'text'
    image_names2 = [name for name in os.listdir(IMAGES_PATH2) for item in IMAGES_FORMAT if
                    os.path.splitext(name)[1] == item]
    # print(image_names2)
    print('图片比对中，请稍等...')
    for name in image_names:
        img = Image.open(IMAGES_PATH + '//' + name)
        img = img.convert('RGB')
        img_rgb = 0
        for i in range(300):
            for j in range(300):
                r, g, b = img.getpixel((i, j))
                img_rgb += r + b + g
        if img_rgb == 300*300*255 or img_rgb == 0:
            continue
        # print(img_rgb)
        for name2 in image_names2:
            for k in range(9):
                img_i = Image.open(IMAGES_PATH2 + '//' + name2 + '//' + str(k) + '.jpg')
                img_i = img_i.convert('RGB')
                img_rgb2 = 0
                for i in range(300):
                    for j in range(300):
                        r, g, b = img_i.getpixel((i, j))
                        img_rgb2 += r + b + g
                if img_rgb == img_rgb2:
                    print(name2)
                    return name2

def second_find(path):
    win_list = []
    IMAGES_PATH = 'ori_split'
    IMAGES_FORMAT = ['.jpg']
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]
    IMAGES_PATH2 = 'text'
    # print(image_names)
    for name in image_names:
        img = Image.open(IMAGES_PATH + '//' + name)
        img = img.convert('RGB')
        img_rgb = 0
        for i in range(300):
            for j in range(300):
                r, g, b = img.getpixel((i, j))
                img_rgb += r + b + g
        if img_rgb == 300 * 300 * 255 * 3:
            win_list.append(9)
            continue
        # print(img_rgb)
        for k in range(9):
            img_i = Image.open(IMAGES_PATH2 + '//' + path + '//' + str(k) + '.jpg')
            img_i = img_i.convert('RGB')
            img_rgb2 = 0
            for i in range(300):
                for j in range(300):
                    r, g, b = img_i.getpixel((i, j))
                    img_rgb2 += r + b + g
            if img_rgb == img_rgb2:
                win_list.append(k)
                break
    return win_list

def get_final(winmap):
    # IMAGES_PATH2 = 'text'
    to_image = Image.new('RGB', (3 * 300, 3 * 300))  # 创建一个新图
    for i in range(9):
            from_image = Image.open('ori_split' + '//' + str(winmap[i]) + '.jpg').resize(
                (300, 300), Image.ANTIALIAS)
            to_image.paste(from_image, (i % 3 * 300, i // 3 * 300))  # 列，行
    to_image.save('final.jpg')

def start_screen(screen):
    global STARTBOOL, RUNBOOL
    start_surface = pygame.Surface(screen.get_size())
    start_surface = start_surface.convert()
    start_surface.fill(bg_color)
    my_font = pygame.font.SysFont("ITCKRIST.TTF", 55)
    text_surface = my_font.render("Pygame is cool!", True, (0, 0, 0))
    start_button = my_font.render("play", True, (0, 0, 0))
    pygame.time.delay(32)  # 延时32毫秒,相当于FPS=32
    while STARTBOOL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 检测玩家单击游戏窗口关闭按钮
                exit()  # 退出游戏
            elif event.type == pygame.MOUSEBUTTONDOWN and 300 <= event.pos[0] <= 550 and 200 <= event.pos[
                1] <= 250:  # 判断鼠标位置以及是否摁了下去。
                STARTBOOL = False
                RUNBOOL = True
        # 每次循环时都重绘屏幕
        screen.blit(start_surface, (0, 0))
        screen.blit(text_surface, (250, 100))
        screen.blit(start_button, (330, 200))
        pygame.draw.rect(start_surface, (255, 0, 0), (300, 200, 150, 50))
        pygame.display.flip()

def win_change(win):
    init_blank = 9
    for i in range(9):
        if i not in win:
            init_blank = i
            # print(init_blank)
            for j in range(9):
                if win[j] == 9:
                    win[j] = i
    print(win)
    win_map = [9, 9, 9, 9, 9, 9, 9, 9, 9]
    for i in range(9):
        for j in range(9):
            if win[j] == i :
                win_map[i] = j
    print(win_map)
    return  win_map,init_blank

def step_change(blank, x, y, swap):
    xx = []
    yy = []
    for i in range(3):
        for j in range(3):
            if imgMap[i][j] == swap[0] - 1:
                xx.append(i)
                yy.append(j)
    for i in range(3):
        for j in range(3):
            if imgMap[i][j] == swap[1] - 1:
                xx.append(i)
                yy.append(j)
    imgMap[xx[0]][yy[0]], imgMap[xx[1]][yy[1]] = imgMap[xx[1]][yy[1]], imgMap[xx[0]][yy[0]]
    if blank == swap[0] - 1:
        x, y = xx[1], yy[1]
    elif blank == swap[1] - 1:
        x, y = xx[0], yy[0]
    return x, y

def get_ori_final(init_blank, win):
    winner = [str(i) for i in win]
    # for i in range(len(winner)):
    #     if winner[i] == str(init_blank):
    #         winner[i] = '0'
    #     elif winner[i] == '0':
    #         winner[i] = str(init_blank)
    # print('winner:',winner)
    dest = []
    for i in range(9):
        dest.append(str(i))
    for i in range(len(dest)):
        if dest[i] == str(init_blank):
            dest[i] = '0'
        elif dest[i] == '0':
            dest[i] = str(init_blank)
    # print('dest:',dest)
    win_str = ''.join(winner)
    dest_str = ''.join(dest)
    # print(win_str)
    srcLayout = win_str
    destLayout = dest_str
    return  srcLayout, destLayout

def Astarmain(srcLayout,destLayout):
    Ss = []
    retCode, lst_steps = solvePuzzle_A(srcLayout, destLayout)
    if retCode != 0:
        print("开始尝试自由交换")
        list_srcLayout = list(srcLayout)
        print(list_srcLayout)
        list1 = list_srcLayout
        for i in range(0,9):
            # if(i == 8):
            #     print("目标布局不可达")
            #     return 's' * 100
            for j in range(i+1,9):
                #开始自由交换
                tt = list_srcLayout[j]
                list_srcLayout[j] = list_srcLayout[i]
                list_srcLayout[i] = tt
                print(list_srcLayout[i])
                print(list_srcLayout[j])
                print(list_srcLayout)
                print('j',j)
                srcLayout2 = ''.join(list_srcLayout)
                print(srcLayout2)
                retCode, lst_steps = solvePuzzle_A(srcLayout2, destLayout)
                if retCode != 0:
                    print("暂时无解")
                    list_srcLayout = list1
                    continue
                else:
                    print('自由交换第(%s)和第(%s)块(原本的位置，它们现在的位置是第（%d）和（%d）)'%(list_srcLayout[i],list_srcLayout[j],i+1,j+1))
                    for nIndex in range(len(lst_steps)):
                        a = lst_steps[nIndex].index("0")
                        b = lst_steps[nIndex - 1].index("0")
                        if (nIndex > 0):
                            if (b - a == 3):
                                Ss.append('w')
                                # print('w')
                            if (b - a == -3):
                                Ss.append('s')
                                # print('s')
                            if (b - a == 1):
                                Ss.append('a')
                                # print('a')
                            if (b - a == -1):
                                Ss.append('d')
                                # print('d')
                s = ''.join(Ss)
                print("经过自由交换以后得到解")
                return s
        print("目标布局不可达")
        return 's'*100
    else:
        for nIndex in range(len(lst_steps)):
            a = lst_steps[nIndex].index("0")
            b = lst_steps[nIndex - 1].index("0")
            if (nIndex > 0):
                if (b - a == 3):
                    Ss.append('w')
                    # print('w')
                if (b - a == -3):
                    Ss.append('s')
                    # print('s')
                if (b - a == 1):
                    Ss.append('a')
                    # print('a')
                if (b - a == -1):
                    Ss.append('d')
                    # print('d')
    s = ''.join(Ss)
    # print(s)
    return s

def winwin(win, init_blank, step, swap):
    x1 = win[swap[0] - 1]
    x2 = win[swap[1] - 1]
    new_blank = 9
    for i in range(9):
        if win[i] == 0:
            win[i] = init_blank
            if init_blank == 0:
                new_blank = i
        elif win[i] == init_blank:
            win[i] = 0
            new_blank = i
    print(win)
    first_list = []
    if step % 2 == 0:
        if new_blank <= 5:
            first_list.append('sw'*(step // 2))
        elif 9 > new_blank > 5:
            first_list.append('ws' * (step // 2))
        elif new_blank >=9:
            print('new_blank >= 9')

    else:
        if new_blank <= 5:
            first_list.append('sw'*(step // 2) + 's')
            win[new_blank], win[new_blank + 3] = win[new_blank + 3], win[new_blank]
        elif 9 > new_blank > 5:
            first_list.append('ws' * (step // 2) + 'w')
            win[new_blank], win[new_blank - 3] = win[new_blank - 3], win[new_blank]
        elif new_blank >=9:
            print('new_blank >= 9')
    print(win)
    # print(first_list)
    xx1 = 9
    xx2 = 9
    for i in range(9):
        if win[i] == x1:
            xx1 = i
        elif win[i] == x2:
            xx2 = i
    win[xx1], win[xx2] = win[xx2], win[xx1]
    # win[swap[0] - 1], win[swap[1] - 1] = win[swap[1] - 1], win[swap[0] - 1]
    return win, first_list

def run_screen(screen, blank, step, swap, win_map_array, s):
    global RUNBOOL, imgMap
    x = blank // 3
    y = blank % 3
    # pygame.key.set_repeat(10, 15)  # 键盘连续按下实现
    img_surface = pygame.image.load('test.jpg')  # pygame使用的图片(surface类型)
    img_surface = pygame.transform.scale(img_surface, (300, 300))  # 图片缩放
    final_surface = pygame.image.load('final.jpg')
    final_surface = pygame.transform.scale(final_surface, (200, 200))
    my_font = pygame.font.SysFont("ITCKRIST.TTF", 55)
    step_surface = my_font.render("step", True, (0, 0, 0))
    replay_surface = my_font.render("replay", True, (0, 0, 0))
    rule_surface = my_font.render("rule:change img"+ str(swap[0]) + ',img' + str(swap[1]) + ', when step == ' + str(step), True, (0, 0, 0))
    step_num = 0
    # 游戏主循环
    t = 0
    while RUNBOOL:
        if imgMap == win_map_array and t == 0:
            print(imgMap)
            print('Succeed!')
            t = 1
        for event in pygame.event.get():  # 窗口的关闭事件
            if event.type == pygame.QUIT:
                exit()
            elif event.type == KEYDOWN:
                x, y, step_num = move(x, y, step_num, event)
            elif event.type == pygame.MOUSEBUTTONDOWN and 480 <= event.pos[0] <= 630 and 300 <= event.pos[
                1] <= 350:  # 判断鼠标位置以及是否摁了下去。
                imgMap = [
                    [0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8]
                ]
                x = blank // 3
                y = blank % 3
                step_num = 0
                t = 0
        screen.fill(bg_color)  # 背景色填充
        step_num_surface = my_font.render(str(step_num), True, (0, 0, 0))
        screen.blit(step_num_surface,(300,325))
        # 绘图
        for i in range(3):
            for j in range(3):
                value = imgMap[i][j]
                dx = (value % 3) * 100  # 计算绘图偏移量
                dy = (int(value / 3)) * 100
                screen.blit(img_surface, (j * 100, i * 100), (dx, dy, 100, 100))
        # 画参考图片
        screen.blit(final_surface, (400, 0))
        screen.blit(step_surface, (50, 325))
        screen.blit(rule_surface, (50, 425))
        pygame.draw.rect(screen, (255, 0, 0), (480, 300, 150, 50))
        pygame.draw.rect(screen, (255, 0, 0), (480, 370, 150, 50))
        screen.blit(replay_surface, (500, 300))
        if step == step_num and swap[0] != swap[1]:
            x, y = step_change(blank, x, y, swap)
            step_num += 1
        elif step == step_num and swap[0] == swap[1]:  # 强制交换
            step_num += 1
        for i in range(4):
            pygame.draw.line(screen, (255, 0, 0), (i * 100, 0), (i * 100, 300))
        for i in range(4):
            pygame.draw.line(screen, (255, 0, 0), (0, i * 100), (300, i * 100))
        pygame.display.flip()  # 刷新界面

def get_challenge_list():  # 获取今日的赛题，以列表方式展示所有的赛题
    url = 'http://47.102.118.1:8089/api/challenge/list'
    html = requests.get(url)  # 获取json文件
    html_json = html.json()
    print(html_json)
    return html_json

def get_challenge_record(uuid):  # 获取赛题的解题记录，返回所有解出这题的队伍的纪录
    url = 'http://47.102.118.1:8089/api/challenge/record/'
    url = url + uuid
    html = requests.get(url)  # 获取json文件
    html_json = html.json()
    print(html_json)

def creat():
    url = 'http://47.102.118.1:8089/api/challenge/create'
    data = {
        "teamid": 57,
        "data": {
            "letter": "w",
            "exclude": 5,
            "challenge": [
                [1, 3, 0],
                [9, 8, 7],
                [2, 6, 4]
            ],
            "step": 19,
            "swap": [1, 2]
        },
        "token": "965d5fbe-4e91-4a89-9f97-fdbe611ecd5a"
    }
    r = requests.post(url, json=data)
    r_json = r.json()
    # 'uuid': '1058aabd-d1bc-43f8-af23-f87faf4f8b2c'
    print(r_json)

def start(uuid):
    url = 'http://47.102.118.1:8089/api/challenge/start/' + uuid
    teamdata = {
        "teamid": 57,
        "token": "965d5fbe-4e91-4a89-9f97-fdbe611ecd5a"
    }
    r = requests.post(url, json=teamdata)
    r_json = r.json()
    print(r_json)
    chanceleft = r_json['chanceleft']
    img_str = r_json['data']['img']
    step = r_json['data']['step']
    swap = r_json['data']['swap']
    uuid = r_json['uuid']
    img_b64decode = base64.b64decode(img_str)  # base64解码
    file = open('test.jpg', 'wb')
    file.write(img_b64decode)
    file.close()
    image = io.BytesIO(img_b64decode)
    img = Image.open(image)
    return img, step, swap, uuid

def up_data(uuid, answer):
    url_up = 'http://47.102.118.1:8089/api/challenge/submit'
    updata = {
        "uuid": uuid,
        "teamid": 57,
        "token": "965d5fbe-4e91-4a89-9f97-fdbe611ecd5a",
        "answer": {
            "operations": answer,
            "swap": []
        }
    }
    r_up = requests.post(url_up, json=updata)
    r_up_json = r_up.json()
    print(r_up_json)

def main():
    pygame.init()  # 初始化
    pygame.display.set_caption('拼图游戏')  # 窗口标题
    img, step, swap, uuid = start('e9d5727c-57fa-4182-a1fd-24b43fd392ce')
    print(step, swap)
    blank = get_blank(img)  # 空白块位置坐标
    ori_path = first_find()
    win = second_find(ori_path)
    win_map, init_blank = win_change(win)
    # print(win)
    # print(win_map)
    # print(init_blank)
    win2, s1 = winwin(win, init_blank, step, swap)
    srcLayout, destLayout = get_ori_final(init_blank, win2)
    s2= Astarmain(srcLayout, destLayout)
    print(s1)
    print(s2)
    s = ''
    if len(s2) < 100 and s1[0] != []:
        s = s1[0] + s2
        print(s)
    print(srcLayout)
    print(destLayout)
    get_final(win_map)
    win_map_array = [
        [win_map[0],win_map[1],win_map[2]],
        [win_map[3],win_map[4],win_map[5]],
        [win_map[6],win_map[7],win_map[8]]
    ]
    screen = pygame.display.set_mode((800, 500), RESIZABLE)  # 窗口大小
    start_screen(screen)
    run_screen(screen, blank, step, swap,win_map_array, s)


if __name__ == '__main__':
    main()

