#Benchmark
#Montero Barraza Alvaro David
#6BV1
import numpy as np
import torneo as trn
import elitista




vect_best_turnmt=[]
vect_best_elitsm=[]

for i in range(10):
    poblacion=trn.pop(100,200,(5.12,5.12),(-5.12,-5.12),(5,5),2)
    poblacion.genetic_operator()
    fitness,_=poblacion.best_individual()
    vect_best_turnmt.append(fitness)
    
for i in range(10):
    poblacion=elitista.pop(100,200,(5.12,5.12),(-5.12,-5.12),(5,5),2)
    poblacion.genetic_operator()
    fitness,_=poblacion.best_individual()
    vect_best_elitsm.append(fitness)
    
    
vect_best_turnmt=np.array(vect_best_turnmt)
vect_best_elitsm=np.array(vect_best_elitsm)

trnmt_desv=np.std(vect_best_elitsm)
elitsm_desv=np.std(vect_best_elitsm)

trnmt_mean=np.mean(vect_best_turnmt)
elitsm_mean=np.mean(vect_best_elitsm)
