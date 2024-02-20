import math
import random as rd
import numpy as np




class pop:
    def __init__(self,num_pop,generations,ls1,li1,ls2,li2,precision1,precision2) -> None:
        self.individuals=[]
        self.num_pop=num_pop
        self.generations=generations
        self.ls1=ls1
        self.li1=li1
        self.ls2=ls2
        self.li2=li2
        self.precision1=precision1
        self.precision2=precision2
        self.pop_init()


    def decode(self,i):
        gen1=self.individuals[i][:self.bits1]
        gen2=self.individuals[i][self.bits1:]
        Xint=0
        Yint=0
        #Binario a entero
        for k in range(len(gen1)):
            j=-1-k
            Xint+=gen1[k]*(2**(self.bits1+j))
        
        Xreal=self.li1+((Xint*(self.ls1-self.li1))/((2**self.bits1)-1))
            
        for k in range(len(gen2)):
            j=-1-k
            Yint+=gen2[k]*(2**(self.bits2+j))
        Yreal=self.li2+((Yint*(self.ls2-self.li2))/((2**self.bits2)-1))
        #Imprimir Individuos codificados y decodificados
        print("Individuo "+str(i))
        print("Codificado: "+str(gen1)+" Real: "+str(Xreal))
        print("Codificado: "+str(gen2)+" Real: "+str(Yreal))
        return (Xreal,Yreal)
        
      
        
    def pop_init(self):
        self.bits1=int(math.log((self.ls1-self.li1)*10**self.precision1,2)+.9)
        self.bits2=int(math.log((self.ls2-self.li2)*10**self.precision2,2)+.9)
        for i in range(self.num_pop):#for para iterar en los individuos
            individual=np.random.randint(2,size=(self.bits1+self.bits2))
            self.individuals.append(individual)
            
    
    def evaluate_all(self):
        for i in range(len(self.individuals)):
            x,y=self.decode(i)
            print("F("+str(x)+","+str(y)+")= "+str(self.obj_funct(x,y)))
            
            
            
    def obj_funct(self,x,y):
        return ((1-x)**2 + (100-y)**2)
    
    
    def parent_selection(self):
        self
    
    
    
Poblacion=pop(5,10,2,-2,2,-2,2,2)
Poblacion.evaluate_all()