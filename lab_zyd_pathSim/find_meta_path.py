from build_graph import init_graph
import pandas as pd
from DGAS_FMPV2 import FMP_algo
import multiprocessing
import math
import datetime
import os
def read_node_file(path):
    nodes = []
    with open(path, "r",encoding='UTF-8-sig') as fp:
        lines = fp.readlines()
        for line in lines:
            line = line[:-1]
            nodes.append(line)
    return nodes
def get_node_type(node):
    """
    Get node type
    :param node:
    :return: type
    """
    type=node[0]
    return type


def create_gene_pair():
    nodes = read_node_file("4DegreeGene_HGNCID.csv")
    print(nodes)
    max_length = 4
    algo = FMP_algo(init_graph())
    pair_list = []
    c = 0
    match_list = []
    for i in nodes:
        match_list.append(i)
        nodes2 = list(set(nodes) - set(match_list))
        for j in nodes2:
            # if not i ==j and not pair_list.__contains__({
            #     "gene1": j,
            #     "gene2": i
            # }):
            if not i == j:
                pair_list.append({
                    "gene1": i,
                    "gene2": j
                })
                # re = algo.start(i, j, max_length)
                # print(re)
            else:
                c += 1
                print(c)
    print(len(pair_list))
    pair_pd = pd.DataFrame(pair_list)
    pair_pd.to_csv("lab_result/gene_pair.csv")

def mutil_prcoessing(dict_parameter):
    gene_pair=dict_parameter['gene_pair']
    max_length=dict_parameter['max_length']
    graph=dict_parameter['graph']
    now_time = datetime.datetime.now().timestamp()
    algo=FMP_algo(graph)
    count = 0
    lens = len(gene_pair)
    final_len = lens
    meta_list={}
    for pair in gene_pair:
        count += 1
        if count % 100 == 0:
            time = datetime.datetime.now().timestamp() - now_time
            array_time = time / (count)
            left =array_time * (final_len - count) / (60)
            print("the estimated time of processing:"+str(os.getpid())+" is:"+str(left)[0:5]+" min")
        gene1=pair[0]
        gene2=pair[1]
        re = algo.start(gene1, gene2, max_length)
        # if score.__len__() > 0:
        #     print(score)
        meta_list = count_meta_path(re,meta_list)
    print(" ############Processing:"+str(os.getpid())+" is done ###################")
    return meta_list
def count_meta_path(re,dict):
    for i in re:
        meta_path_name=i["meta_path_name"]
        if dict.__contains__(meta_path_name):
            dict[meta_path_name]['num_of_pair']+=1
            dict[meta_path_name]['ins']+=i['ins']
        else:
            dict[meta_path_name]={
                "num_of_pair":1,
                "ins":i['ins']
            }
    return dict
def create_multi_task_data(gene_pairs, cores, max_length,):
    list_len = len(gene_pairs)
    cut_count = math.floor(list_len / cores)
    cut_list = []
    print("Split data("+str(list_len)+") into "+str(cores)+" set:")
    graph=init_graph()

    for i in range(0, cores-1):
        print(str(i * cut_count)+"--"+str(i * cut_count + cut_count - 1))
        piece = gene_pairs[i * cut_count:i * cut_count + cut_count - 1]
        cut_list.append({
            'gene_pair': piece,
            'max_length': max_length,
            'graph':graph
        })
    i = cores-1
    final_piece = gene_pairs[i * cut_count:list_len - 1]
    print(str(i * cut_count)+"--"+str(list_len-1))
    cut_list.append({
        'gene_pair': final_piece,
        'max_length': max_length,
        'graph': graph
    })
    return cut_list
if __name__ == '__main__':

    gene_pair=pd.read_csv("lab_result/gene_pair.csv",index_col=0)
    max_length=4
    gene_pair=gene_pair.to_records(index=None)
    cores = multiprocessing.cpu_count() - 2
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=cores)
    print("The number of cpu cores is " + str(cores))
    multiprocessing_data=create_multi_task_data(gene_pair,cores,max_length)
    total={}
    for y in pool.imap_unordered(mutil_prcoessing,multiprocessing_data):
        for k,v in y.items():
            if total.__contains__(k):
                total[k]['num_of_pair']+=v['num_of_pair']
                total[k]['ins']+=v['ins']
            else:
                total[k]={
                    'num_of_pair':v['num_of_pair'],
                    'ins':v['ins']
                }
    total_list=[]
    for k,v in total.items():
        total_list.append({
            "meta_path_name":k,
            "num_of_pair":v['num_of_pair'],
            "ins":v['ins']
        })
    total_pd=pd.DataFrame(total_list)
    total_pd.to_csv("lab_result/meta_path_total.csv")