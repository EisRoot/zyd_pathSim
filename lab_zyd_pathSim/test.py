# -*- coding: utf-8 -*-
from DGAS_Limit import DGAS_limit_core
from DGAS_FMP import FMP_algo
import pandas as pd
import datetime
import math
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
    limit=dict_parameter['limit']
    now_time = datetime.datetime.now().timestamp()
    algo=DGAS_limit_core(limit)
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
            print("the estimated time is:"+str(left)[0:5]+" min")
        if gene1 == gene2:
            continue
        score = algo.start(gene1, gene2, max_length)
        if score.__len__() > 0:
            print(score)
        score_list = score_list + score

    try:
        score_pd = pd.DataFrame(score_list)
        score_pd.to_csv("lab_result/final_score_step_"+gene1+".csv", mode='a')
        f = open('lab_result/score_list_step_'+gene1+'.txt', 'a')
        f.write(str(score_list))
        f.close()
    except PermissionError:
        print('error')
    return score_list
def create_multi_task_data(gene_nodes,cores,max_length,gene1,limit):
    list_len = len(gene_nodes)
    cut_count = math.floor(list_len / cores)
    cut_list = []
    print("Split data("+str(list_len)+") into "+str(cores)+" set:")

    for i in range(0, cores-1):
        print(str(i * cut_count)+"--"+str(i * cut_count + cut_count - 1))
        piece = gene_nodes[i * cut_count:i * cut_count + cut_count - 1]
        cut_list.append({
            'gene1': gene1,
            'gene_nodes': piece,
            'max_length': max_length,
            'limit':limit
        })
    i = cores-1
    final_piece = gene_nodes[i * cut_count:list_len - 1]
    print(str(i * cut_count)+"--"+str(list_len-1))
    cut_list.append({
        'gene1': gene1,
        'gene_nodes': final_piece,
        'max_length': max_length,
        'limit':limit
    })
    return cut_list
def get_parameter():
    if len(sys.argv) < 3:
        print("please input two gene id!")
        exit()
        # gene1="G:HGNC:6932"
        # fileName="HGNC6932"
    else:
        gene1 = "G:HGNC:" + str(sys.argv[1])
        gene2 = "G:HGNC:" + str(sys.argv[2])
        fileName = "HGNC" + str(sys.argv[1]) + "_HGNC" + str(sys.argv[2])

        return gene1, gene2, fileName
def cut_meta_path(mPath):
    """
    Cut meta_path string into two part.
    One is a meta_path from the started gene node to the center node.
    Another is from the ended gene node.
    For example, input mPath like 'GDPdG' and the output are 'GDP' and 'Gdp"
    :param mPath:
    :return: head2center,tail2center
    """
    le=len(mPath)
    if le%2==0:
        print("This meta path:"+mPath+" is not even")
        return None
    else:
        #'GDG' 'GDPG
        center = math.floor(le / 2)
        head2center=mPath[0:center+1]
        tail2center=mPath[center:le][::-1]
        if head2center==tail2center:
            return head2center
        else:
            print("This meta path:" + mPath + " is not symmetrical")
            return None


if __name__ == '__main__':
    #g1,g2,fileName=get_parameter()
    g1='G:HGNC:6932'
    g2='G:HGNC:9236'
    fileName="6932_9236"
    max_length=4
    zyd=FMP_algo()
    print("Begin to found meta path between " + g1 + " and " + g2)
    meta_path_candidate=zyd.start(g1,g2,max_length*2-1)
    print(str(len(meta_path_candidate))+" meta paths were found")
    meta_path_limit=[]
    for candidate in meta_path_candidate:
        meta_path=cut_meta_path(candidate)
        if not meta_path == None:
            print(candidate+"---"+meta_path)
            meta_path_limit.append(meta_path)


    cores = multiprocessing.cpu_count()-2
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=cores)
    print("The number of cpu cores is "+str(cores))
    gene_nodes=read_node_file("zyd_network/node/node_gene.csv")

    cores_for_gene1=math.floor(cores/2)
    cores_for_gene2=cores-cores_for_gene1
    multi_prcoessing_data1=create_multi_task_data(gene_nodes,cores_for_gene1,max_length,g1,meta_path_limit)
    multi_prcoessing_data2=create_multi_task_data(gene_nodes,cores_for_gene2,max_length,g1,meta_path_limit)
    multi_prcoessing_data=multi_prcoessing_data1+multi_prcoessing_data2

    final_score_list =[]
    for y in pool.imap_unordered(mutil_prcoessing,multi_prcoessing_data):
        final_score_list=final_score_list+y
    score_pd=pd.DataFrame(final_score_list)
    score_pd.to_csv("final_score_"+fileName+".csv")
    f = open('score_list_'+fileName+'.txt', 'w')
    f.write(str(final_score_list))
    f.close()


