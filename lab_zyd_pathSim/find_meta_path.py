from build_graph import init_graph
import pandas as pd
from DGAS_FMPV2 import DGAS_core
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

nodes=read_node_file("4DegreeGene_HGNCID.csv")
print(nodes)
max_length=4
algo=DGAS_core(init_graph())
for i in nodes:
    for j in nodes:
        if not i ==j:
            re=algo.start(i,j,max_length)
            print(re)

