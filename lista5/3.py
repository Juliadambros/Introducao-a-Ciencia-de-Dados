import requests
import pandas as pd

busca = input("Digite o nome do filme: ")

url = "http://www.omdbapi.com/"
params = {
    "apikey": "",
    "s": busca
}

r = requests.get(url, params=params)
dados = r.json()

if "Search" in dados:
    df = pd.DataFrame(dados["Search"])
    print(df)
else:
    print("Erro:", dados)