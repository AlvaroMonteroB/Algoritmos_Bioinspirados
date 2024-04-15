#Benchmark
#Montero Barraza Alvaro David
#6BV1
import numpy as np

import casas

ejecuciones=10



vect_best_elitsm=[]


for i in range(ejecuciones):
    poblacion=casas.pop(100,200,(400,400),(0,0),(0,0),2)
    poblacion.genetic_operator()
    fitness,_=poblacion.best_individual()
    vect_best_elitsm.append(fitness)
    
    

vect_best_elitsm=np.array(vect_best_elitsm)


elitsm_desv=np.std(vect_best_elitsm)


elitsm_mean=np.mean(vect_best_elitsm)



elitsm_worst=np.amax(vect_best_elitsm)
elitsm_best=np.amin(vect_best_elitsm)


print("==================Estadísticas de optimización de casas=======================")
print("Mejor: "+str(elitsm_best))
print("Media: "+str(elitsm_mean))
print("Peor:  "+str(elitsm_worst))
print("Desv:  "+str(elitsm_desv))