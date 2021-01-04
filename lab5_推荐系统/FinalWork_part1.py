# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 12:27:34 2020

@author: brave
"""

'''
part1：基于用户的协同过滤推荐算法
实验要求：
        给定MovieLens数据集，包含电影评分，电影标签等文件，其中电影评分文件
    分为训练集train_set和test_set两部分。
        对训练集中的评分数据构造用户-电影效用矩阵，使用pearson相似度计算方法
    计算用户之间的相似度，也即相似度矩阵。对单个用户进行推荐时，找到与其最相似
    的K个用户，用这k个用户的评分情况对当前用户的所有未评分电影进行评分预测，选
    取评分最高的n个电影进行推荐。
        在测试集中包含100条用户-电影评分记录，用于计算推荐算法中预测评分的准
    确性，对预测集中的每个用户-电影需要计算其预测评分，再和真实评分进行对比，
    误差计算使用SSE误差平方和。
算法详情：
    1 找到与目标用户兴趣相似的用户集合
    2 找到这个集合中用户喜欢的，并且目标用户没有听说过的物品推荐给目标用户
    
Pearson:
    （1）0：X，Y两变量无关系
    （2）0.00~1.00：正相关
    （3）-1.00~0.00：负相关
    绝对值越大，相关性越强
    公式：
    ∑(X-X.mean())(Y-Y.mean())/( ∑(X-X.mean())^2 * ∑(Y-Y.mean())^2 )^0.5
'''
import pandas as pd
import numpy as np
import csv

#加载文件
def data_load(filename):
    #读取前三列：用户id、电影id、评分
    data_set = pd.read_csv(filename, usecols=['userId','movieId','rating'])
    #转换成用户评分矩阵
    global user_movie
    user_movie = data_set.pivot(index='userId',columns='movieId',values='rating')
    print(user_movie)

#构建评分向量
def build_xy(user_id1,user_id2):
    #找出两个user电影列表里的相同电影
    bool_array = user_movie.loc[user_id1].notnull() & user_movie.loc[user_id2].notnull()
    return user_movie.loc[user_id1, bool_array], user_movie.loc[user_id2, bool_array]

#pearson相似度计算
def pearson(user_id1, user_id2):
    x, y = build_xy(user_id1, user_id2)
    mean1, mean2 = x.mean(), y.mean()
    denominator = (sum((x-mean1)**2)*sum((y-mean2)**2))**0.5
    try:
        value = sum((x - mean1) * (y - mean2)) / denominator
    #两个变量的标准差不满足均不为0，即分母为0时
    except ZeroDivisionError:
        value = 0
    return value

#寻找最相似的k个用户
def find_Nearest_K_Users(user_id, k = 66):
    return user_movie.drop(user_id).index.to_series().apply(pearson, args=(user_id,)).nlargest(k)
 
#预测评分
def calculateRating(user_id, movie_id):
    nearest_user_id = find_Nearest_K_Users(user_id).index
    ans = []
    for i in nearest_user_id:
        #相近用户已评分但目标用户未评分的电影
        tmp = user_movie.loc[i, user_movie.loc[user_id].isnull() & user_movie.loc[i].notnull()].sort_values()
        if movie_id in tmp.index:
            ans.append(tmp[movie_id])
    ans = np.array(ans)
    if len(ans) == 0:
        result = -1
    else:
        result = ans.mean()
    return result

#测试函数
def test(filename):
    f = open('part1_final.txt','w')
    num = 0
    count = 0
    SSE = 0
    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    del rows[0]
    for i in rows:
        f.write("userId: "+i[0]+" movieId: "+i[1]+" 正确评分: "+i[2])
        tmp = calculateRating(int(i[0]), int(i[1]))
        num += 1
        print("calculate done one user ")
        print(num)
        if tmp == -1:
            f.write(" 预测评分: 缺失")
            print(" 缺失")
        else:
            print(" 可预测")
            f.write(" 预测评分: "+str(tmp))
            sse = (tmp-float(i[2]))**2
            SSE += sse
            count += 1
            f.write(" 误差平方: "+str(sse))
        f.write("\n")
    f.write("有预测结果的人数："+str(count))
    f.write("\n")
    f.write("SSE: "+str(SSE))
    f.close()
    print("work done")
       
if __name__ == '__main__':
    data_load('train_set.csv')
    test('test_set.csv')