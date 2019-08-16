import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.rc('font', family='Times New Roman')

data=pd.read_csv("lab_result816/lab_auc.csv")
plt.plot(data['number of pairs'],data['SCENARIO'],marker="o",label='SCENARIO')
plt.plot(data['number of pairs'],data['Wang_CC'],marker="o",label='Wang_CC',linestyle='dashed')
plt.plot(data['number of pairs'],data['Wang_BP'],marker="o",label='Wang_BP',linestyle='dotted')
plt.plot(data['number of pairs'],data['Wang_MF'],marker="o",label='Wang_MF')
plt.plot(data['number of pairs'],data['Resnik_CC'],marker="o",label='Resnik_CC',linestyle='dashed')
plt.plot(data['number of pairs'],data['Resnik_BP'],marker="o",label='Resnik_BP',linestyle='dotted')
plt.plot(data['number of pairs'],data['Resnik_MF'],marker="o",label='Resnik_MF')
plt.plot(data['number of pairs'],data['Lin_CC'],marker="o",label='Lin_CC',linestyle='dashed')
plt.plot(data['number of pairs'],data['Lin_BP'],marker="o",label='Lin_BP',linestyle='dotted')
plt.plot(data['number of pairs'],data['Lin_MF'],marker="o",label='Lin_MF')

plt.xlabel("Pairs of Validation Data Set",fontsize=22)
plt.xticks([150,300,600,1200],fontsize=15)
plt.yticks(fontsize=18)
plt.ylabel("AUC Score",fontsize=22)
plt.legend(loc="lower right",ncol=3)
plt.show()