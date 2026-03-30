import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import json


def carregar_config(caminho_json):
    with open(caminho_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def carregar_dados(config):
    caminho_csv = config["input_config"]["csv_path"]
    separador = config["input_config"]["separator"]
    encoding = config["input_config"]["encoding"]

    df = pd.read_csv(caminho_csv, sep=separador, encoding=encoding)

    df.columns = df.columns.str.strip()

    coluna_ano = config["columns_config"]["year_column"]
    coluna_vendas = config["columns_config"]["sales_column"]

    df[coluna_ano] = df[coluna_ano].astype(int)
    df[coluna_vendas] = pd.to_numeric(df[coluna_vendas], errors='coerce')

    df = df.dropna()

    return df


def filtrar_ultimos_anos(df, config):
    coluna_ano = config["columns_config"]["year_column"]

    anos_validos = df[coluna_ano].dropna().unique()
    anos_validos = sorted(anos_validos)

    n = config["filter_config"]["last_n_years"]
    ultimos_anos = anos_validos[-n:]

    df_filtrado = df[df[coluna_ano].isin(ultimos_anos)]

    return df_filtrado


def calcular_estatisticas(df, config):
    coluna_vendas = config["columns_config"]["sales_column"]

    desc = df[coluna_vendas].describe().to_dict()
    desc["sum"] = df[coluna_vendas].sum()
    desc["variance"] = df[coluna_vendas].var()

    return desc


def gerar_grafico(df, config):
    coluna_ano = config["columns_config"]["year_column"]
    coluna_vendas = config["columns_config"]["sales_column"]
    caminho_grafico = config["output_config"]["graph_path"]

    vendas_por_ano = df.groupby(coluna_ano)[coluna_vendas].sum()
    valores = vendas_por_ano.values / 1e9

    plt.figure(figsize=(10, 5))
    plt.plot(vendas_por_ano.index, valores, marker='o')

    plt.title("Vendas de Gasolina por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Bilhões de Litros")
    plt.xticks(vendas_por_ano.index)

    plt.grid(True)
    plt.savefig(caminho_grafico)
    plt.close()


def gerar_grafico_regiao(df, config):
    coluna_regiao = config["columns_config"]["region_column"]
    coluna_vendas = config["columns_config"]["sales_column"]
    caminho = config["output_config"]["region_graph_path"]

    vendas_por_regiao = df.groupby(coluna_regiao)[coluna_vendas].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(
        vendas_por_regiao.values,
        labels=vendas_por_regiao.index,
        autopct='%1.1f%%',
        startangle=90
    )

    plt.title("Distribuição de Vendas de Gasolina por Região")

    plt.savefig(caminho)
    plt.close()


def salvar_no_banco(df, config):
    caminho_banco = config["output_config"]["database_path"]
    nome_tabela = config["output_config"]["table_name"]

    conn = sqlite3.connect(caminho_banco)
    df.to_sql(nome_tabela, conn, if_exists="replace", index=False)
    conn.close()


def main():
    config = carregar_config("dados.json")
    df = carregar_dados(config)
    df_filtrado = filtrar_ultimos_anos(df, config)

    stats = calcular_estatisticas(df_filtrado, config)

    print("\nESTATÍSTICAS:")
    for chave, valor in stats.items():
        print(f"{chave}: {valor:.2f}")

    gerar_grafico(df_filtrado, config)
    gerar_grafico_regiao(df_filtrado, config)
    salvar_no_banco(df_filtrado, config)


if __name__ == "__main__":
    main()