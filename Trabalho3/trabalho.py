import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import errorcode

CSV_PATH = "Trabalho3/vendas-anuais-de-gasolina-c-por-municipio.csv"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "trabalho3"
}

PASTA_SAIDA = "Trabalho3/resultados"
os.makedirs(PASTA_SAIDA, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(PASTA_SAIDA, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def carregar_dados():
    try:
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")
        df.columns = [
            "ano", "regiao", "uf", "produto",
            "codigo_ibge", "municipio", "vendas"
        ]

        df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
        df["vendas"] = pd.to_numeric(df["vendas"], errors="coerce")
        df["codigo_ibge"] = pd.to_numeric(df["codigo_ibge"], errors="coerce")

        df = df.dropna()

        df["ano"] = df["ano"].astype(int)
        df["codigo_ibge"] = df["codigo_ibge"].astype(int)

        logging.info("Dados carregados com sucesso.")
        return df

    except FileNotFoundError:
        logging.error("Arquivo CSV não encontrado.")
        print("Erro: arquivo CSV não encontrado.")
        return None

    except pd.errors.EmptyDataError:
        logging.error("Arquivo CSV está vazio.")
        print("Erro: o arquivo CSV está vazio.")
        return None

    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        print("Erro ao carregar dados:", e)
        return None


def filtrar_dados(df):
    try:
        anos = sorted(df["ano"].unique())
        ultimos = anos[-10:]
        df_filtrado = df[df["ano"].isin(ultimos)]

        logging.info("Filtragem dos últimos 10 anos concluída.")
        return df_filtrado

    except Exception as e:
        logging.error(f"Erro ao filtrar dados: {e}")
        print("Erro ao filtrar dados:", e)
        return None


def criar_estrutura():
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS trabalho3")
        cursor.execute("USE trabalho3")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                ano INT,
                regiao VARCHAR(50),
                uf VARCHAR(5),
                produto VARCHAR(50),
                codigo_ibge INT,
                municipio VARCHAR(100),
                vendas FLOAT,
                PRIMARY KEY (ano, municipio, uf)
            )
        """)

        conn.commit()
        logging.info("Banco de dados e tabela criados/verificados com sucesso.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuário ou senha.")
            logging.error("Erro de usuário ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados não existe.")
            logging.error("Banco de dados não existe.")
        else:
            print("Erro no MySQL:", err)
            logging.error(f"Erro no MySQL ao criar estrutura: {err}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


def salvar_no_mysql(df):
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for _, linha in df.iterrows():
            cursor.execute("""
                SELECT COUNT(*) FROM vendas
                WHERE ano = %s AND municipio = %s AND uf = %s
            """, (linha["ano"], linha["municipio"], linha["uf"]))

            existe = cursor.fetchone()[0]

            if existe:
                cursor.execute("""
                    UPDATE vendas
                    SET regiao = %s,
                        produto = %s,
                        codigo_ibge = %s,
                        vendas = %s
                    WHERE ano = %s AND municipio = %s AND uf = %s
                """, (
                    linha["regiao"],
                    linha["produto"],
                    linha["codigo_ibge"],
                    linha["vendas"],
                    linha["ano"],
                    linha["municipio"],
                    linha["uf"]
                ))
            else:
                cursor.execute("""
                    INSERT INTO vendas (
                        ano, regiao, uf, produto,
                        codigo_ibge, municipio, vendas
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    linha["ano"],
                    linha["regiao"],
                    linha["uf"],
                    linha["produto"],
                    linha["codigo_ibge"],
                    linha["municipio"],
                    linha["vendas"]
                ))

        conn.commit()
        logging.info("Dados salvos no MySQL com sucesso.")

    except mysql.connector.Error as err:
        if conn is not None:
            conn.rollback()

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuário ou senha.")
            logging.error("Erro de usuário ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados não existe.")
            logging.error("Banco de dados não existe.")
        else:
            print("Erro no MySQL:", err)
            logging.error(f"Erro ao salvar no MySQL: {err}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


def consultar_dados():
    conn = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM vendas", conn)
        logging.info("Consulta ao banco executada com sucesso.")
        return df

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuário ou senha.")
            logging.error("Erro de usuário ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados não existe.")
            logging.error("Banco de dados não existe.")
        else:
            print("Erro no MySQL:", err)
            logging.error(f"Erro ao consultar dados: {err}")
        return None

    except Exception as e:
        print("Erro ao consultar dados:", e)
        logging.error(f"Erro geral ao consultar dados: {e}")
        return None

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def calcular_estatisticas(df):
    try:
        stats = df["vendas"].describe()

        print("\nESTATÍSTICAS:")
        print(stats)

        caminho_stats = os.path.join(PASTA_SAIDA, "estatisticas.txt")
        with open(caminho_stats, "w", encoding="utf-8") as f:
            f.write("ESTATÍSTICAS DAS VENDAS\n\n")
            f.write(str(stats))

        logging.info("Estatísticas calculadas e salvas com sucesso.")

    except Exception as e:
        logging.error(f"Erro ao calcular estatísticas: {e}")
        print("Erro ao calcular estatísticas:", e)


def grafico_barras(df):
    try:
        vendas_ano = df.groupby("ano")["vendas"].sum()

        plt.figure(figsize=(10, 6))
        plt.bar(vendas_ano.index.astype(str), vendas_ano.values)
        plt.title("Total de Vendas de Gasolina por Ano")
        plt.xlabel("Ano")
        plt.ylabel("Vendas Totais")
        plt.xticks(rotation=45)
        plt.tight_layout()

        caminho = os.path.join(PASTA_SAIDA, "grafico_barras_ano.png")
        plt.savefig(caminho)
        plt.close()

        logging.info("Gráfico de barras gerado com sucesso.")

    except Exception as e:
        logging.error(f"Erro ao gerar gráfico de barras: {e}")
        print("Erro ao gerar gráfico de barras:", e)


def grafico_area_empilhada(df):
    try:
        tabela = df.pivot_table(
            index="ano",
            columns="regiao",
            values="vendas",
            aggfunc="sum",
            fill_value=0
        )

        plt.figure(figsize=(11, 6))
        plt.stackplot(tabela.index, tabela.T.values, labels=tabela.columns)
        plt.title("Evolução das Vendas por Região ao Longo dos Anos")
        plt.xlabel("Ano")
        plt.ylabel("Vendas")
        plt.legend(title="Região", loc="upper left")
        plt.tight_layout()

        caminho = os.path.join(PASTA_SAIDA, "grafico_area_regioes.png")
        plt.savefig(caminho)
        plt.close()

        logging.info("Gráfico de área empilhada gerado com sucesso.")

    except Exception as e:
        logging.error(f"Erro ao gerar gráfico de área empilhada: {e}")
        print("Erro ao gerar gráfico de área empilhada:", e)


def main():
    try:
        logging.info("Iniciando pipeline")

        df = carregar_dados()
        if df is None:
            return

        df = filtrar_dados(df)
        if df is None or df.empty:
            print("Erro: não há dados válidos para processar.")
            logging.warning("DataFrame vazio após filtragem.")
            return

        criar_estrutura()
        salvar_no_mysql(df)

        df_db = consultar_dados()
        if df_db is None or df_db.empty:
            print("Erro: não foi possível consultar dados do banco.")
            logging.warning("Consulta retornou vazia.")
            return

        calcular_estatisticas(df_db)
        grafico_barras(df_db)
        grafico_area_empilhada(df_db)

        logging.info("Pipeline executado com sucesso.")
        print("Pipeline executado com sucesso.")
        print(f"Resultados salvos em: {PASTA_SAIDA}")

    except Exception as e:
        logging.error(f"Erro geral no pipeline: {e}")
        print("Erro:", e)


if __name__ == "__main__":
    main()