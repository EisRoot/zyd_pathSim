import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
from build_graph import init_graph,read_node_file,get_node_type
matplotlib.rc('font', family='Times New Roman')
matplotlib.rcParams.update({'font.size': 15})

nodes=read_node_file("zyd_network/node/node_gene.csv")
graph=init_graph()
mydict=[]
for node in nodes:
    count_num=0
    for neighber in graph.neighbors(node):
        count_num+=1
    mydict.append(count_num)

# 随机生成（10000,）服从正态分布的数据
plt.hist(mydict, bins=25, normed=0, facecolor="lightblue", edgecolor="black",range=(0,160))

# 显示横轴标签
plt.xlabel("Degree of Gene Node")
# 显示纵轴标签
plt.ylabel("Total Number of Gene Node")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('degree_hist.png', dpi=1200)
# 显示图标题
plt.show()

