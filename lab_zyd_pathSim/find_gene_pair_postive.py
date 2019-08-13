import pandas as pd
genes=pd.read_csv("zyd_network/gene_with_EC.csv")
#print(genes)
final_list=[]
for name, group in genes.groupby('Enzyme IDs'):
    if len(group)>1:
        print(group)
        list=[]
        for index,row in group.iterrows():
            list.append({
                "HGNC":row['HGNC ID'],
                "RefSeq":row['RefSeq IDs'],
                "Enzyme IDs":row['Enzyme IDs']
            })
        list2=list
        for i in list:
            list2.remove(i)
            for j in list2:
                final_list.append({
                    "gene1":i["HGNC"],
                    "RefSeq1":i["RefSeq"],
                    "gene2":j["HGNC"],
                    "RefSeq2":j["RefSeq"],
                    "EC":i["Enzyme IDs"]
                })

re=pd.DataFrame(final_list)
re2=re.sample(80)
re2.to_csv("postive_pair.csv",index=None)
