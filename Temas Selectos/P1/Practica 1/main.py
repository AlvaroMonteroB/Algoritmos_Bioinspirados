import math
import random as rd
import numpy as np




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
        print("Individuo "+str(i))
        print("Codificado: "+str(gen[0])+" Real: "+str(real[0]))
        print("Codificado: "+str(gen[1])+" Real: "+str(real[1]))
        return real
        
      
        
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
    
    
#Se tienen que poner juntos los limites superiores e inferiores, en la misma tupla
Poblacion=pop(5,10,(2,2),(-2,-2),(2,2),2)
Poblacion.evaluate_all()