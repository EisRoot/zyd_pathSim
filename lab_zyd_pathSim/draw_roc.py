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
matplotlib.rcParams.update({'font.size': 25})
data=pd.read_csv("lab_result816/lab_result_percent_300.csv",dtype=str)
data2=pd.read_csv("lab_result816/lab_result_Wang_Resnik_Lin_300.csv",index_col=0)
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

fig,ax=plt.subplots()
lw = 4
plt.figure(figsize=(10, 10))
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='SCENARIO (AUC = %0.3f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
plt.plot(fpr_Wang_CC, tpr_Wang_CC, color='red',linestyle='dashed',
         lw=lw, label='Wang_CC (AUC = %0.3f)' % roc_auc_Wang_CC)
plt.plot(fpr_Resnik_CC, tpr_Resnik_CC, color='green',linestyle='dashdot',
         lw=lw, label='Resnik_CC (AUC = %0.3f)' % roc_auc_Resnik_CC)
plt.plot(fpr_Lin_CC, tpr_Lin_CC, color='blue',linestyle='dotted',
         lw=lw, label='Lin_CC (AUC = %0.3f)' % roc_auc_Lin_CC)

plt.plot(fpr_Wang_BP, tpr_Wang_BP, color='red',linestyle='dashed',
         lw=lw, label='Wang_BP (AUC = %0.3f)' % roc_auc_Wang_BP)
plt.plot(fpr_Resnik_BP, tpr_Resnik_BP, color='green',linestyle='dashdot',
         lw=lw, label='Resnik_BP (AUC = %0.3f)' % roc_auc_Resnik_BP)
plt.plot(fpr_Lin_BP, tpr_Lin_BP, color='blue',linestyle='dotted',
         lw=lw, label='Lin_BP (AUC = %0.3f)' % roc_auc_Lin_BP)

plt.plot(fpr_Wang_MF, tpr_Wang_MF, color='red',linestyle='dashed',
         lw=lw, label='Wang_MF (AUC = %0.3f)' % roc_auc_Wang_MF)
# plt.plot(fpr_Resnik_MF, tpr_Resnik_MF, color='green',linestyle='dashdot',
#          lw=lw, label=r'$\mathit{Resnik\_MF(AUC=%0.3f)}$' % roc_auc_Resnik_MF)
plt.plot(fpr_Resnik_MF, tpr_Resnik_MF, color='green',linestyle='dashdot',
         lw=lw, label='Resnik_MF (AUC = %0.3f)' % roc_auc_Resnik_MF)
plt.plot(fpr_Lin_MF, tpr_Lin_MF, color='blue',linestyle='dotted',
         lw=lw, label='Lin_MF (AUC = %0.3f)' % roc_auc_Lin_MF)
font2 = {'family': 'Times New Roman',
'weight' : 'normal',
'size'   : 35,
}

matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'
matplotlib.rcParams['mathtext.it'] = 'Times New Roman:italic'

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xticks(fontsize=28)
plt.yticks(fontsize=28)
# xrange=[0,0.2,0.4,0.6,0.8,1.0]
# lab=['sad','0.2','0.4','0.6','0.8','1.0']
# ax.set_yticks(xrange)
# ax.set_yticklabels(lab)
plt.xlabel('False Positive Rate',font2)
plt.ylabel('True Positive Rate',font2)
plt.legend(loc="lower right")
plt.tight_layout()
#plt.savefig('test3.png',dip=1200)
plt.show()