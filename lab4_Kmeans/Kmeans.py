# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 14:59:21 2020

@author: brave
"""

import numpy as np 
import random

final_centers = []
times = 0

'''
数据预处理
'''
def getData(filename): 
    f = open(filename, "r")
    data = []
    ans = []
    for line in f:
        tmp = []
        linelist = line.strip('\n').split(',')
        ans.append(float(linelist[0]))
        del linelist[0]
        for num in linelist:
            num = float(num)
            tmp.append(num)
        data.append(tmp)
    return np.array(data), np.array(ans)

'''
聚类
'''
def classify(data, centers):
    length = centers.shape[0]
    classes = [[] for i in range(length)]
    
    for i in range(data.shape[0]):
        per_data = data[i]
        #计算平方和
        diffMat = np.tile(per_data, (length, 1)) - centers
        sqDiffMat = diffMat**2
        sqDisMat = sqDiffMat.sum(axis=1)
        #排序
        sortedIndex = sqDisMat.argsort()
        #数据插入对应属性
        classes[sortedIndex[0]].append(list(per_data))
    return classes
        
'''
质心更新
'''
def updateCenters(classes):
    centers = []
    for i in range(len(classes)):
        per_class = classes[i]
        per_class = np.array(per_class)
        center = per_class.sum(axis=0)/len(per_class)
        centers.append(center)
    return np.array(centers)

'''
主函数
'''
def kmeans(data, centers):
    global times
    times += 1
    print("enter kmeans "+str(times))
    #聚类
    classes = classify(data, centers)
    #修改中心点
    newCenters = updateCenters(classes)
    if (newCenters == centers).all():
        global final_centers
        final_centers = centers
        return 
    kmeans(data, newCenters)
    
'''
结果分析
'''
def calculateResult(myData, ans, final_centers):
    right = 0
    f = open('final.txt', "w")
    length = centers.shape[0]
    for i in range(myData.shape[0]):
        per_data = myData[i]
        diffMat = np.tile(per_data, (length, 1)) - final_centers
        sqDiffMat = diffMat**2
        sqDisMat = sqDiffMat.sum(axis=1)
        sortedIndex = sqDisMat.argsort()
        f.write("正确属性："+str(int(ans[i]))+"  预测属性："+str(sortedIndex[0]+1)+"  到正确质心平方和："+str(sqDisMat[int(ans[i]) - 1])+"\n")
        if sortedIndex[0] + 1 == int(ans[i]):
            right += 1
    f.write("正确率："+str(right/myData.shape[0]))
    print(right)
    print(right/myData.shape[0])
    
if __name__ == '__main__':
    myData, ans = getData("WineData.data")
    centers = [myData[random.randint(0, 58)], myData[random.randint(59, 129)], myData[random.randint(130, myData.shape[0]-1)]]
    centers = np.array(centers)
    kmeans(myData, centers)
    calculateResult(myData, ans, final_centers)