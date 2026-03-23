import numpy as np

arr = np.random.randint(100, 500, 12)

r = arr.reshape((3,4))

venda = r.sum(axis=1)

media = r.mean(axis=0)

dias = np.sum(r > 400)

print("Array original:")
print(arr)

print("\nMatriz 3x4:")
print(r)

print("\nTotal de vendas por linha:")
print(venda)

print("\nMédia por coluna:")
print(media)

print("\nQuantidade de valores > 400:")
print(dias)

#desafios

arr1 = np.arange(0,10)
print("\nArray 0-9:")
print(arr1)

print("\nMatriz booleana:")
print(np.ones((3,3), dtype=bool))

impar = arr1[arr1 % 2 == 1]
print("\nÍmpares:")
print(impar)

print("\nÍmpares negativos:")
print(impar * -1)

matriz = np.random.randint(1, 100, (5,5))
print("\nMatriz 5x5:")
print(matriz)

print("\nSoma das colunas:")
print(matriz.sum(axis=0))

print("\nMaior valor por linha:")
print(matriz.max(axis=1))

a = np.array([1, 2, 3, 4, 5])
print("\nBroadcasting (a + 2):")
print(a + 2)


a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("\nConcatenação:")
print(np.concatenate((a, b)))

arr2 = np.array([10, 20, 30, 40])
print("\nArray invertido:")
print(arr2[::-1])

#desafios2

temp = np.array([22, 24, 21, 23, 25, 20, 22])

print("\nTemperatura média:")
print(temp.mean())

print("Dia mais quente:")
print(temp.max())

vendas = np.random.randint(50, 200, (3,4))

print("\nVendas:")
print(vendas)

print("Total por produto:")
print(vendas.sum(axis=1))

notas = np.array([75, 88, 92, 65, 70, 80, 95, 60, 85, 78])

print("\nNota mínima:")
print(notas.min())

print("Nota máxima:")
print(notas.max())


sensor = np.random.rand(20)

print("\nLeituras acima de 0.7:")
print(sensor[sensor > 0.7])


precos = np.array([120.50, 121.00, 119.80, 122.30, 120.00])

variacao = (precos[1:] - precos[:-1]) / precos[:-1] * 100

print("\nVariação percentual:")
print(variacao)


print("\nMatriz identidade:")
print(np.eye(4))


print("\nZeros 3x3:")
print(np.zeros((3,3)))

print("\nUns 2x5:")
print(np.ones((2,5)))

img = np.random.randint(0, 255, 25)

print("\nImagem 5x5:")
print(img.reshape((5,5)))

nums = np.arange(10)

print("\nPares:")
print(nums[nums % 2 == 0])

arr3 = np.array([1,2,3,4,5])

print("\nSoma acumulada:")
print(np.cumsum(arr3))

print("\nLinspace:")
print(np.linspace(0,10,5))

notas = np.array([80,90,70])
pesos = np.array([0.3,0.5,0.2])

print("\nMédia ponderada:")
print(np.average(notas, weights=pesos))

m = np.array([[2,8,6],
              [3,7,9]])

print("\nTransposta:")
print(m.T)

m = np.arange(12).reshape(3,4)

print("\nLinhas invertidas:")
print(m[::-1])

a = np.array([1,2,3])
b = np.array([3,2,1])

print("\nComparação:")
print(a == b)

arr = np.random.randint(0,100,10)

print("\nArray:")
print(arr)

print("Maiores que 50:")
print(arr > 50)

arr = np.array([1,7,3,7,5,7])

print("\nQuantidade de 7:")
print(np.count_nonzero(arr == 7))

arr = np.array([1.23, 2.78, 3.50, 4.11])

print("\nArredondado:")
print(np.round(arr))

a = np.array([1,2,3])
b = np.array([4,5,6])

print("\nEmpilhado vertical:")
print(np.vstack((a,b)))
