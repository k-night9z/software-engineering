import profile

if __name__ == '__main__':
    s1 = input("请输入要打开的原文件：")
    s2 = input("请输入要打开的对比文件：")
    vec1,vec2=get_word_vector(s1,s2)
    dist1=cos_dist(vec1,vec2)
    print(dist1)