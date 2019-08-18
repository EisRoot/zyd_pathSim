import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import math

matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'
matplotlib.rc('font', family='Times New Roman')
matplotlib.rcParams.update({'font.size': 34})
plt.figure(figsize=(10, 10))
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
data=pd.read_csv("lab_result816/lab_auc.csv")
#data=pd.read_csv("lab_result/lab_efficacy.csv")
# list1=[]
# list2=[]
# for i in data['Parallel']:
#     list1.append(math.log10(i))
# for i in data['Without Parallel']:
#     list2.append(math.log10(i))
# plt.plot(data['length'],list1,marker="^",markersize=14,color='red',label='Parallel',lw=3)
# plt.plot(data['length'],list2,marker="o",markersize=14,color='blue',label='Baseline',lw=3)
plt.plot(data['number of pairs'],data['SCENARIO'],marker="^",markersize=14,color='red',label='SCENARIO',lw=3)
plt.plot(data['number of pairs'],data['Wang_CC'],marker="o",markersize=14,label='Wang_CC',linestyle='dashed',lw=3)
plt.plot(data['number of pairs'],data['Wang_BP'],marker="p",markersize=14,label='Wang_BP',linestyle='dotted', color='darkblue',lw=3)
plt.plot(data['number of pairs'],data['Wang_MF'],marker="s",markersize=14,label='Wang_MF',lw=3)
# plt.plot(data['number of pairs'],data['Resnik_CC'],marker="o",markersize=14,lw=3,label='Resnik_CC',linestyle='dashed')
# plt.plot(data['number of pairs'],data['Resnik_BP'],marker="p",markersize=14,lw=3,label='Resnik_BP',linestyle='dotted',color='darkblue')
# plt.plot(data['number of pairs'],data['Resnik_MF'],marker="s",markersize=14,lw=3,label='Resnik_MF')
# plt.plot(data['number of pairs'],data['Lin_CC'],marker="o",markersize=14,lw=3,label='Lin_CC',linestyle='dashed')
# plt.plot(data['number of pairs'],data['Lin_BP'],marker="p",markersize=14,lw=3,label='Lin_BP',linestyle='dotted',color='darkblue')
# plt.plot(data['number of pairs'],data['Lin_MF'],marker="s",markersize=14,lw=3,label='Lin_MF')



plt.xlabel("Sizes of Validation Data Set",fontsize=42)
plt.xticks([150,300,600,1200],fontsize=35)
plt.yticks([0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00],fontsize=35)
plt.ylabel("AUC",fontsize=42)
plt.legend(loc="lower right",ncol=1)
plt.tight_layout()
plt.savefig('line_Wang.pdf')
plt.show()
# plt.xlabel("Max Length of Gene Meta Path",fontsize=42)
# plt.xticks([3,5,7,9],fontsize=35)
# plt.yticks([0,1,2,3,4],['',r'$10$',r'$10^2$',r'$10^3$',r'$10^4$'],fontsize=35)
# plt.ylabel(r'Average Computing Time(s)',fontsize=42)
# plt.legend(loc="lower right",ncol=1)
# plt.tight_layout()
# plt.savefig('computing.pdf')
# plt.show()