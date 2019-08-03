# -*- coding: utf-8 -*-
from zyd_pathSimV3 import zyd_pathSim_algo
import pandas as pd
import datetime
import math
import random
import multiprocessing
import sys

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
    zps=zyd_pathSim_algo()
    count = 0
    lens = len(gene_nodes)
    final_len = lens
    score_list=[]
    for gene2 in gene_nodes:
        count += 1
        if count % 30 == 0:
            time = datetime.datetime.now().timestamp() - now_time
            array_time = math.floor(time / (count))
            left =array_time * (final_len - count) / (3600)
            print("the estimated time is:"+str(left))
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

gene1="G:HGNC:6932"

max_length=4
if len(sys.argv)==1:
    gene1="G:HGNC:6932"
else:
    gene1="G:HGNC:"+str(sys.argv[0])
   
print("the gene is: "+gene1)

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
final_score_list =[]
for y in pool.imap_unordered(mutil_prcoessing,cut_list):
    final_score_list=final_score_list+y
score_pd=pd.DataFrame(final_score_list)
score_pd.to_csv("final_score.csv")
f = open('score_list.txt', 'w')
f.write(str(final_score_list))
f.close()
