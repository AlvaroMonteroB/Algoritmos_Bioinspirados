import math
import random as rd
import numpy as np
import matplotlib.pyplot as plt

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
        for j in range(len(self.bits)):
            gen.append(self.individuals[i][aux:self.bits[j]+aux])
            aux+=self.bits[j]
        Xint=0
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
        self
        integer1=rd.randint(0,self.num_pop)
        integer2=rd.randint(0,self.num_pop)
        while integer1==integer2:
            integer2=rd.randint(0,self.num_pop)
        
        champ1=self.decode(integer1)#Champ es una lista con variables x,y
        champ2=self.decode(integer2)
        if self.obj_funct(champ1)>self.obj_funct(champ2):
            return integer1
        else:
            return integer2
        
    
    def genetic_operator(self):
        self.vector=[]
        for i in range(self.generations):
            print("Generacion "+str(i))
            new_generation=[]
            for j in range(self.num_pop/2):
                while True:
                    ind1=self.parent_selection()#Indice de los padres
                    ind2=self.parent_selection()
                    while ind1==ind2:
                        ind2=self.parent_selection()
                    parent1=self.individuals[ind1]
                    parent2=self.individuals[ind2]
                    if rd.uniform(0,1)>P:#Si es mayor no se cruzan
                        new_generation.append(parent1)
                        new_generation.append(parent2)
                        break
                    #Puntos de cruza
                    p1=rd.randint(0,sum(self.bits))
                    p2=rd.randint(0,sum(self.bits))
                    while p1==p2:
                        p2=rd.randint(0,sum(self.bits))
                    if p1>p2:
                        son1=np.concatenate((parent1[0:p2],parent2[p2:p1],parent1[p1:]))
                        son2=np.concatenate((parent2[0:p2],parent1[p2:p1],parent2[p1:]))
                    else:
                         son1=np.concatenate((parent1[0:p1],parent2[p1:p2],parent1[p2:]))
                         son2=np.concatenate((parent2[0:p1],parent1[p1:p2],parent2[p2:]))
                    #Mutacion
                    if rd.uniform()<=Pm:
                        genmut=rd.randint(0,sum(self.bits))
                        son1[genmut]=np.bitwise_xor(son1[genmut],1)
                    if rd.uniform()<=Pm:
                        genmut=rd.randint(0,sum(self.bits))
                        son2[genmut]=np.bitwise_xor(son2[genmut],1)
        
        
        
        
        
        
        self.vector=np.array(self.vector)
        self.plot_graph()
    
    
    
    
    
    
    
#Se tienen que poner juntos los limites superiores e inferiores, en la misma tupla
Poblacion=pop(5,10,(2,2),(-2,-2),(2,2),2)
Poblacion.evaluate_all()