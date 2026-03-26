import string
import csv
import requests
from bs4 import BeautifulSoup
from collections import Counter

def contar_palavras(arquivo_txt):
    try:
        with open(arquivo_txt, "r", encoding="utf-8") as f:
            texto = f.read().lower()

        for p in string.punctuation:
            texto = texto.replace(p, "")

        palavras = texto.split()
        contagem = Counter(palavras)

        print("\nTop 10 palavras:")
        for palavra, freq in contagem.most_common(10):
            print(palavra, "-", freq)

    except FileNotFoundError:
        print("Arquivo de texto não encontrado.")

def analisar_csv(arquivo_csv):
    total = 0
    quantidade = 0

    try:
        with open(arquivo_csv, "r", encoding="utf-8") as f:
            leitor = csv.DictReader(f)

            for linha in leitor:
                preco = float(linha["preco_unitario"])
                total += preco
                quantidade += 1

        if quantidade > 0:
            media = total / quantidade
            print(f"\nPreço médio dos produtos: {media:.2f}")
        else:
            print("\nNenhum produto encontrado.")

    except FileNotFoundError:
        print("Arquivo CSV não encontrado.")

def extrair_h2(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")

        titulos = soup.find_all("h2")

        if not titulos:
            print("\nNenhum <h2> encontrado nessa página.")
            return

        print("\nTítulos <h2> encontrados:")
        for t in titulos:
            print("-", t.get_text(strip=True))

    except requests.RequestException as e:
        print("Erro ao acessar a página:", e)

def buscar_github(topico):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": topico,
        "per_page": 5
    }

    try:
        resposta = requests.get(url, params=params, timeout=10)
        dados = resposta.json()

        print(f"\nRepositórios sobre '{topico}':")

        for repo in dados.get("items", []):
            print(repo["name"])
            print(repo["html_url"])
            print("-------------------")

    except requests.RequestException:
        print("Erro na requisição da API.")

def main():
    while True:
        print("\n=== MENU ===")
        print("1 - Contar palavras")
        print("2 - Analisar CSV")
        print("3 - Extrair <h2> de site")
        print("4 - Buscar repositórios no GitHub")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            arquivo = input("Digite o nome do arquivo .txt: ")
            contar_palavras(arquivo)

        elif opcao == "2":
            arquivo = input("Digite o nome do arquivo CSV: ")
            analisar_csv(arquivo)

        elif opcao == "3":
            url = input("Digite a URL: ")
            extrair_h2(url)

        elif opcao == "4":
            topico = input("Digite o tópico: ")
            buscar_github(topico)

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()