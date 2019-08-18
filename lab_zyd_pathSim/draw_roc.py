# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 16:13:04 2017
@author: lizhen
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import pandas as pd
from sklearn.metrics import roc_curve, auc ,roc_auc_score  ###计算roc和auc
matplotlib.rc('font', family='Times New Roman')
matplotlib.rcParams.update({'font.size': 30})
data=pd.read_csv("lab_result816/lab_result_percent_1200.csv",dtype=str)
data2=pd.read_csv("lab_result816/lab_result_Wang_Resnik_Lin_1200.csv",)
y_score_Wang_CC=data2["Wang_CC"]
y_score_Wang_BP=data2["Wang_BP"]
y_score_Wang_MF=data2["Wang_MF"]

y_score_Resnik_CC=data2["Resnik_CC"]
y_score_Resnik_BP=data2["Resnik_BP"]
y_score_Resnik_MF=data2["Resnik_MF"]

y_score_Lin_CC=data2["Lin_CC"]
y_score_Lin_BP=data2["Lin_BP"]
y_score_Lin_MF=data2["Lin_MF"]
# y_score_Wang_MF=data2["Wang_MF"]
#
# y_score_Wang_MF=data2["Wang_MF"]

y_test2=data2["Label"].astype(dtype=int)

y_score=data["rank_percent"].astype(dtype=float)
y_test=data["label"].astype(dtype=int)

# Compute ROC curve and ROC AUC for each class
fpr, tpr, threshold = roc_curve(y_test, y_score)  ###计算真正率和假正率
fpr_Wang_CC, tpr_Wang_CC, threshold_Wang_CC = roc_curve(y_test2, y_score_Wang_CC)  ###计算真正率和假正率
fpr_Wang_BP, tpr_Wang_BP, threshold_Wang_BP = roc_curve(y_test2, y_score_Wang_BP)  ###计算真正率和假正率
fpr_Wang_MF, tpr_Wang_MF, threshold_Wang_MF = roc_curve(y_test2, y_score_Wang_MF)  ###计算真正率和假正率

fpr_Resnik_CC, tpr_Resnik_CC, threshold_Resnik_CC = roc_curve(y_test2, y_score_Resnik_CC)  ###计算真正率和假正率
fpr_Resnik_BP, tpr_Resnik_BP, threshold_Resnik_BP = roc_curve(y_test2, y_score_Resnik_BP)  ###计算真正率和假正率
fpr_Resnik_MF, tpr_Resnik_MF, threshold_Resnik_MF = roc_curve(y_test2, y_score_Resnik_MF)  ###计算真正率和假正率

fpr_Lin_CC, tpr_Lin_CC, threshold_Lin_CC = roc_curve(y_test2, y_score_Lin_CC)  ###计算真正率和假正率
fpr_Lin_BP, tpr_Lin_BP, threshold_Lin_BP = roc_curve(y_test2, y_score_Lin_BP)  ###计算真正率和假正率
fpr_Lin_MF, tpr_Lin_MF, threshold_Lin_MF = roc_curve(y_test2, y_score_Lin_MF)  ###计算真正率和假正率

# auc_score= roc_auc_score(y_test, y_score)  ###计算真正率和假正率
# auc_score_Wang_CC = roc_auc_score(y_test2, y_score_Wang_CC)  ###计算真正率和假正率
# auc_score_Wang_BP = roc_auc_score(y_test2, y_score_Wang_BP)  ###计算真正率和假正率
# auc_score_Wang_MF = roc_auc_score(y_test2, y_score_Wang_MF)  ###计算真正率和假正率
#
# auc_score_Resnik_CC= roc_auc_score(y_test2, y_score_Resnik_CC)  ###计算真正率和假正率
# auc_score_Resnik_BP = roc_auc_score(y_test2, y_score_Resnik_BP)  ###计算真正率和假正率
# auc_score_Resnik_MF = roc_auc_score(y_test2, y_score_Resnik_MF)  ###计算真正率和假正率
#
# auc_score_Lin_CC= roc_auc_score(y_test2, y_score_Lin_CC)  ###计算真正率和假正率
# auc_score_Lin_BP= roc_auc_score(y_test2, y_score_Lin_BP)  ###计算真正率和假正率
# auc_score_Lin_MF= roc_auc_score(y_test2, y_score_Lin_MF)  ###计算真正率和假正率
#
# print(auc_score)
roc_auc = auc(fpr, tpr)  ###计算auc的值
roc_auc_Wang_CC = auc(fpr_Wang_CC, tpr_Wang_CC)  ###计算auc的值
roc_auc_Wang_BP = auc(fpr_Wang_BP, tpr_Wang_BP)  ###计算auc的值
roc_auc_Wang_MF = auc(fpr_Wang_MF, tpr_Wang_MF)  ###计算auc的值

roc_auc_Resnik_CC = auc(fpr_Resnik_CC, tpr_Resnik_CC)  ###计算auc的值
roc_auc_Resnik_BP = auc(fpr_Resnik_BP, tpr_Resnik_BP)  ###计算auc的值
roc_auc_Resnik_MF = auc(fpr_Resnik_MF, tpr_Resnik_MF)  ###计算auc的值

roc_auc_Lin_CC = auc(fpr_Lin_CC, tpr_Lin_CC)  ###计算auc的值
roc_auc_Lin_BP = auc(fpr_Lin_BP, tpr_Lin_BP)  ###计算auc的值
roc_auc_Lin_MF = auc(fpr_Lin_MF, tpr_Lin_MF)  ###计算auc的值


lw = 4
plt.figure(figsize=(10,10))
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
#ytick.minor.pad      : 3.4    ## distance to the minor tick label in points

plt.plot(fpr, tpr,color='red',
         lw=lw, label='SCENARIO\n(AUC = %0.3f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
# plt.plot(fpr_Wang_CC, tpr_Wang_CC,color='darkblue',
#          lw=lw, label='Wang_CC\n(AUC = %0.3f)' % roc_auc_Wang_CC)
# plt.plot(fpr_Resnik_CC, tpr_Resnik_CC, color='darkblue',
#          lw=lw, label='Resnik_CC\n(AUC = %0.3f)' % roc_auc_Resnik_CC)
plt.plot(fpr_Lin_CC, tpr_Lin_CC, color='darkblue',
         lw=lw, label='Lin_CC\n(AUC = %0.3f)' % roc_auc_Lin_CC)

# plt.plot(fpr_Wang_BP, tpr_Wang_BP,
#          lw=lw, label='Wang_BP\n(AUC = %0.3f)' % roc_auc_Wang_BP,linestyle='dashdot',)
# plt.plot(fpr_Resnik_BP, tpr_Resnik_BP, linestyle='dashdot',
#          lw=lw, label='Resnik_BP\n(AUC = %0.3f)' % roc_auc_Resnik_BP)
plt.plot(fpr_Lin_BP, tpr_Lin_BP,linestyle='dashdot',
         lw=lw, label='Lin_BP\n(AUC = %0.3f)' % roc_auc_Lin_BP)

# plt.plot(fpr_Wang_MF, tpr_Wang_MF,
#          lw=lw, label='Wang_MF\n(AUC = %0.3f)' % roc_auc_Wang_MF,linestyle='dashed')
# plt.plot(fpr_Resnik_MF, tpr_Resnik_MF, linestyle='dashed',
#          lw=lw, label='Resnik_MF\n(AUC = %0.3f)' % roc_auc_Resnik_MF)
plt.plot(fpr_Lin_MF, tpr_Lin_MF, linestyle='dashed',
         lw=lw, label='Lin_MF\n(AUC = %0.3f)' % roc_auc_Lin_MF)
font2 = {'family': 'Times New Roman',
'weight' : 'normal',
'size'   : 42,
}
plt.rcParams['ytick.major.left'] = False
plt.rcParams['ytick.minor.pad'] = 100
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'
matplotlib.rcParams['mathtext.it'] = 'Times New Roman:italic'

plt.plot([0, 1], [0, 1], '--',color='lightgrey', lw=3, linestyle='--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.xticks([0,0.2,0.4,0.6,0.8,1.0],["0","0.2","0.4","0.6","0.8","1.0"],fontsize=35)
plt.yticks([0.2,0.4,0.6,0.8,1.0],fontsize=35)
# xrange=[0,0.2,0.4,0.6,0.8,1.0]
# lab=['sad','0.2','0.4','0.6','0.8','1.0']
# ax.set_yticks(xrange)
# ax.set_yticklabels(lab)
# ax.spines['bottom'].set_linewidth(3)###设置底部坐标轴的粗细
# ax.spines['left'].set_linewidth(3)####设置左边坐标轴的粗细
# ax.spines['right'].set_linewidth(3)###设置右边坐标轴的粗细
# ax.spines['top'].set_linewidth(3)####设置上部坐标轴的粗细

plt.xlabel('False Positive Rate',fontsize=42)
plt.ylabel('True Positive Rate',font2)
plt.legend(loc="lower right")
plt.tight_layout()

plt.savefig('S_Lin.pdf')
plt.show()