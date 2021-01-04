import pandas as pd
from numpy import *
import numpy as np

'''
    创建以电影类别为键,Id为值的字典,类别到数字的映射关系,电影名到数字的映射关系
'''
def loadDataSet():
    movies = pd.read_csv('movies.csv')
    movies_genres = movies['genres']
    movies_Ids = movies['movieId']
    # 创建电影类别的字典
    movies_genres_dict = {}
    for i in range(len(movies_genres)):
        genres = movies_genres[i].split('|')
        movies_genres[i] = genres
        for genre in genres:
            if genre != '(no genres listed)':
                movies_genres_dict.setdefault(genre, []).append(movies_Ids[i])
    # 建立类别到数字的映射关系(0-18)
    genre_to_num = {}
    i = 0
    for genre in movies_genres_dict:
        genre_to_num[genre] = i
        i += 1
    # 建立电影Id到数字的映射关系(0-9124)
    Id_to_num = {}
    i = 0
    for Ids in movies_Ids:
        Id_to_num[Ids] = i
        i += 1
    return movies_genres_dict, genre_to_num, Id_to_num, movies_genres

'''
    得到训练集的userId{movieId:rating}的字典关系
'''
def loadTrainSet():
    trainSet = pd.read_csv('train_set.csv')
    user_Ids = trainSet['userId']
    movie_Ids = trainSet['movieId']
    rating = trainSet['rating']
    userIds = [0]*672
    movieIds = {}
    for i in range(len(user_Ids)):
        movieIds[movie_Ids[i]] = rating[i]
        #当前用户的最后一个评价
        if (i != len(user_Ids) - 1) and (user_Ids[i] != user_Ids[i+1]):
            userIds[user_Ids[i]] = movieIds
            movieIds = {}
    userIds[671] = movieIds
    return userIds

'''
    得到关于电影与特征值的n(电影个数)*m(特征值个数)的tf-idf特征矩阵
    :param movies_genres_dict:
    :return:
'''
def get_tfidf_matrix(movies_genres_dict, genre_to_num, Id_to_num, movies_genres):
    # 计算每个类在不同的电影(文档)的tf_idf值
    tfidf_matrix = np.zeros((9125, 19))
    for genre in movies_genres_dict:
        j = genre_to_num[genre]
        idf = math.log(9125 / len(movies_genres_dict[genre]), 10)
        for Id in movies_genres_dict[genre]:
            i = Id_to_num[Id]
            l = len(movies_genres[i])
            tf = 1 / l
            tfidf_matrix[i, j] = idf * tf
    return tfidf_matrix

'''
    用余弦相似度的计算方法，得到相似度矩阵
'''
def get_similarity_matrix(tfidf_matrix):
    # 1925×19
    n = len(tfidf_matrix) #1925
    for i in range(n):
        a = np.dot(tfidf_matrix[i], tfidf_matrix[i])
        if a != 0:
            tfidf_matrix[i] = tfidf_matrix[i] / math.sqrt(a)
    similarity_matrix = np.dot(tfidf_matrix, tfidf_matrix.T)
    return similarity_matrix

'''
    获取01矩阵：如果电影存在某特征值，则特征值为1，不存在则为0
'''
def get_01_matrix(movies_genres_dict, genre_to_num, Id_to_num):
    one_zero_matrix = np.zeros((9125, 19))
    for genre in movies_genres_dict:
        j = genre_to_num[genre]
        for Id in movies_genres_dict[genre]:
            i = Id_to_num[Id]
            one_zero_matrix[i, j] = 1
    return one_zero_matrix

'''
    采用minhash算法对特征矩阵(01)进行降维处理，从而得到相似度矩阵
    注意minhash采用jarcard方法计算相似度
'''
def minhash(one_zero_matrix):
    # 转置：19 * 9125
    one_zero_matrix = one_zero_matrix.T
    # h1(x) = (x+1)mod19, h2(x) = (2x+1)mod19, h3(x) = (3x+1)mod19, h4(x) = (4x+1)mod19, h5(x) = (5x+1)mod19
    # hash_matrix[i, j]:hi+1的第j列的hash值
    hash_matrix = np.zeros((5, 19))
    for i in range(len(hash_matrix)):
        for j in range(len(hash_matrix[i])):
            if i == 0:
                hash_matrix[i, j] = (j + 1) % 19
            if i == 1:
                hash_matrix[i, j] = (2 * j + 1) % 19
            if i == 2:
                hash_matrix[i, j] = (3 * j + 1) % 19
            if i == 3:
                hash_matrix[i, j] = (4 * j + 1) % 19
            if i == 4:
                hash_matrix[i, j] = (5 * j + 1) % 19
    # 签名矩阵
    sign_matrix = np.full((5, 9125), inf)
    for i in range(len(one_zero_matrix)):
        for j in range(len(one_zero_matrix[i])):
            if(one_zero_matrix[i][j] == 1):
                if(hash_matrix[0, i] < sign_matrix[0, j]):
                    sign_matrix[0, j] = hash_matrix[0, i]
                if (hash_matrix[1, i] < sign_matrix[1, j]):
                    sign_matrix[1, j] = hash_matrix[1, i]
                if (hash_matrix[2, i] < sign_matrix[2, j]):
                    sign_matrix[2, j] = hash_matrix[2, i]
                if (hash_matrix[3, i] < sign_matrix[3, j]):
                    sign_matrix[3, j] = hash_matrix[3, i]
                if (hash_matrix[4, i] < sign_matrix[4, j]):
                    sign_matrix[4, j] = hash_matrix[4, i]
    sign_matrix = sign_matrix.T
    similarity_matrix = np.zeros((9125, 9125))
    for i in range(9125):
        similarity_matrix[i, i] = 1
        for j in range(i, 9125):
            s1 = set(sign_matrix[i])
            s2 = set(sign_matrix[j])
            similarity_matrix[i, j] = float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
            similarity_matrix[j, i] = similarity_matrix[i, j]
    return similarity_matrix
'''
    根据指定的userId,获取已打分的movieId和rating
    根据相似度矩阵获取预测电影和已打分的电影的相似度
    如果当前预测电影与某已打分的电影的相似度大于0，加入计算集合
    将计算集合中的电影根据公式对当前预测的电影进行打分

'''
def get_score(userId, predict_movieId, userIds, similarity_matrix, Id_to_num):
    # 计算集合
    compute_Ids = {}
    for movieId in userIds[userId]: #遍历当前所有已打分的电影Id
        if similarity_matrix[Id_to_num[movieId], Id_to_num[predict_movieId]] > 0:
            compute_Ids[movieId] = userIds[userId][movieId]
        else:
            similarity_matrix[Id_to_num[movieId], Id_to_num[predict_movieId]] = 0
    # 对当前预测电影进行打分
    sim_sum = 0
    score_sim = 0
    sum = 0
    # 如果没有与预测电影相似度大于零的电影
    if len(compute_Ids) == 0:
        for movieId in userIds[userId]:
            sum += userIds[userId][movieId]
        score = sum / len(userIds[userId])
    # 如果有与预测电影相似度大于零的电影
    else:
        for movieId in compute_Ids:
            sim = similarity_matrix[Id_to_num[movieId], Id_to_num[predict_movieId]]
            sim_sum += sim
            score_sim += compute_Ids[movieId] * sim
        score = score_sim / sim_sum
    return score

'''
    推荐评测评分排名前k的电影
'''
def recommend(userId, k, res):
    testSet = pd.read_csv('test_set.csv')
    testUserIds = testSet['userId']
    testMovieIds = testSet['movieId']
    recommend_dict = {}
    recommend_list = [0]*10
    j = 0
    for i in range(len(testUserIds)):
        if(testUserIds[i] == userId):
            recommend_dict[testMovieIds[i]] = res[i]
            recommend_list[j] = recommend_dict
            recommend_dict = {}
            j += 1
    # 按score进行排序
    l = j
    while l > 0:
        for i in range(l - 1):
            for key in recommend_list[i]:
                a = recommend_list[i][key]
            for key in recommend_list[i + 1]:
                b = recommend_list[i + 1][key]
            if a > b:
                temp = recommend_list[i]
                recommend_list[i] = recommend_list[i + 1]
                recommend_list[i + 1] = temp
        l -= 1
    # 选出score值前k的电影的Id
    recommend_k = []
    if k < j:
        for i in range(k):
            for key in recommend_list[i]:
                recommend_k.append(key)
    else:
        for i in range(j):
            for key in recommend_list[i]:
                recommend_k.append(key)
    return recommend_k


if __name__ == '__main__':
    # 加载movie.csv的数据
    movies_genres_dict, genre_to_num, Id_to_num, movies_genres = loadDataSet()
    # 得到tf_idf矩阵(9125,19)
    tfidf_matrix = get_tfidf_matrix(movies_genres_dict,genre_to_num, Id_to_num, movies_genres)
    # 得到01矩阵
    one_zero_matrix = get_01_matrix(movies_genres_dict,genre_to_num, Id_to_num)
    #用minhash
    #similarity_matrix = minhash(one_zero_matrix)
    # 用余弦相似度的计算方法，得到电影之间的相似度矩阵
    similarity_matrix = get_similarity_matrix(tfidf_matrix)
    #one_zero_matrix = get01_matrix(similarity_matrix)
    # num->Id
    num_to_Id = {}
    i = 0
    for Id in Id_to_num:
        num_to_Id[Id] = i
        i += 1
    # 获取训练集的userIds列表,userIds[i]存储了userId=i的用户对电影的打分情况
    userIds = loadTrainSet()
    # 加载测试集进行测试
    testSet = pd.read_csv('test_set.csv')
    testUserIds = testSet['userId']
    testMovieIds = testSet['movieId']
    testRatings = testSet['rating']
    res = []
    S = []
    for i in range(len(testUserIds)):
        res.append(get_score(testUserIds[i], testMovieIds[i], userIds, similarity_matrix, Id_to_num))
        S.append((res[i] - testRatings[i]) * (res[i] - testRatings[i]))
    # 输出每一条预测评分，SSE
    print("%-8s"%"userId", "%-8s"%"movieId", "%-8s"%"正确评分", "%-8s"%"预测评分", "%-8s"%"误差平方")
    for i in range(len(testUserIds)):
        print("%-8d" % testUserIds[i], "%-8d" % testMovieIds[i], "%-10f" % testRatings[i], "%-10f" % res[i], "%-10f" % S[i])
    SSE = 0
    for i in range(len(S)):
        SSE += S[i]
    print("SEE:",SSE)

    #进行电影推荐
    userId,k = map(int, input("输入userID和推荐的电影个数k:").split())
    recommend_k = recommend(userId, k, res)
    print(recommend_k)