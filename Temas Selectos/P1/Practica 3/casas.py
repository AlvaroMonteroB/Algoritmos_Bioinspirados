import math
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy



Pi=3.141592653
P=.9
Pm=.05

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
            real.append(math.floor(self.li[l] +((Xint*(self.ls[l]-self.li[l]))/((2**self.bits[l])-1))))
            

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
        #x_sz=sum(self.bits)
        #y_sz=self.num_pop
        #self.individuals=np.empty((y_sz,x_sz))
        self.individuals=[np.random.randint(2,size=(sum(self.bits))) for i in range(self.num_pop)]
    
    def evaluate_all(self):
        for i in range(len(self.individuals)):
            values=self.decode(i)
                    #Imprimir Individuos codificados y decodificados
           
            print("Individuo "+str(i))
            print("Codificado: "+str(self.individuals[i][0:self.bits[0]])+" Real: "+str(values[0]))
            print("Codificado: "+str(self.individuals[i][self.bits[0]: ])+" Real: "+str(values[1]))
           
        
            print("F("+str(values[0])+","+str(values[1])+")= "+str(self.obj_funct(values)))        
            
                
    
    def obj_funct(self,real):
        x=real[0]
        y=real[1]
        
        sum=self.restrictions(x,y)
        
        
        return math.floor(40000*x+60000*y + sum)
    
    def restrictions(self,x,y):
        sum=0
        g1=x+y-400
        g2=1200-(2*x+4*y)
        g3=(x+y)*.4-x
        if g1 > 0:
            sum+=(g1**2) * 10000
        if g2 > 0:
            sum+=(g2**2) * 10000
        if g3 > 0:
            sum+=(g3**2) * 10000
        return sum
            
            
        
    
    #TODO==============================================
    def parent_selection(self,available):
        integer1=rd.choice(list(available))
        available.remove(integer1)
        return integer1
        
        
        
    
    def best_individual(self):
        rank=[]
        for i,ind in zip(range(len(self.individuals)),self.individuals):
            vars=self.decode(i)
            rank.append((self.obj_funct(vars),ind))
        sorted_rank=sorted(rank,key=lambda x:x[0],reverse=False)
        return sorted_rank[0]
    
    
            
        
    #TODO=============================================
    def genetic_operator(self):
        self.vector=[]
        fitness,_=self.best_individual()
        self.vector.append(fitness)
        for i in range(self.generations):
            #print("Generacion "+str(i))
            #print(f"Poblacion con {num_ind}")
            
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
                #Puntos de cruza
                points = sorted(rd.sample(range(sum(self.bits)), 2))
                p1=points[0]
                p2=points[1]
                if p1>p2:
                    son1=np.concatenate((parent1[0:p2],parent2[p2:p1],parent1[p1:]))
                    son2=np.concatenate((parent2[0:p2],parent1[p2:p1],parent2[p1:]))
                else:
                     son1=np.concatenate((parent1[0:p1],parent2[p1:p2],parent1[p2:]))
                     son2=np.concatenate((parent2[0:p1],parent1[p1:p2],parent2[p2:]))
                #Mutacion
                if rd.uniform(0,1)<=Pm:
                    genmut=rd.randint(0,sum(self.bits)-1)
                    son1[genmut]^=1
                if rd.uniform(0,1)<=Pm:
                    genmut=rd.randint(0,sum(self.bits)-1)
                    son2[genmut]^=1
                prospectos.append(son1)
                prospectos.append(son2) 
                prospectos.append(parent1)
                prospectos.append(parent2)
                fitness_rank=[]   
                for gen in prospectos:
                    vars_=self.decode(gen)
                    fitness_rank.append((gen,self.obj_funct(vars_)))
                fitness_sorted=sorted(fitness_rank,key=lambda x:x[1],reverse=False)#Sorteamos de menor a mayor
                
                    
                    
                
                new_generation.append(fitness_sorted[0][0])
                new_generation.append(fitness_sorted[1][0])
                
            """
            _,individual=self.best_individual()
            if self.num_pop%2==0:
                index=rd.randint(0,self.num_pop-1)
                new_generation[index]=individual
            else:
                new_generation.append(individual)
                                                """
            self.individuals=deepcopy(new_generation)
            #fitness,_=self.best_individual()
            #self.vector.append(fitness)
        #self.vector=np.array(self.vector)
        #self.plot_graph()

if __name__ == "__main__":    
    Poblacion=pop(200,200,(400,400),(0,0),(0,0),2)
    Poblacion.genetic_operator()
    fitness,chrom=Poblacion.best_individual()
    nums=Poblacion.decode(chrom)
    print(f"F({nums[0]},{nums[1]}) = {fitness}")