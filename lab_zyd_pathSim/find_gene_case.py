from build_graph import init_graph
import pandas as pd
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

nodes=read_node_file("zyd_network/node/node_gene.csv")
graph=init_graph()
list=[]
for node in nodes:
    count=set()
    count_num=0
    for neighber in graph.neighbors(node):
        type=get_node_type(neighber)
        count.add(type)
        count_num+=1
    if count_num>100:
        list.append(node)
print(len(list))

data=pd.DataFrame(list)
data.to_csv("4DegreeGene_HGNCID.csv",index=None)