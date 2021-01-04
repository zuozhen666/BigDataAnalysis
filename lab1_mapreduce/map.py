# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:21:28 2020

@author: brave
"""

import threading

def map(readpath, writepath):
    
    fp = open(readpath, "a")
    fp.write("\n")
    fp.close()
    
    fo = open(writepath, "w")

    with open(readpath) as file:
        for line in file:
            linelist = line.split(', ')
            length = len(linelist)
            for word in linelist:
                if length == 1:
                    word = word[0:-1]
                fo.write(word+",1\n")
                length = length - 1

    fo.close()
        
    
if __name__ == '__main__':
    t1 = threading.Thread(target = map, args=("data\source01", "map_ans\spurce01_ans"))
    t2 = threading.Thread(target = map, args=("data\source02", "map_ans\spurce02_ans"))
    t3 = threading.Thread(target = map, args=("data\source03", "map_ans\spurce03_ans"))
    t4 = threading.Thread(target = map, args=("data\source04", "map_ans\spurce04_ans"))
    t5 = threading.Thread(target = map, args=("data\source05", "map_ans\spurce05_ans"))
    t6 = threading.Thread(target = map, args=("data\source06", "map_ans\spurce06_ans"))
    t7 = threading.Thread(target = map, args=("data\source07", "map_ans\spurce07_ans"))
    t8 = threading.Thread(target = map, args=("data\source08", "map_ans\spurce08_ans"))
    t9 = threading.Thread(target = map, args=("data\source09", "map_ans\spurce09_ans"))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()