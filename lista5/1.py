import pandas as pd

df = pd.read_csv(
    "lista5/vendas.csv",
    header=None,        
    index_col=0,        
    na_values="ND"      
)

print(df.head())
print(df.info())