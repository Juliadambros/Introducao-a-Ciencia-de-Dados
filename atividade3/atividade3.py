import pandas as pd

def exercicio1():
    df = pd.read_csv(
        "atividade3/vendas.csv", 
        sep=",", 
        encoding='utf-8', 
        usecols=['produto', 'quantidade', 'preco_unitario'],
        dtype={
            'produto' : 'string',
            'quantidade' : 'int64',
            'preco_unitario' : 'float64'
        }
    )

    print(df)

def exercicio2():
    df = pd.read_csv(
        "atividade3/clima.CSV",
        sep=";",
        encoding='utf-8', 
        skiprows=8,
        parse_dates=['Data'],
        index_col='Data',

    )

    print(df)

def exercicio3():
    df = pd.read_csv(
        "atividade3/log_sistema.csv",
        comment="#",
        nrows=2,
        engine="python"
    )

    print(df)

def exercicio4():
    df = pd.read_csv(
        "atividade3/estoque.csv",
        sep=";",
        decimal=",",
        dtype={
            "valor_unitario": "float64",
            "peso_kg": "float64"
        }
    )

    print(df)
    print(df.dtypes)

def exercicio5():
    df = pd.read_csv(
        "atividade3/transacoes.csv",
        sep=",",
        decimal=".",
        dtype={
            "valor": "float64",
        }
    )

    print(df)
    print(df.dtypes)

def exercicio6():
    df = pd.read_csv(
        "atividade3/sensores.csv",
        sep=",",
        na_values=["NA", "-"] 
    )

    print(df)
    print()
    df.info() 

def exercicio7():
    df = pd.read_csv(
        "atividade3/experimento.csv", 
        sep=","
    )
    print(df.head())
    print()
    print(df.tail())
    print()
    print(df.describe())

def exercicio8():
    df = pd.read_csv(
        "atividade3/big_data_simulado.csv", 
        sep=","
    )

    df.info()

def exercicio9():
    df = pd.read_csv("atividade3/notas.csv")

    print(df.describe())
    print("\nMédia das disciplinas:")
    print(df[['matematica','portugues','historia']].mean())

def exercicio10():
    for bloco in pd.read_csv("atividade3/transacoes_grandes.csv", chunksize=20):
        print("Número de linhas do bloco:", len(bloco))
        print("Primeiras 3 linhas:")
        print(bloco.head(3))
        print("-" * 40)

def exercicio11():
    for bloco in pd.read_csv(
        "atividade3/dados_sensor_gigante.csv",
        chunksize=10,
        na_values=["NA", "-"]
    ):
        bloco["temperatura"] = pd.to_numeric(bloco["temperatura"], errors="coerce")

        media_temp = bloco["temperatura"].mean()
        faltantes = bloco["temperatura"].isna().sum()

        print("Bloco com", len(bloco), "linhas")
        print("Temperatura média:", media_temp)
        print("Valores ausentes em temperatura:", faltantes)
        print("-" * 40)


if __name__ == "__main__":
    exercicio1()
    exercicio2()
    exercicio3()
    exercicio4()
    exercicio5()
    exercicio6()
    exercicio7()
    exercicio8()
    exercicio9()
    exercicio10()
    exercicio11()

