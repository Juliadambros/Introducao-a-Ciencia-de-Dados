import os
import json
import requests
from pathlib import Path

def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def criar_pastas(*pastas):
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)

def limpar_nome_arquivo(nome):
    invalidos = '<>:"/\\|?*'
    for c in invalidos:
        nome = nome.replace(c, "_")
    return nome.strip()

def salvar_texto(caminho_arquivo, titulo, resumo):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"Título: {titulo}\n\n")
        arquivo.write("Resumo:\n")
        arquivo.write(resumo)

def salvar_historico(caminho_arquivo, termo, titulo):
    with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Pesquisa: {termo} | Resultado: {titulo}\n")

def baixar_imagem(url, caminho_arquivo):
    if not url or url == "N/A":
        return False

    try:
        resposta = requests.get(url, timeout=20)
        resposta.raise_for_status()

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(resposta.content)

        return True
    except requests.RequestException:
        return False

def buscar_filme(base_url, api_key, termo):
    params = {
        "apikey": api_key,
        "t": termo
    }

    resposta = requests.get(base_url, params=params, timeout=20)
    resposta.raise_for_status()
    return resposta.json()

def main():
    credenciais = carregar_json("Trabalho1/credentials.json")
    config = carregar_json("Trabalho1/config.json")

    api_key = credenciais["API_KEY"]
    base_url = config["api"]["base_url"]

    text_dir = config["output_config"]["text_dir"]
    image_dir = config["output_config"]["image_dir"]
    history_file = config["output_config"]["history_file"]

    criar_pastas(text_dir, image_dir, "resultados")

    termo_pesquisa = input("Digite o nome do filme: ").strip()

    if not termo_pesquisa:
        print("Nenhum filme foi informado.")
        return

    try:
        dados = buscar_filme(base_url, api_key, termo_pesquisa)

        if dados.get("Response") != "True":
            print("Filme não encontrado.")
            return

        titulo = dados.get("Title", "Sem título")
        resumo = dados.get("Plot", "Sem resumo")
        poster = dados.get("Poster", "N/A")

        nome_base = limpar_nome_arquivo(titulo)

        caminho_texto = os.path.join(text_dir, f"{nome_base}.txt")
        caminho_imagem = os.path.join(image_dir, f"{nome_base}.jpg")

        salvar_texto(caminho_texto, titulo, resumo)
        salvar_historico(history_file, termo_pesquisa, titulo)

        imagem_salva = baixar_imagem(poster, caminho_imagem)

        print("\nResultado da pesquisa:")
        print(f"Título: {titulo}")
        print(f"Resumo: {resumo}")

        print(f"\nTexto salvo em: {caminho_texto}")

        if imagem_salva:
            print(f"Imagem salva em: {caminho_imagem}")
        else:
            print("Imagem não disponível.")

    except requests.RequestException as erro:
        print(f"Erro na requisição: {erro}")
    except FileNotFoundError as erro:
        print(f"Arquivo não encontrado: {erro}")
    except json.JSONDecodeError:
        print("Erro ao ler os arquivos JSON.")
    except Exception as erro:
        print(f"Erro inesperado: {erro}")

if __name__ == "__main__":
    main()