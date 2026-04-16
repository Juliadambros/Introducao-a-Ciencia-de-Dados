import firebase_admin
from firebase_admin import credentials, firestore, auth, messaging
from firebase_admin.exceptions import FirebaseError
import mysql.connector
from decimal import Decimal

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("lista6/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    print("Firebase inicializado com sucesso.")

except FirebaseError as e:
    print("Erro ao inicializar Firebase:", e)

db = firestore.client()

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Julia26.",
        database="mydb"
    )
    print("Conexão com MySQL realizada com sucesso.")

except mysql.connector.Error as e:
    print("Erro ao conectar no MySQL:", e)
    conexao = None

def criar_usuario():
    try:
        user = auth.create_user(
            email="teste@gmail.com",
            password="123456",
            display_name="Julia"
        )

        print(f"UID: {user.uid}")

        usuario = auth.get_user(user.uid)
        print("Email:", usuario.email)
        print("Nome:", usuario.display_name)

    except FirebaseError as e:
        print("Erro no Firebase Auth:", e)

    except Exception as e:
        print("Erro inesperado ao criar usuário:", e)

def get_mysql_data():
    if conexao is None:
        print("Sem conexão com o MySQL.")
        return []

    try:
        print("Obtendo dados do MySQL...")
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    except mysql.connector.Error as e:
        print("Erro ao consultar MySQL:", e)
        return []

def enviar_produtos_firestore():
    mysql_records = get_mysql_data()

    if not mysql_records:
        print("Nenhum produto encontrado para enviar.")
        return

    print("Salvando dados no Firestore...")

    for record in mysql_records:
        try:
            doc_id = str(record["id"])

            if isinstance(record["preco"], Decimal):
                record["preco"] = float(record["preco"])

            del record["id"]

            db.collection("produtos_mysql").document(doc_id).set(record)

            print(f"Documento '{doc_id}' salvo no Firestore.")

        except FirebaseError as e:
            print(f"Erro ao salvar no Firestore (doc {record}):", e)

        except Exception as e:
            print("Erro inesperado ao salvar:", e)

def consultar_produtos():
    print("\nConsultando produtos com preço > 15...\n")

    valor_minimo = 15.0

    try:
        docs = db.collection("produtos_mysql") \
                 .where("preco", ">", valor_minimo) \
                 .stream()

        encontrou = False
        for doc in docs:
            data = doc.to_dict()
            print(f"Nome: {data['nome']} | Preço: R$ {data['preco']}")
            encontrou = True

        if not encontrou:
            print("Nenhum produto encontrado.")

    except FirebaseError as e:
        print("Erro na consulta do Firestore:", e)

def enviar_notificacao_topico():
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title="Promoção!",
                body="Temos novos produtos com desconto"
            ),
            topic="produtos"
        )

        response = messaging.send(message)
        print("Notificação enviada! ID:", response)

    except FirebaseError as e:
        print("Erro ao enviar notificação:", e)

    except Exception as e:
        print("Erro inesperado no envio:", e)

def menu():
    while True:
        print("\n========= MENU =========")
        print("1 - Criar usuário")
        print("2 - Enviar produtos do MySQL para o Firestore")
        print("3 - Consultar produtos com preço > 15")
        print("4 - Enviar notificação")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            enviar_produtos_firestore()
        elif opcao == "3":
            consultar_produtos()
        elif opcao == "4":
            enviar_notificacao_topico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

menu()

if conexao is not None:
    try:
        conexao.close()
        print("Conexão com MySQL encerrada.")
    except Exception as e:
        print("Erro ao fechar conexão:", e)