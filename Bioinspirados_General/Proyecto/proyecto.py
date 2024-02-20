'''
Integrantes:
    Dominguez Ortiz Ruben Adrian
    Gutierrez Viveros Cristian Rogelio

5BV1

Practica 1

'''

import random
import numpy as np
import csv
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder


class cromosoma:
    def __init__(self, genes, accuracy):
        self.genes = genes
        self.accuracy = accuracy

def leer_datos(path):
    data = []
    with open(path, 'r') as archivo:
        reader = csv.reader(archivo)
        next(reader, None)

        for linea in reader:
            data.append(linea)
    return data

def randomize(x, y):

    indices = np.arange(len(x))
    np.random.shuffle(indices)

    x = [x[i] for i in indices]
    y = [y[i] for i in indices]

    return x, y

def split(x, y, n_splits, current):
    size = len(x) // n_splits
    test = []
    train = []
    test_y = []
    train_y = []

    current_i = size * current 
    current_f = size * (current + 1) 

    for i in range(len(x)):
        if i >= current_i and i <= current_f:
            test.append(x[i])
            test_y.append(y[i])
        else:
            train.append(x[i])
            train_y.append(y[i])
    return train, train_y, test, test_y

def ganancia(x, y,individuo):
    columnas = []
    for i in range(len(x[0])):
        if individuo[i] == 1:
            columnas.append(i)
    scores = np.zeros(5)
    # Esta linea es para poder segmentar por indices las caracteristicas lol
    x = np.array(x)
    for i in range(4):
        x_train, y_train, x_test, y_test = split(x[:,columnas], y, 4, i)
        acc = evaluate(x_train, y_train, x_test, y_test)
        scores[i] = acc
    scores[4] = (scores[1] + scores[2] + scores[3] + scores[0]) / 4

    #print(scores)
    return scores[4]


def evaluate(x_train, y_train, x_test, y_test):

    # Mandamos a llamar a scikit para una SVM
    SVM = SVC()
    SVM.fit(x_train, y_train)


    acc = 0
    # Revisamos el accuracy
    pred_SVM = SVM.predict(x_test)

    for i in range(len(y_test)):
        if pred_SVM[i] == y_test[i]:
            acc += 1

    return ((acc*100) / len(y_test))

def generarIndividuo(size):
    # Nos aseguramos que el individuo tenga almenos una caracteristica activada
    vacio = True
    while vacio:
        individuo = []
        for i in range(size):
            using_feature = random.randint(0,1)
            individuo.append(using_feature)
        if 1 in individuo:
            vacio = False
    return individuo


def definirPoblacionInicial(cantidadPoblacion, num_ft, x, y):
    poblacion = []
    for i in range(cantidadPoblacion):
        individuo = generarIndividuo(num_ft)
        acc = ganancia(x,y, individuo)
        poblacion.append(cromosoma(individuo,acc))
    return poblacion


def ruleta(poblacion, x, y):
    probabilidades = []
    nuevagen = []
    acc_total = 0

    # Realizamos la suma total de todos los accuracy
    for elemento in poblacion:
        acc_total += elemento.accuracy

    sumatoria = 0

    # Ahora por cada elemento, ponderamos su probabilidad dividiendo su acc sobre el total
    # Sumatoria nos dara un numero empezando con 0 que ira subiendo con cada acc, hasta llegar a 1
    # Esto nos ayuda a que al generar un numero entre 0 a 1 para la ruleta, solo pasemos por la lista de
    # probabilidades uno a uno hasta encontrear p() > i
    for elemento in poblacion:
        probabilidad = elemento.accuracy / acc_total
        sumatoria += probabilidad
        probabilidades.append(round(sumatoria, 3))

    # print(probabilidades)

    for i in range(10):
        # Creamos las probabilidades tanto para los padres como para su reproduccion
        padre1 = random.random()
        padre2 = random.random()
        reproduccion = random.random()

        reproducidos = 0
        mutados = 0

        seleccionado = False
        hijo1 = []
        hijo2 = []

        for i in range(len(probabilidades)):
            if padre1 < probabilidades[i]:
                padre1 = i
                break

        # seleccionado nos ayuda a que padre1 y padre 2 no sean el mismo individuo
        while not seleccionado:
            for i in range(len(probabilidades)):
                if padre2 < probabilidades[i]:
                    padre2 = i
                    break
            if padre2 == padre1:
                padre2 = random.random()
            else:
                seleccionado = True
                #print("padres: " + str(padre1) + " y " + str(padre2))
        
        #print("Fase de prob")
        if reproduccion <= 0.85:

            reproducidos += 2
            #sprint("Fase de reproduccion")
            hijo1, hijo2 = reproducir(poblacion[padre1], poblacion[padre2],x,y)
            #print("Fase de mutacion")

            mutacion(hijo1,x,y)
            mutacion(hijo2,x,y)
            #print("Fase de seleccion")

            hijo1, hijo2 = seleccion(poblacion[padre1], poblacion[padre2], hijo1, hijo2)


        else:
            hijo1 = poblacion[padre1]
            hijo2 = poblacion[padre2]

        nuevagen.append(hijo1)
        nuevagen.append(hijo2)

    
    return nuevagen

def reproducir(padre1, padre2, x, y):
    hijo1 = []
    hijo2 = []
    admitido = False
    while not admitido:
        umbrales = []
        for i in range(len(padre1.genes)):
            num = random.random()
            umbrales.append(num)

        for i in range(len(padre1.genes)):
            if umbrales[i] < 0.5:
                hijo1.append(padre1.genes[i])
            else:
                hijo1.append(padre2.genes[i])
        
        for i in range(len(padre1.genes)):
            if umbrales[i] < 0.5:
                hijo2.append(padre2.genes[i])
            else:
                hijo2.append(padre1.genes[i])
        if 1 in hijo1 and 1 in hijo2:
            admitido = True
            hijo1 = cromosoma(hijo1, ganancia(x,y,hijo1))
            hijo2 = cromosoma(hijo2, ganancia(x,y,hijo2))
        else:
            hijo1 = []
            hijo2 = []
    #print(hijo)
    return hijo1, hijo2

def seleccion(padre1, padre2, hijo1, hijo2):
    ganancias = [
        [padre1, padre1.accuracy], [padre2, padre2.accuracy], [hijo1, hijo1.accuracy], [hijo2, hijo2.accuracy]
    ]
    ganancias.sort(key=lambda x: x[1], reverse=True)
    mejor1 = ganancias[0][0]
    mejor2 = ganancias[1][0]
    print("Seleccionados en reproduccion y seleccion: ",mejor1.accuracy," y ",mejor2.accuracy)

    return mejor1, mejor2

def mutacion(hijo, x, y):
    admitido = False
    while not admitido:
        umbral_mutacion = []
        nuevos_genes = hijo.genes
        for i in range(len(hijo.genes)):
            num = random.random()
            umbral_mutacion.append(num)
        
        for i in range(len(hijo.genes)):
            if umbral_mutacion[i] <= 0.1:
                nuevos_genes[i] = random.randint(0,1)
        if 1 in nuevos_genes:
            hijo.genes = nuevos_genes
            hijo.accuracy = ganancia(x, y, hijo.genes)
            admitido = True

path = 'TUANDROMD.csv'
data = leer_datos(path)

# Declaramos los datos una matriz manejable
data = np.array(data)



cantidadPoblacion = 20
# restriccion = [(1,3),(3,2)]

genes = len(data[0])
# Separo x y y de data
x = data[:, :-1]
y = data[:, -1]
x = np.array(x)
#restricciones = [0, 3, 0, 2, 0, 0, 0, 0]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
x, y = randomize(x,y)

print([y[0]])
print(x[0])
print(len(x))

num_ft = len(x[0])
#ind = generarIndividuo(len(x[0]))
poblacion = definirPoblacionInicial(cantidadPoblacion, num_ft, x, y)
print(len(poblacion))



generacion = poblacion

generaciones = 75
generacion_counter = 0
print("\nMostrando hijos de cada generacion\n")
#generacion = ruleta(generacion, restricciones)
elementobase = generacion[0].genes
elementobase2 = generacion[10].genes
counter_c = 0
for i in range(generaciones):
    print("generacion",i+1)
    generacion_counter += 1
    generacion = ruleta(generacion, x, y)
    if counter_c == 7:
        break
    if generacion[0].genes == elementobase and generacion[10].genes == elementobase2:
        counter_c += 1
    else:
        elementobase = generacion[0].genes
        elementobase2 = generacion[10].genes
        counter_c = 0


print("Generacion Final")
print("Converge en la generacion numero: " + str(generacion_counter))
for elemento in generacion:
    print(elemento.genes)
    print(elemento.accuracy)

generacion.sort(key=lambda x: x.accuracy, reverse=True)

print("\n--------------------------------------------------------------------------------")
print("Mejor solucion en la generacion final:")
print(generacion[0].genes)
print("Ganancia:" + str(generacion[0].accuracy))

# -------------------------------------------------------------------------------------------
# for i in range(generaciones)
# lista_ordenada = sorted(generacion, key=lambda x: x.ganancia, reverse=True)
# for elemento in lista_ordenada:
# print(f"{elemento.genes}, peso = {elemento.peso}, ganancia = {elemento.ganancia}")
