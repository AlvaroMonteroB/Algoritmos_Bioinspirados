#Benchmark
#Montero Barraza Alvaro David
#6BV1
import numpy as np
import torneo as trn
import elitista

ejecuciones=10


vect_best_turnmt=[]
vect_best_elitsm=[]

for i in range(ejecuciones):
    poblacion=trn.pop(100,200,(5.12,5.12),(-5.12,-5.12),(5,5),2)
    poblacion.genetic_operator()
    fitness,_=poblacion.best_individual()
    vect_best_turnmt.append(fitness)
    
for i in range(ejecuciones):
    poblacion=elitista.pop(100,200,(5.12,5.12),(-5.12,-5.12),(5,5),2)
    poblacion.genetic_operator()
    fitness,_=poblacion.best_individual()
    vect_best_elitsm.append(fitness)
    
    
vect_best_turnmt=np.array(vect_best_turnmt)
vect_best_elitsm=np.array(vect_best_elitsm)

trnmt_desv=np.std(vect_best_turnmt)
elitsm_desv=np.std(vect_best_elitsm)

trnmt_mean=np.mean(vect_best_turnmt)
elitsm_mean=np.mean(vect_best_elitsm)

turnmt_worst=np.amax(vect_best_turnmt)
turnmt_best=np.amin(vect_best_turnmt)

elitsm_worst=np.amax(vect_best_elitsm)
elitsm_best=np.amin(vect_best_elitsm)

print("====================Estadisticas de selección por torneo=====================")
print("Mejor: "+str(turnmt_best))
print("Media: "+str(trnmt_mean))
print("Peor:  "+str(turnmt_worst))
print("Desv:  "+str(trnmt_desv))

print("==================Estadísticas de cruzamiento elitista=======================")
print("Mejor: "+str(elitsm_best))
print("Media: "+str(elitsm_mean))
print("Peor:  "+str(elitsm_worst))
print("Desv:  "+str(elitsm_desv))