# -*- coding: utf-8 -*-
from zyd_pathSimV3 import zyd_pathSim_algo
import pandas as pd
import datetime
import math
import random

def read_node_file(path):
    nodes = []
    with open(path, "r",encoding='UTF-8-sig') as fp:
        lines = fp.readlines()
        for line in lines:
            line = line[:-1]
            nodes.append(line)
    return nodes

gene_node=read_node_file("zyd_network/node/node_gene.csv")
zps=zyd_pathSim_algo()
gene1="G:HGNC:6932"
score_list=[]
max_length=4
now_time = datetime.datetime.now().timestamp()
count=0
len=len(gene_node)
final_len=len
kk=10
round=0
for gene2 in gene_node:
    kk-=1
    count+=1
    if count%10==0:
        time = datetime.datetime.now().timestamp() - now_time
        array_time = math.floor(time / (count))
        left = math.floor(array_time * (final_len - count) / (3600))
        print(left)
    if gene1==gene2:
        continue
    score=zps.start(gene1,gene2,max_length)
    if score.__len__() > 0:
        print(score)
    score_list=score_list+score

    if kk ==0:
        try:
            score_pd = pd.DataFrame(score_list)
            score_pd.to_csv("lab_result/final_score.csv",mode='w')
            f = open('lab_result/score_list.txt', 'w')
            f.write(str(score_list))
            f.close()
            kk=1000
            round+=1
        except PermissionError:
            print('error')

score_pd=pd.DataFrame(score_list)

score_pd.to_csv("final_score.csv")
f = open('score_list.txt', 'w')
f.write(str(score_list))
f.close()