from build_graph import init_graph,read_node_file,get_node_type
import pandas as pd
import math
nodes=read_node_file("zyd_network/node/node_gene.csv")
graph=init_graph()
mydict=[]
for node in nodes:
    count_num=0
    for neighber in graph.neighbors(node):
        count_num+=1
    mydict.append(count_num)
# mydict={}
# for node in nodes:
#     count_num=0
#     for neighber in graph.neighbors(node):
#         count_num+=1
#     if mydict.__contains__(count_num):
#         mydict[count_num]+=1
#     else:
#         mydict[count_num]=1
# edict={}
# for k,v in mydict.items():
#     during=math.floor(k/10)
#     if edict.__contains__(during):
#         edict[during]+=v
#     else:
#         edict[during]=v
mylist=[]
for k,v in mydict.items():
    mylist.append({
        "range":k,
        "number of gene":v
    })
mydict_pd=pd.DataFrame(mylist)
mydict_pd.to_csv("lab_result/estimated_gene_degree.csv")
mydict2={}
# for node in nodes:
#     count=set()
#     for neighber in graph.neighbors(node):
#         type=get_node_type(neighber)
#         count.add(type)
#     type_num=count.__len__()
#     if mydict2.__contains__(type_num):
#         mydict2[type_num]+=1
#     else:
#         mydict2[type_num]=1
# mylist2=[]
# for k,v in mydict2.items():
#     mylist2.append({
#         "number of type":k,
#         "number of gene":v
#     })
# mydict2_pd=pd.DataFrame(mylist2)
# mydict2_pd.to_csv("lab_result/estimated_gene_neighbor_type.csv")
