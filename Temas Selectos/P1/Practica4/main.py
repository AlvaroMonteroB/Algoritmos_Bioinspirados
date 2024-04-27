#Montero Barraza Alvaro David
#Ingenieria en IA 6BV1
#Agente viajero
import random as rd
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np


P=.9
Pm=.05

cities={0:'New York',1:'Los Angeles',2:'Chicago',3:'Houston',4:'Phoenix',5:'Philadelphia',6:'San Diego',7:'Dallas',8:'San Francisco',9:'Austin',10:'Las Vegas'}

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

class pop:
    def __init__(self,num_pop,dist_matrix) -> None:
        self.num_pop=num_pop
        self.dist_matrix=dist_matrix
        self.pop_init()
        
    def pop_init(self):
        self.num_cities=len(self.dist_matrix)
        self.individuals=[]
        num_range=list(range(0,self.num_cities))
        #print(num_range)
        for i in range( self.num_pop):
                rd.shuffle(num_range)
                self.individuals.append(num_range.copy()) 
                #distance=self.dist_matrix[num_range[0]][num_range[-1]]
                #print('\n\n\n')
                #print(self.evaluate_one(self.individuals[-1]))
                self.heuristic(self.individuals[-1],4) 
                



    def heuristic(self,individual,m):
        #return individual
        output=individual.copy()
        #print(output)
        for i in range(self.num_cities):
            m_nearest=[]
            for j in range(self.num_cities):
                if(i!=j):
                    m_nearest.append([self.dist_matrix[i][j],j]) # Se pone la distancia junto al indice de la ciudad
                    
            m_nearest=sorted(m_nearest,key=lambda x : x[0],reverse=False)#Lista sorteada de vecinos
            m_nearest=m_nearest[:m]#los m vecinos mas cercanso
            nearest_index=rd.randint(0,m-1)#Indice aleatorio para testear
            test_city=m_nearest[nearest_index][1]#Adquirimos el indice de la ciudad en la matriz de distancias
            
            #Estamos en i asi que vamos a testear si la ruta mejora cambiando de lugar el vecino mas cercano
            chrom_index=output.index(test_city)#Sacamos el indice de el vecino mas cercano en nuestro vector actual
            
            aux=deepcopy(output)
            aux2=deepcopy(output)
            
            aux.pop(i)
            aux2.pop(i)
            
            new_index=(chrom_index+1) % self.num_cities
            new_index2=(chrom_index + 1) % self.num_cities
            aux.insert(new_index,output[i])
            aux2.insert(new_index2,output[i])
            
            #print(aux)
            #print(self.evaluate_one(aux))
            rank=[(output,self.evaluate_one(output)) , (aux,self.evaluate_one(aux)), (aux2,self.evaluate_one(aux2))]
            rank=sorted(rank , key = lambda x : x[1], reverse= False)
            output=rank[0][0]
            
        return output
        
    
    def plot_graph(self):
        x_=np.arange(len(self.vector))
        plt.plot(x_, self.vector)
        plt.xlabel('Índice')
        plt.ylabel('Valor')
        plt.title('Gráfico de dispersión del vector')
        plt.grid(True)
        plt.show()        
    
    
                    
    def evaluate_one(self,individual):
        distance=self.dist_matrix[individual[0]][individual[-1]]
        for i in range(self.num_cities-1):
            distance+=self.dist_matrix[individual[i]][individual[i+1]]
        return distance
            
    def evaluate_best(self,individual):
        distance=self.dist_matrix[individual[0]][individual[-1]]
        print(f'Distancia agregada {distance} distancia fin {distance} de {cities[individual[0]]} a {cities[individual[-1]]}')
        #print(distance)
        for i in range(self.num_cities-1):
            aux=self.dist_matrix[individual[i]][individual[i+1]]
            distance+=aux
            print(f'Distancia agregada {aux} distancia fin {distance} de {cities[i]} a {cities[i+1]}')
        return distance
    
    
    
    def best_route(self) :
        indiv_fitness=[]
        for ind in self.individuals:
                indiv_fitness.append((ind.copy(),self.evaluate_one(ind)))
        
        sorted_routes=sorted(indiv_fitness, key=lambda x:x[1],reverse=False)
        return sorted_routes[0]
     
     
    def parent_selection(self,available):
        integer1=rd.choice(list(available))
        available.remove(integer1)
        return integer1     
     
            
    def genetic_operator(self,generations, graph=False):
        
       if graph:
            self.vector=[]
            _,fitness=self.best_route()
            self.vector.append(fitness)
        
       for i in range(generations):
            available_indices = set(range(self.num_pop))
            new_generation=[]
            for j in range(int(self.num_pop/2)):
                prospectos=[]
                ind1=self.parent_selection(available_indices)#Indice de los padres
                ind2=self.parent_selection(available_indices)
                
                parent1=self.individuals[ind1]
                parent2=self.individuals[ind2]
                
                if rd.uniform(0,1)>=P:#Si es mayor no se cruzan
                    new_generation.append(deepcopy(parent1))
                    new_generation.append(deepcopy(parent2))
                    continue
                
                #Edge recombination
                neighbors={}
                for k in range(self.num_cities):
                    neighbors[parent1[k]]=[parent1[(k-1) % self.num_cities], parent1[(k+1) % self.num_cities]]
                    neighbors[parent2[k]]=[parent2[(k-1) % self.num_cities], parent2[(k+1) % self.num_cities]]
                    
                current_node=rd.choice(list(neighbors.keys()))
                son=[current_node]
                
                while len(son)<self.num_cities:
                    neighbors[current_node].sort()
                    min_neighbors=[n for n in neighbors[current_node] if n not in son]
                    if min_neighbors:
                        current_node=min_neighbors[0]
                        son.append(current_node)
                    else:
                        remaining_nodes=[n for n in parent1 if n not in son]
                        current_node = rd.choice(remaining_nodes)
                        son.append(current_node)
                        
                son=self.heuristic(son,4)
                prospectos=[son,parent1,parent2]
                fitness_rank=[]
                for rute in prospectos:
                    fitness_rank.append([rute,self.evaluate_one(rute)])
                fitness_sorted = sorted(fitness_rank,key=lambda x:x[1],reverse=False)
                
                new_generation.append(fitness_sorted[0][0])
                new_generation.append(fitness_sorted[1][0])
            
            self.individuals=deepcopy(new_generation)

            if graph:
                _,fitness=self.best_route()
                self.vector.append(fitness)
       if rd.uniform(0,1)<Pm:    
            index_random=rd.randint(0,self.num_pop)
            rd.shuffle(self.individuals[index_random])
        
       if graph:
            self.vector=np.array(self.vector)
            self.plot_graph()
        

if __name__ == "__main__":   
    poblacion=pop(20,distances)
    poblacion.genetic_operator(20,True)

    ind,fitness=poblacion.best_route()

    print(ind)
    print(fitness)

    print(poblacion.evaluate_best(ind))