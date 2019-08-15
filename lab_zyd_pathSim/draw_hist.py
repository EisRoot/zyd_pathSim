import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
from build_graph import init_graph,read_node_file,get_node_type
matplotlib.rc('font', family='Times New Roman')
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'
matplotlib.rcParams['mathtext.it'] = 'Times New Roman'
plt.rcParams['figure.figsize'] = (8.8, 5.0) # 设置figure_size尺寸
matplotlib.rcParams['mathtext.fontset'] = 'custom'

plt.rcParams['ytick.direction'] = 'in'
range_pd=pd.read_csv("lab_result/estimated_gene_degree_range.csv")
range_pd=range_pd.sort_values("range")
x=range_pd["range"].to_list()[0:10]
y=range_pd["number of gene"].to_list()
y_over=y[11:-1]
print(y_over)
over_100_count=0
for i in y_over:
    over_100_count+=i
y=y[0:10]
y.append(over_100_count)
x2=[]
for i in x:
    if i ==0:
        x2.append("[0,10)")
        continue
    str2="["+str(i)+"0,"+str(i+1)+"0"+")"
    x2.append(str2)
x2.append("[100,+∞)")
len1=len(y)
print(x2)
print(y)
# nodes=read_node_file("zyd_network/node/node_gene.csv")
# graph=init_graph()
# mydict=[]
# for node in nodes:
#     count_num=0
#     for neighber in graph.neighbors(node):
#         count_num+=1
#     mydict.append(count_num)
#
# # 随机生成（10000,）服从正态分布的数据
# plt.hist(mydict, bins=25, normed=0, facecolor="lightblue", edgecolor="black",range=(0,160),)
fig,ax=plt.subplots()

plt.bar(range(len1), y, color = 'lightblue',width=0.75)
# 显示横轴标签
plt.xlabel("Range of Degrees")
plt.xticks(range(len1), x2,fontsize=12)
# 显示纵轴标签
plt.ylabel('Number of Gene Nodes ('+r'$\mathit{× 10^3}$'+')')
yts=range(0,8000,1000)
ylab=['0','1','2','3','4','5','6','7']
ax.set_yticks(yts)
ax.set_yticklabels(ylab)
plt.yticks(fontsize=18)
plt.xticks(fontsize=13)
plt.tight_layout()
plt.savefig('degree_hist.pdf')
# 显示图标题
plt.show()

