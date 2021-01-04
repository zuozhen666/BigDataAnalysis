# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:39:36 2020

@author: brave
"""

import threading

def reduce(readpath1, readpath2, readpath3, writepath):
    
    tmp_dict = {}
    
    fo = open(writepath, "w")
    
    with open(readpath1) as file:
        for line in file:
            tmp_word = line.split(',')
            word = tmp_word[0]
            num = tmp_word[1]
            num = num[0:-1]
            if word not in tmp_dict.keys():
                tmp_dict[word] = int(num)
            else:
                tmp_dict[word] += int(num) 
                
    with open(readpath2) as file:
        for line in file:
            tmp_word = line.split(',')
            word = tmp_word[0]
            num = tmp_word[1]
            num = num[0:-1]
            if word not in tmp_dict.keys():
                tmp_dict[word] = int(num)
            else:
                tmp_dict[word] += int(num) 
                
    with open(readpath3) as file:
        for line in file:
            tmp_word = line.split(',')
            word = tmp_word[0]
            num = tmp_word[1]
            num = num[0:-1]
            if word not in tmp_dict.keys():
                tmp_dict[word] = int(num)
            else:
                tmp_dict[word] += int(num) 
    
    for key in tmp_dict:
        fo.write(key+","+str(tmp_dict[key])+"\n")
    
   
if __name__ == '__main__':
    t1 = threading.Thread(target = reduce, args=("map_ans\spurce01_ans","map_ans\spurce02_ans","map_ans\spurce03_ans","reduce_ans\source123"))
    t2 = threading.Thread(target = reduce, args=("map_ans\spurce04_ans","map_ans\spurce05_ans","map_ans\spurce06_ans","reduce_ans\source456"))
    t3 = threading.Thread(target = reduce, args=("map_ans\spurce07_ans","map_ans\spurce08_ans","map_ans\spurce09_ans","reduce_ans\source789"))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    reduce("reduce_ans\source123","reduce_ans\source456","reduce_ans\source789","final_ans")
    