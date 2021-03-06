# -*- coding: utf-8 -*-
import jieba
import numpy as np
import sys

def get_word_vector(s1, s2):
    """
    :param s1: 句子1
    :param s2: 句子2
    :return: 返回句子的余弦相似度
    """
    # 分词
    cut1 = jieba.cut(s1)
    cut2 = jieba.cut(s2)
    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    # 输出向量
    # print(word_vector1)
    # print(word_vector2)
    return word_vector1, word_vector2


def cos_dist(vec1, vec2):
    """
    :param vec1: 向量1
    :param vec2: 向量2
    :return: 返回两个向量的余弦相似度
    """
    ans = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return ans

def Format(fileName):
    try:
        with open(fileName, 'r', encoding='utf-8') as f:
            result = f.read()
            # sub用空字符替换标点符号
            result = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）：]+", "", result)
    #如果路径名无效或文件名不匹配
    except:
        print("读取失败")
    return result

# 命令行获取绝对路径
originFilePath = sys.argv[1]
fakeFilePath = sys.argv[2]
outputFilePath = sys.argv[3]
vec1, vec2 = get_word_vector(originFilePath, fakeFilePath)
ans = cos_dist(vec1, vec2)
#以字符串形式写入
ans=str(ans)
outputfile = open(outputFilePath, 'w', encoding='utf-8')
outputfile.write(ans)
outputfile.close()