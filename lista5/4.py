import pandas as pd
import sqlalchemy as sqla

engine = sqla.create_engine("sqlite:///meu_banco.db")

with engine.connect() as conn:
    conn.execute(sqla.text("""
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY,
            nome TEXT,
            preco REAL
        )
    """))

    conn.execute(sqla.text("""
        INSERT INTO produtos(nome, preco)
        VALUES ('Mouse', 50.0), ('Teclado', 120.0), ('Monitor', 800.0)
    """))
    
    conn.commit()

df = pd.read_sql("SELECT * FROM produtos", engine)

print(df)