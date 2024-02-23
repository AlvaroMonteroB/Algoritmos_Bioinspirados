import math
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D

P=.9 #Probabilidad de cruza
Pm=.05 #Probabilidad de mutacion
class pop:
    def __init__(self,num_pop,generations,ls,li,precision,nvar) -> None:
        self.individuals=[]
        self.num_pop=num_pop
        self.generations=generations
        self.nvar=nvar
        self.ls=list()
        self.li=[]
        self.precision=[]
        for i in range(nvar):
            self.ls.append(ls[i])
            
        for i in range(nvar):
            self.li.append(li[i])
            
        for i in range(nvar):
            self.precision.append(precision[i])
            
        self.pop_init()
        


    def decode(self,i):
        gen=[]
        aux=0
        #Dividir bits de ambas variables
        if isinstance(i,np.ndarray):
            for j in range(len(self.bits)):
                gen.append(i[aux:self.bits[j]+aux])
                aux+=self.bits[j]
         
        else:        
            for j in range(len(self.bits)):
                gen.append(self.individuals[i][aux:self.bits[j]+aux])
                aux+=self.bits[j]
        real=[]
        #Binario a entero
        for l in range(self.nvar):#Numero de variables/genes
            Xint=0
            for k in range(len(gen[l])):
                j=-1-k
                Xint+=gen[l][k]*(2**(self.bits[l]+j))
            real.append(self.li[l] +((Xint*(self.ls[l]-self.li[l]))/((2**self.bits[l])-1)))
            
        #Imprimir Individuos codificados y decodificados
        """
        print("Individuo "+str(i))
        print("Codificado: "+str(gen[0])+" Real: "+str(real[0]))
        print("Codificado: "+str(gen[1])+" Real: "+str(real[1]))"""
        return real
        
      
    def plot_graph(self):
        x_=np.arange(len(self.vector))
        plt.plot(x_, self.vector)
        plt.xlabel('Índice')
        plt.ylabel('Valor')
        plt.title('Gráfico de dispersión del vector')
        plt.grid(True)
        plt.show()
        
    def pop_init(self):
        self.bits=[]
        for i in range(self.nvar):
            self.bits.append(int(math.log((self.ls[i]-self.li[i])*10**self.precision[i],2)+.9))
            
        for i in range(self.num_pop):#for para iterar en los individuos
            individual=np.random.randint(2,size=(sum(self.bits)))
            self.individuals.append(individual)
            
    
    def evaluate_all(self):
        for i in range(len(self.individuals)):
            values=self.decode(i)
            print("F("+str(values[0])+","+str(values[1])+")= "+str(self.obj_funct(values)))        
            
                
    
    def obj_funct(self,real):
        x=real[0]
        y=real[1]
        return ((1-x)**2 + (100-y)**2)
    
    
    def parent_selection(self):
        integer1=rd.randint(0,len(self.individuals)-1)
        integer2=rd.randint(0,len(self.individuals)-1)
        while integer1==integer2:
            integer2=rd.randint(0,self.num_pop-1)
        
        champ1=self.decode(integer1)#Champ es una lista con variables x,y
        champ2=self.decode(integer2)
        if self.obj_funct(champ1)>self.obj_funct(champ2):
            return integer1
        else:
            return integer2
        
    
    def best_individual(self):
        rank=[]
        for i,ind in zip(range(len(self.individuals)),self.individuals):
            vars=self.decode(i)
            rank.append((self.obj_funct(vars),ind))
        sorted_rank=sorted(rank,key=lambda x:x[0],reverse=False)
        return sorted_rank[0]
            
        
    
    def genetic_operator(self):
        self.vector=[]
        fitness,_=self.best_individual()
        self.vector.append(fitness)
        for i in range(self.generations):
            print("Generacion "+str(i))
            num_ind=len(self.individuals)
            print(f"Poblacion con {num_ind}")
            new_generation=[]
            for j in range(int(self.num_pop/2)):
                while True:
                    ind1=self.parent_selection()#Indice de los padres
                    ind2=self.parent_selection()
                    while ind1==ind2:
                        ind2=self.parent_selection()
                    parent1=self.individuals[ind1]
                    parent2=self.individuals[ind2]
                    if rd.uniform(0,1)>=P:#Si es mayor no se cruzan
                        new_generation.append(deepcopy(parent1))
                        new_generation.append(deepcopy(parent2))
                        break
                    #Puntos de cruza
                    p1=rd.randint(0,sum(self.bits)-1)
                    p2=rd.randint(0,sum(self.bits)-1)
                    while p1==p2:
                        p2=rd.randint(0,sum(self.bits)-1)
                    if p1>p2:
                        son1=np.concatenate((parent1[0:p2],parent2[p2:p1],parent1[p1:]))
                        son2=np.concatenate((parent2[0:p2],parent1[p2:p1],parent2[p1:]))
                    else:
                         son1=np.concatenate((parent1[0:p1],parent2[p1:p2],parent1[p2:]))
                         son2=np.concatenate((parent2[0:p1],parent1[p1:p2],parent2[p2:]))
                    #Mutacion
                    if rd.uniform(0,1)<=Pm:
                        genmut=rd.randint(0,sum(self.bits)-1)
                        son1[genmut]=np.bitwise_xor(son1[genmut],1)
                    if rd.uniform(0,1)<=Pm:
                        genmut=rd.randint(0,sum(self.bits)-1)
                        son2[genmut]=np.bitwise_xor(son2[genmut],1)
                    new_generation.append((son1))
                    new_generation.append(son2)
                    break
            _,individual=self.best_individual()
            new_generation.append(individual)

            self.individuals=deepcopy(new_generation)
            fitness,_=self.best_individual()
            self.vector.append(fitness)
            
            

        
        
        
        
        self.vector=np.array(self.vector)
        self.plot_graph()
    
    
    
    
    
    
    
#Se tienen que poner juntos los limites superiores e inferiores, en la misma tupla
Poblacion=pop(5,10,(2,2),(-2,-2),(2,2),2)
Poblacion.genetic_operator()
fitness,chrom=Poblacion.best_individual()
nums=Poblacion.decode(chrom)
print(f"F({nums[0]},{nums[1]}) = {fitness}")