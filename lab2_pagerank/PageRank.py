'''
PageRank：
    1.如果一个网页被很多其他网页链接到的话说明这个网页比较重要；
    2.如果一个PR值很高的网页链接到一个其他的网页，那么被链接的王爷的PR值也会相应的提高。

'''

import numpy as np

def handle_csv(filename):
    
    '''
    解析csv文件
        parameter:文件路径
        return:
            num_to_node:阿拉伯数字到节点的映射
            edges:边(表示节点关联关系)
    '''
    f = open(filename, 'r')
    
    #包含重复边
    tmp_edges = []
    for line in f:
        points = line.strip('\n').split(',')
        del points[0]
        tmp_edges.append(points)
    del  tmp_edges[0]
    
    #去重
    edges = []
    for edge in  tmp_edges:
        if edge not in edges:
            edges.append(edge)
            
    #获取节点集合
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
            
    #将节点映射为阿拉伯数字
    i = 0
    node_to_num = {}
    num_to_node = {}
    for node in nodes:
        node_to_num[node] = i
        num_to_node[i] = node
        i += 1
    for edge in edges:
        edge[0] = node_to_num[edge[0]]
        edge[1] = node_to_num[edge[1]]
        
    return num_to_node, edges

if __name__ == '__main__':
    
    num_to_node,edges = handle_csv("sent_receive.csv")
    N = len(num_to_node)
    
    #生成转移矩阵
    M = np.zeros([N, N])
    for edge in edges:
        M[edge[1], edge[0]] = 1
    for j in range(N):
        sum_of_col = sum(M[:, j])
        for i in range(N):
            if(sum_of_col != 0):
                M[i, j] /= sum_of_col
            else:
                M[i, j] = 0
                
    #阻尼系数
    β = 0.85
    A = β * M + (1 - β) / N * np.ones([N, N])

    #r:各个点当前PageRank值
    r = np.ones(N) / N
    tmp_r = np.zeros(N)

    #误差初始化
    e = 1

    #迭代计算
    while e > 0.00000001:
        tmp_r = np.dot(A, r)
        e = tmp_r - r
        e = max(map(abs, e))
        r = tmp_r

    #结果字典
    ans = {}
    i = 0
    for pagerank in r:
        node = num_to_node[i]
        ans [node] = pagerank
        i = i + 1
    
    #排序
    pagerank_list = list(ans .items())
    pagerank_list.sort(key = lambda x:x[1], reverse = True)
    
    #结果写入文件
    f = open('final.txt', "w")
    f.write("id      重要度"+" \n")
    for page in pagerank_list:
        f.write(page[0]+"      "+str(page[1])+" \n")