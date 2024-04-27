#Benchmark
#Montero Barraza Alvaro David
#6BV1
import numpy as np

import main

distances = [
    [0, 3091, 927, 1876, 2704, 94, 2999, 1641, 3471, 1838, 3013],
    [3091, 0, 2542, 1681, 375, 2994, 138, 1442, 389, 1407, 290],
    [927, 2542, 0, 1337, 2169, 930, 2464, 1100, 2935, 1168, 2465],
    [1876, 1681, 1337, 0, 1308, 1778, 1603, 240, 2075, 163, 1604],
    [2704, 375, 2169, 1308, 0, 2603, 366, 1069, 767, 1034, 296],
    [94, 2994, 930, 1778, 2603, 0, 2898, 1543, 3369, 1740, 2915],
    [2999, 138, 2464, 1603, 366, 2898, 0, 1364, 531, 1329, 338],
    [1641, 1442, 1100, 240, 1069, 1543, 1364, 0, 1836, 201, 1365],
    [3471, 389, 2935, 2075, 767, 3369, 531, 1836, 0, 1801, 607],
    [1838, 1407, 1168, 163, 1034, 1740, 1329, 201, 1801, 0, 1330],
    [3013, 290, 2465, 1604, 296, 2915, 338, 1365, 607, 1330, 0]
]




ejecuciones=10



vect_best_elitsm=[]

best=[]
param=False
for i in range(ejecuciones):
    poblacion=main.pop(20,distances)
    if i==ejecuciones-1:
        param=True
    poblacion.genetic_operator(25,param)
    _,fitness=poblacion.best_route()
    vect_best_elitsm.append(fitness)
    if i+1==ejecuciones:
        print(f'Individuo {_}\n')
        poblacion.evaluate_best(_)
    
    

vect_best_elitsm=np.array(vect_best_elitsm)


elitsm_desv=np.std(vect_best_elitsm)


elitsm_mean=np.mean(vect_best_elitsm)



elitsm_worst=np.amax(vect_best_elitsm)
elitsm_best=np.amin(vect_best_elitsm)

print('\n\n')
print("==================Estadísticas de optimización de agente viajero=======================")
print("Mejor: "+str(elitsm_best))
print("Media: "+str(elitsm_mean))
print("Peor:  "+str(elitsm_worst))
print("Desv:  "+str(elitsm_desv))