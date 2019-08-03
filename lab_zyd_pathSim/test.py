# -*- coding: utf-8 -*-
from zyd_pathSimV3 import zyd_pathSim_algo
import pandas as pd
import datetime
import math
import random
import multiprocessing

def read_node_file(path):
    nodes = []
    with open(path, "r",encoding='UTF-8-sig') as fp:
        lines = fp.readlines()
        for line in lines:
            line = line[:-1]
            nodes.append(line)
    return nodes
def mutil_prcoessing(dict_parameter):
    gene1=dict_parameter['gene1']
    gene_nodes=dict_parameter['gene_nodes']
    max_length=dict_parameter['max_length']
    now_time = datetime.datetime.now().timestamp()
    count = 0
    lens = len(gene_node)
    final_len = lens

    for gene2 in gene_nodes:
        kk -= 1
        count += 1
        if count % 10 == 0:
            time = datetime.datetime.now().timestamp() - now_time
            array_time = math.floor(time / (count))
            left = math.floor(array_time * (final_len - count) / (3600))
            print(left)
        if gene1 == gene2:
            continue
        score = zps.start(gene1, gene2, max_length)
        if score.__len__() > 0:
            print(score)
        score_list = score_list + score

    try:
        score_pd = pd.DataFrame(score_list)
        score_pd.to_csv("lab_result/final_score_step.csv", mode='a')
        f = open('lab_result/score_list_step.txt', 'a')
        f.write(str(score_list))
        f.close()
    except PermissionError:
        print('error')
    return score_list

cores = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cores)
print(cores)


gene_node=read_node_file("zyd_network/node/node_gene.csv")
zps=zyd_pathSim_algo()
gene1="G:HGNC:6932"
score_list=[]
max_length=4

list_len=len(gene_node)
cut_count=math.floor(list_len/cores)
each=math.floor(list_len/cut_count)
cut_list=[]
for i in range(0,cut_count-2):
    piece=gene_node[i*each:i*each+each-1]
    cut_list.append({
        'gene1':gene1,
        'gene_nodes':piece,
        'max_length':max_length
    })
i=cut_count-1
final_piece=gene_node[i*each:list_len-1]
cut_list.append({
        'gene1':gene1,
        'gene_nodes':final_piece,
        'max_length':max_length
    })
score_list =[]
for y in pool.imap_unordered(mutil_prcoessing,cut_list):
    score_list=score_list+y
score_pd=pd.DataFrame(score_list)
score_pd.to_csv("final_score.csv")
f = open('score_list.txt', 'w')
f.write(str(score_list))
f.close()
