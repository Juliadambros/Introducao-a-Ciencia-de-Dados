import pandas as pd
import numpy as np

relatorio_anual = pd.DataFrame({
    "ano": [2025] * 50,
    "valor": np.random.randint(100, 1000, 50)
})

with pd.ExcelWriter("lista5/relatorio.xlsx") as writer:
    relatorio_anual.to_excel(writer, sheet_name="Resultados", index=False)
    relatorio_anual.to_excel(writer, sheet_name="Dados Brutos", index=False)

df = pd.read_excel("lista5/relatorio.xlsx", sheet_name="Dados Brutos")

print(df)