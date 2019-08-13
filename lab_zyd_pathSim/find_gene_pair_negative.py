import pandas as pd


genes=pd.read_csv("zyd_network/gene_without_EC.csv")
list=[]
for i in range(0,200):
    samples=genes.sample(2)
    H1=samples["HGNC ID"].iloc[0]
    H2=samples["HGNC ID"].iloc[1]
    R1=samples["RefSeq IDs"].iloc[0]
    R2=samples["RefSeq IDs"].iloc[1]
    list.append({
        "gene1":H1,
        "gene2":H2,
        "RefSeq1":R1,
        "RefSeq2":R2
    })
print(list)
re=pd.DataFrame(list)
re.to_csv("negative_pair.csv",index=None)