#
#Montero Barraza Alvaro David
#Algoritmos Bioinspirados
#5BV1
import random
import math

def worker_cycle(worker_list):
    min_value = 0
    best_bee = []

    for i in range(len(worker_list)):
        while True:
            k = random.randint(0, len(worker_list) - 1)
            if k != i:
                break

        j = random.randint(0, 1)
        new_coordinates = worker_list[i][0]
        new_coordinates[j] = worker_list[i][0][j] + (random.uniform(-1, 1) * (worker_list[i][0][j] - worker_list[k][0][j]))

        if new_coordinates[j] > 5:
            new_coordinates[j] = 5
        if new_coordinates[j] < -5:
            new_coordinates[j] = -5

        fit = evaluation(new_coordinates)

        if fit < worker_list[i][1]:
            worker_list[i][0] = new_coordinates
            worker_list[i][1] = fit
            worker_list[i][2] = 0
        else:
            worker_list[i][2] += 1
            if worker_list[i][2] == 5:
                worker_list[i] = explorer_cycle(worker_list[i])

        if worker_list[i][1] < min_value:
            best_bee = worker_list[i]

        print(f"Abeja: {i + 1}  Fuente: {worker_list[i][0]}")
    print()
    return best_bee

def explorer_cycle(bee):
    new_list = []

    if bee[2] >= 5:
        bee = []
        for i in range(2):
            r = random.uniform(0, 1)
            new_list.append(lim_inf + r * (lim_sup - lim_inf))
        
        bee.append(new_list)
        val = evaluation(new_list)
        bee.append(val)
        bee.append(0)
    return bee

def observer_cycle(worker_list):
    sum_value = 0
    min_value = 999
    best_bee = []
    probabilities = []

    for i in range(len(worker_list)):
        if worker_list[i][1] < 0:
            sum_value += 1 + abs(worker_list[i][1])
            
        else:
            sum_value += (1 / (1 + worker_list[i][1]))
    #print(sum_value+"\n")

    for i in range(len(worker_list)):
        if worker_list[i][1] < 0:
            probabilities.append((1 + abs(worker_list[i][1])) / sum_value)
        else:
            probabilities.append((1 / (1 + worker_list[i][1])) / sum_value)

    for i in range(len(worker_list)):
        accumulated = 0
        x = random.uniform(0, 1)

        for j in range(len(probabilities)):
            accumulated += probabilities[j]

            if x <= accumulated:
                while True:
                    k = random.randint(0, len(worker_list) - 1)
                    if k != i:
                        break

                a = random.randint(0, 1)
                new_coordinates = worker_list[i][0]
                new_coordinates[a] = worker_list[i][0][a] + (random.uniform(-1, 1) * (worker_list[i][0][a] - worker_list[k][0][a]))

                if new_coordinates[a] > 5:
                    new_coordinates[a] = 5
                if new_coordinates[a] < -5:
                    new_coordinates[a] = -5

                fit = evaluation(new_coordinates)

                if fit < worker_list[i][1]:
                    if fit < min_value:
                        min_value = fit
                        best_bee = [new_coordinates, fit]
                else:
                    if worker_list[i][1] < min_value:
                        best_bee = worker_list[i]
                        min_value = worker_list[i][1]

    return best_bee

def evaluation(bee):
    x = bee[0]
    y = bee[1]
    return (x ** 2) + (y ** 2) + (25 * (math.sin(x) + math.sin(y)))


#Aqui empieza

lim_inf,lim_sup,workers,observers,limit,cycles=[-5,5,20,20,5,50]

worker_list = []
#Declaracion de abejas
for i in range(workers):
    bee = []
    for j in range(2):
        r = random.uniform(0, 1)
        bee.append(lim_inf + r * (lim_sup - lim_inf))
    eva = evaluation(bee)
    worker_list.append([bee, eva, 0])


best_bee = []

for i in range(cycles):
    #print("Ciclo "+i)
    #Ciclo de abejas trabajadoras
    worker = worker_cycle(worker_list)
    
    #Ciclo de observadoras
    observer = observer_cycle(worker_list)

    if observer[1] < worker[1]:
        best_bee = observer
    else:
        best_bee = worker
    #print(f"best_bee"")

print("---")
print(f"Best bee found: {best_bee}")