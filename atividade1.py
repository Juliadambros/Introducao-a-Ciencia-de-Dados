import math


def exercicio1():
    nome = "Júlia Dambrós"
    idade = 20
    altura = 1.74
    cidade = "Renascença"

    print(f"{nome}, {idade} anos, "f"{altura}m — {cidade}")

def exercicio2():
    lista = ["macarrão", "café", "leite", "suco", "chocolate"]

    lista.append("coca")
    lista.append("farofa")
    lista.remove("leite")
    lista.sort()

    print("Lista final:", lista)

def exercicio3():
    notas = [6.5, 8.0, 7.3, 9.0, 2.5]

    media = sum(notas) / len(notas)
    maior = max(notas)
    menor = min(notas)

    print("Média:", media)
    print("Maior nota:", maior)
    print("Menor nota:", menor)

def exercicio4():
    impares = [x for x in range(1, 21) if x % 2 != 0]

    print("Números ímpares de 1 a 20:")
    print(impares)

def exercicio5():
    contato = {
        "Júlia" : "9974746464",
        "Ana" : "9292992292",
        "Maria" : "9988383838"
    }

    nome = input("Digite o nome para buscar: ")

    if nome in contato:
        print("Telefone:", contato[nome])
    else:
        print("Contato não encontrado")

def exercicio6(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def exercicio7():
    frase = input("Digite uma frase: ").lower()

    palavras = frase.split()
    contador = {}

    for palavra in palavras:
        if palavra in contador:
            contador[palavra] += 1
        else:
            contador[palavra] = 1

    ordenado = sorted(contador.items(), key=lambda x: x[1], reverse=True)

    print("3 palavras mais frequentes:")
    for palavra, quantidade in ordenado[:3]:
        print(palavra, ":", quantidade)

def estatisticas(*numeros):
    media = sum(numeros) / len(numeros)
    maior = max(numeros)
    menor = min(numeros)

    return {
        "media": media,
        "maximo": maior,
        "minimo": menor
    }


def exercicio8():
    resultado = estatisticas(5, 8, 10, 3, 7)
    print(resultado)

class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def vender(self, quantidade):
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            print("Venda realizada.")
        else:
            print("Estoque insuficiente.")

    def repor(self, quantidade):
        self.estoque += quantidade
        print("Estoque atualizado.")

    def exibir_info(self):
        print("Produto:", self.nome)
        print("Preço:", self.preco)
        print("Estoque:", self.estoque)


def exercicio9():
    p = Produto("Notebook", 3500, 10)

    p.exibir_info()
    p.vender(3)
    p.repor(5)
    p.exibir_info()

class Veiculo:
    def tipo_habilitacao(self):
        print("Tipo de habilitação genérico")


class Carro(Veiculo):
    def tipo_habilitacao(self):
        print("Habilitação necessária: Categoria B")


class Moto(Veiculo):
    def tipo_habilitacao(self):
        print("Habilitação necessária: Categoria A")


def exercicio10():
    carro = Carro()
    moto = Moto()

    carro.tipo_habilitacao()
    moto.tipo_habilitacao()

if __name__ == "__main__":
    exercicio1()
    exercicio2()
    exercicio3()
    exercicio4()
    exercicio5()

    d = exercicio6((1, 2), (4, 6))
    print("Distância:", d)

    exercicio7()
    exercicio8()
    exercicio9()
    exercicio10()