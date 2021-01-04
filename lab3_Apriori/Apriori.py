# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 21:09:02 2020

@author: brave
"""

'''
关系的两种形式：
    频繁项集：数据集中经常出现在一块的物品的集合
    关联规则：两种物品之间可能存在很强的关系
衡量关系的指标：
    支持度：数据集中包含该项集的记录的比例
    置信度：类似条件概率 例如关联规则A->B，它的置信度为：支持度(A,B)/支持度B
题目要求：
    输出1~3阶频繁项集与关联规则，各个频繁项的支持度，各个规则的置信度，各阶频繁项集的数量以及关联规则的总数
    固定参数以方便检查，频繁项集的最小支持度为0.005，关联规则的最小置信度为0.5
'''

'''
文件预处理
'''
def loadDataSet(filename):
    f = open(filename,'r')
    dataSet = []
    for line in f:
        linelist = line.strip('\n').split(',')
        del linelist[0]
        linelist[0] = linelist[0][2:]
        length = len(linelist)
        linelist[length-1] = linelist[length-1][:-2]
        dataSet.append(linelist)
    del dataSet[0]
    return dataSet

'''
创建1项集
'''
def createC1(dataSet):
    C1 = []
    for transcation in dataSet:
        for item in transcation:
            if not {item} in C1:
                C1.append({item})
    C1.sort()
    return list(map(frozenset, C1))

'''
扫描数据集
'''
def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt.keys():
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []                        #频繁项集
    supportData = {}                    #候选项集支持度字典
    for key in ssCnt:
        support = ssCnt[key] / numItems
        supportData[key] = support
        if support >= minSupport:
            retList.append(key)
    return retList, supportData
    
'''
利用频繁项集构建候选项集
'''
def aprioriGen(Lk, k):
    Ck = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L1.sort()
            L2 = list(Lk[j])[:k - 2]
            L2.sort()
            if L1 == L2:
                Ck.append(Lk[i] | Lk[j])
    return Ck

'''
apriori主函数
'''
def apriori(D, minSupport):
    C1 = createC1(D)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (k < 4):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1
    return L, supportData

'''
关联规则
'''
def generateRules(L, supportData, minConf):
    ass_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = supportData[freq_set] / supportData[freq_set - sub_set]
                    ass_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= minConf and ass_rule not in ass_rule_list:
                        ass_rule_list.append(ass_rule)
            sub_set_list.append(freq_set)
    return ass_rule_list

if __name__ == '__main__':
    myData = loadDataSet("Groceries.csv")
    L, supportData = apriori(myData, 0.005)
    rules = generateRules(L, supportData, 0.5)
    #写入文件
    f = open('final.txt', "w")
    f.write("1阶总数："+str(len(L[0]))+"\n")
    f.write("2阶总数："+str(len(L[1]))+"\n")
    f.write("3阶总数："+str(len(L[2]))+"\n")
    f.write("关联规则总数："+str(len(rules))+"\n")
    f.write("1阶"+"\n")
    for i in L[0]:
        f.write(str(i)+"\n")
    
    f.write("2阶"+"\n")
    for i in L[1]:
        f.write(str(i)+"\n")
    
    f.write("3阶"+"\n")
    for i in L[2]:
        f.write(str(i)+"\n")
    
    f.write("关联规则"+"\n")
    for i in rules:
        f.write(str(i)+"\n")
    
    