#
#Montero Barraza Alvaro David
#Algoritmos Bioinspirados
#5BV1
import random
import math

#Función que ejecuta el ciclo de búsqueda de alimentos por las abejas obreras
def ciclo_obrera(lista_workers):
    min = 0  #Valor mínimo inicial para comparación
    best_abeja = []
    #Iteración sobre abejas trabajadoras
    for i in range(len(lista_workers)):  
        #Selecciona una abeja diferente de la lista
        while True:  
            k = random.randint(0, len(lista_workers) - 1)
            if k != i:
                break
        #Selecciona coordenada x o y aleatoriamente
        j = random.randint(0, 1)  
        #Posición actual de la abeja
        nuevas_coor = lista_workers[i][0]  
        nuevas_coor[j] = lista_workers[i][0][j] + (random.uniform(-1, 1) * (lista_workers[i][0][j] - lista_workers[k][0][j]))
        #Verifica límites del espacio de búsqueda
        if nuevas_coor[j] > 5:
            nuevas_coor[j] = 5
        if nuevas_coor[j] < -5:
            nuevas_coor[j] = -5
        #Evalúa la nueva posición
        fit = evaluacion(nuevas_coor)  

        #Compara la nueva posición con la actual, actualiza si es mejor
        if fit < lista_workers[i][1]:
            lista_workers[i][0] = nuevas_coor
            lista_workers[i][1] = fit
            lista_workers[i][2] = 0
        else:
            lista_workers[i][2] += 1
            #Si no mejora en 5 ciclos, se convierte en exploradora
            if lista_workers[i][2] == 5:  
                lista_workers[i] = ciclo_exploradora(lista_workers[i])
        #Actualiza la mejor abeja encontrada
        if lista_workers[i][1] < min:  
            best_abeja = lista_workers[i]

        #Imprime información de la abeja en cada ciclo
        print(f"Abeja: {i + 1}  Fuente de comida: {lista_workers[i][0]}")
    print()
    #Devuelve la mejor abeja encontrada en esta iteración
    return best_abeja  

#Función que realiza el ciclo de búsqueda de alimentos por las abejas exploradoras
def ciclo_exploradora(abeja):
    lista = []
    #Verifica si la abeja ha agotado sus intentos y no ha mejorado
    if abeja[2] >= 5:  
        abeja = [] 
        #Se generan nuevas coordenadas aleatorias
        for i in range(2):  
            r = random.uniform(0, 1)
            lista.append(lim_inf + r * (lim_sup - lim_inf))
        #Se crean y evaluan las nuevas coordenadas
        abeja.append(lista)  
        val = evaluacion(lista)  
        abeja.append(val)  
        abeja.append(0)  
    return abeja

#Función que ejecuta el ciclo de búsqueda de alimentos por las abejas observadoras
def ciclo_observadora(lista_workers):
    #Inicializamos variable para sumatoria y un min para la comparacion
    sumatoria = 0
    min = 999  
    best_abeja = []
    probabilidades = []  
    #Calcula la sumatoria para las probabilidades de selección
    for i in range(len(lista_workers)):
        if lista_workers[i][1] < 0:
            sumatoria += 1 + abs(lista_workers[i][1])
        else:
            sumatoria += (1 / (1 + lista_workers[i][1]))

    #Calcula las probabilidades de selección de las abejas
    for i in range(len(lista_workers)):
        if lista_workers[i][1] < 0:
            probabilidades.append((1 + abs(lista_workers[i][1])) / sumatoria)
        else:
            probabilidades.append((1 / (1 + lista_workers[i][1])) / sumatoria)

    #Selección de una abeja para observar según las probabilidades
    for i in range(len(lista_workers)):
        acumulado = 0
        x = random.uniform(0, 1)

        for j in range(len(probabilidades)):
            acumulado += probabilidades[j]

            if x <= acumulado:
                while True:  #Selecciona una abeja diferente de la lista
                    k = random.randint(0, len(lista_workers) - 1)
                    if k != i:
                        break
                #Selecciona coordenada x o y aleatoriamente
                a = random.randint(0, 1)  
                #Posición actual de la abeja
                nuevas_coor = lista_workers[i][0]  
                #Actualiza la posición según la abeja seleccionada
                nuevas_coor[a] = lista_workers[i][0][a] + (random.uniform(-1, 1) * (lista_workers[i][0][a] - lista_workers[k][0][a]))
                #Verifica que se cumplan las restricciones
                if nuevas_coor[a] > 5:
                    nuevas_coor[a] = 5
                if nuevas_coor[a] < -5:
                    nuevas_coor[a] = -5
                #Evaluacion de la nueva posicion
                fit = evaluacion(nuevas_coor) 

                #Compara la nueva posición con la actual y se actualiza si es mejor
                if fit < lista_workers[i][1]:
                    #Actualiza la mejor abeja encontrada por las observadoras
                    if fit < min:  
                        min = fit
                        best_abeja = [nuevas_coor, fit]
                else:
                    if lista_workers[i][1] < min:
                        best_abeja = lista_workers[i]
                        min = lista_workers[i][1]
    #Devuelve la mejor abeja encontrada por las observadoras
    return best_abeja  

#Función de evaluación de la posición de una abeja, esta funcion a evaluar es la misma que en la practica anterior
def evaluacion(abeja):
    x = abeja[0]
    y = abeja[1]
    return (x ** 2) + (y ** 2) + (25 * (math.sin(x) + math.sin(y)))


#Inicializacion de las variables que ocuparemos dentro del algoritmo
lim_inf = -5
lim_sup = 5
workers = 20
observers = 20
limite = 5
ciclos = 50

#Lista que almacena las abejas trabajadoras con sus posiciones y evaluaciones
lista_workers = []
for i in range(workers):
    abeja = [] 
    #Generación de coordenadas aleatorias
    for j in range(2):  
        r = random.uniform(0, 1)
        abeja.append(lim_inf + r * (lim_sup - lim_inf))
    #Evaluaicon de las coordenadas
    eva = evaluacion(abeja)  
    #Agrega la abeja a la lista de trabajadoras con su evaluación
    lista_workers.append([abeja, eva, 0])  

#Busqueda de la mejor abeja a lo largo de los ciclos definidos
#Variable para guardar la mejor abeja global encontrada
mejor_goblal = 999 
#Variable para guardar la mejor abeja encontrada en cada ciclo
mejor_abeja = []  
#Se realiza el ciclo principal del algoritmo
for i in range(ciclos):
    #Realiza el ciclo de las abejas obreras
    obrera = ciclo_obrera(lista_workers)  
    #Realiza el ciclo de las abejas observadoras
    observadora = ciclo_observadora(lista_workers)  
    #Se compara y actualiza la mejor abeja encontrada en cada ciclo
    if observadora[1] < obrera[1]:
        mejor_abeja = observadora
    else:
        mejor_abeja = obrera

#Se imprime la mejor abeja encontrada
print("---")
print(f"Mejor abeja encontrada: {mejor_abeja}")