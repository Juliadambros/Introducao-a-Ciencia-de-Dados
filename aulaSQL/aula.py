import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Julia26.",
    database="mydb"
)

cursor = conexao.cursor()
cursor.execute("SELECT * FROM usuarios")

for linha in cursor:
    print(linha)

conexao.close()