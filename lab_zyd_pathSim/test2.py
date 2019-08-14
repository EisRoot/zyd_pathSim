# -*- coding: utf-8 -*-
from DGAS_LimitV2 import DGAS_limit_core
from DGAS_FMPV2 import FMP_algo
from build_graph import init_graph
import pandas as pd
import datetime
import math
import multiprocessing
import sys
import os
import copy

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
    graph=dict_parameter['graph']
    now_time = datetime.datetime.now().timestamp()
    algo=DGAS_limit_core(limit,graph)
    count = 0
    lens = len(gene_nodes)
    final_len = lens
    score_list=[]
    for gene2 in gene_nodes:
        count += 1
        if count % 100 == 0:
            time = datetime.datetime.now().timestamp() - now_time
            array_time = time / (count)
            left =array_time * (final_len - count) / (60)
            print("the estimated time of processing:"+str(os.getpid())+" is:"+str(left)[0:5]+" min")
        if gene1 == gene2:
            continue
        score = algo.start(gene1, gene2, max_length)
        # if score.__len__() > 0:
        #     print(score)
        score_list = score_list + score
    print(" ############Processing:"+str(os.getpid())+" is done ###################")
    return score_list
def create_multi_task_data(gene_nodes,cores,max_length,gene1,limit,num_of_processings):
    list_len = len(gene_nodes)
    cut_count = math.floor(list_len / cores)
    cut_list = []
    print("Split data("+str(list_len)+") into "+str(cores)+" set:")
    graph=init_graph()

    for i in range(0, cores-1):
        print(str(i * cut_count)+"--"+str(i * cut_count + cut_count - 1))
        piece = gene_nodes[i * cut_count:i * cut_count + cut_count - 1]
        cut_list.append({
            'gene1': gene1,
            'gene_nodes': piece,
            'max_length': max_length,
            'limit':limit,
            'graph':graph
        })
    i = cores-1
    final_piece = gene_nodes[i * cut_count:list_len - 1]
    print(str(i * cut_count)+"--"+str(list_len-1))
    cut_list.append({
        'gene1': gene1,
        'gene_nodes': final_piece,
        'max_length': max_length,
        'limit':limit,
        'graph': graph
    })
    return cut_list
def get_parameter():
    if len(sys.argv) < 3:
        print(" Use G:HGNC:6932 and G:HGNC:9236 as input")
        #exit()
        return None,None,None
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
def combine_whole(l):
    lenth=len(l)
    list=[]
    if lenth==0:
        return []
    else:
        for i in range(1,lenth+1):
            list=list+combine(l,i)
    return list

def combine(l, n):
    answers = []
    one = [0] * n

    def next_c(li=0, ni=0):
        if ni == n:
            answers.append(copy.copy(one))
            return
        for lj in range(li, len(l)):
            one[ni] = l[lj]
            next_c(lj + 1, ni + 1)

    next_c()
    return answers
def read_rank(pd,meta_path_candidate,gene1,gene2):
    rank_list=[]
    for meta_path in meta_path_candidate:
        pd2 = pd[pd['mPath'] == meta_path]
        pd2=pd2.sort_values('score',ascending=False)
        pd2['score_rank']=pd2['score'].rank(method='dense',ascending=False)
        max_rank=pd2['score_rank'].max()
        pd3=pd2[
            (pd2['gene1']==gene1)&
            (pd2['gene2']==gene2)
            ]
        meta_path_rank=pd3.iloc[0]['score_rank']

        rank_list.append({
            "meta_path_rank":meta_path_rank,
            "meta_path":meta_path,
            "gene1":gene1,
            "gene2":gene2,
            "total_rank":max_rank
        })

    return rank_list


if __name__ == '__main__':
    time1=datetime.datetime.now().timestamp()
    g1,g2,fileName=get_parameter()
    if g1==None:
        g1='G:HGNC:6932'
        g2='G:HGNC:9236'
        fileName="6932_9236"
    max_length=4
    zyd=FMP_algo(init_graph())
    print("Begin to found meta path between " + g1 + " and " + g2)
    meta_path_candidate=[]
    re=zyd.start(g1,g2,max_length)
    for r in re:
        meta_path_candidate.append(r["meta_path_name"])
    print(str(len(meta_path_candidate))+" meta paths were found")
    meta_path_limit=[]
    meta_path_chosen=[]
    for candidate in meta_path_candidate:
        meta_path=cut_meta_path(candidate)
        if not meta_path == None:
            meta_path_chosen.append(candidate)
            print(candidate+"---"+meta_path)
            meta_path_limit.append(meta_path)


    cores = multiprocessing.cpu_count()-2
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=cores)
    print("The number of cpu cores is "+str(cores))
    gene_nodes=read_node_file("zyd_network/node/node_gene.csv")


    cores_for_gene1=math.floor(cores/2)
    cores_for_gene2=cores-cores_for_gene1
    multi_prcoessing_data1=create_multi_task_data(gene_nodes,cores_for_gene1,max_length,g1,meta_path_limit,cores)
    multi_prcoessing_data2=create_multi_task_data(gene_nodes,cores_for_gene2,max_length,g2,meta_path_limit,cores)
    multi_prcoessing_data=multi_prcoessing_data1+multi_prcoessing_data2

    final_score_list =[]
    for y in pool.imap_unordered(mutil_prcoessing,multi_prcoessing_data):
        final_score_list=final_score_list+y
    score_pd=pd.DataFrame(final_score_list)
    score_pd.to_csv("lab_result/final_score_"+fileName+".csv")
    print(score_pd)

    # score_pd=pd.read_csv("final_score_6932_9236.csv")
    # meta_path_candidate=['GTG','GDpDpDG']
    meta_path_candidate=combine_whole(meta_path_candidate)
    meta_path_candidate2=[]

    for i in meta_path_candidate:
        meta_path_candidate2.append(str(i))
    print(meta_path_candidate2)

    rank_list=read_rank(score_pd,meta_path_candidate2,g1,g2)
    rank_pd=pd.DataFrame(rank_list)
    rank_pd = rank_pd.sort_values('meta_path_rank')
    first_one=rank_pd.iloc[0]
    print("The result is:")
    print("Meta path:"+first_one['meta_path']+", rank is "+str(int(first_one['meta_path_rank']))+" and total rank is "+str(int(first_one['total_rank'])))
    time2=datetime.datetime.now().timestamp()
    print("Cost time:")
    cost_time=(time2-time1)/60
    print(str(cost_time)[0:4])
    rank_pd.to_csv("lab_result/final_result_"+fileName+".csv")






