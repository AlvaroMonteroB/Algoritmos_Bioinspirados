import random as rd
from copy import deepcopy
P=.80#Probabilidad


dict_names={#Name, weight, price, minimum,max
    0:("Decoy Detonators",4,10,0,10),
    1:("Love potion",4,8,3,5),
    2:("Extendable Ears",5,12,0,10),
    3:("Skiving Snackbox",5,6,2,10),
    4:("Fever Fudge",2,3,0,10),
    5:("Puking Pastilles",1.5,2,0,10),
    6:("Nosebleed Nougat",1,2,0,10)
}


class Gen:
    def __init__(self,name,price,weight,quantity) -> None:#
        self.name=name
        self.price=price
        self.weight=weight
        self.quantity=quantity
        
        
def chr_weight(chr:list()):
    weight=0
    for ch in chr:
        weight+=ch.quantity*ch.weight
    return weight
    
           
        
class Pop():
    def __init__(self,num_pop,generations,weight_max) -> None:
        self.individuals=list()
        self.fitness=list()
        self.num_pop=num_pop
        self.generations=generations
        self.weight_max=weight_max
        
    def pop_init(self):
        self.min=list()
        self.max=list()
        min,max=0,0
        for g in range(self.num_pop):#For para generar individuos
            gen_capacity=31
            
            while gen_capacity>self.weight_max:#Si la capacidad es mas de 30 repetimos 
                aux_chromosome=list()
                for i in range(7):
                    name,weight,price,min_val,max_val=dict_names[i]
                    quantity=rd.randint(min_val,max_val)
                    aux_gen=Gen(name,price,weight,quantity)
                    aux_chromosome.append(aux_gen)#vector de genes
                    #Calculamos el peso de los 7 genes del cromosoma
                    
                gen_capacity=chr_weight(aux_chromosome) #Peso del cromosoma
                #print(str(gen_capacity)+"\n")
                
                if gen_capacity<=self.weight_max:#Si es menor o igual al maximo hacemos el append del cromosoma
                    #print(str(len(self.individuals))+ " numero de cromosomas")
                    self.individuals.append(aux_chromosome)
                #En cualquier caso vamos a limpiar el cromosoma auxiliar para reescribirlo       
                
                
        for cr in self.individuals:#cromosomas
            print(" peso "+str(chr_weight(cr)))

            
        for i in range(7):
            _,_,_,mmin,mmax=dict_names[i]
            self.min.append(mmin)
            self.max.append(mmax)
            
    def rulette(self):#Metodo de ruleta
        prob=rd.random()
        fitness=list()        
        for chrom in self.individuals:
            aux=0
            for gen in chrom:
                aux+=(gen.price * gen.quantity)
            aux=aux/chr_weight(chrom)
            fitness.append(deepcopy(aux))#Funcion de fitness
        total=sum(fitness)
        separated_prob=[]
        for vals in fitness:#Crear probabilidad para cada cromosoma
            separated_prob.append(vals/total)
        temp=0
        acumulated_prob=[]
        for val in separated_prob:#Crear probabilidad acumulada
            acumulated_prob.append(val+temp)
            temp=acumulated_prob[-1]
        for i in range(len(acumulated_prob)):
            if prob<=acumulated_prob[i]:
                return i
        return
        
            
                
                
                
        
        
        
    def genetic_operator(self):#Operador para reproducir una nueva generacion
        
        for i in range(1):#Generaciones de nuestro algoritmo
            new_generation=[]
            print(str(self.rulette())+" "+str(self.rulette()))
            
            
                
  
            
                

Poblacion=Pop(10,50,30)
Poblacion.pop_init()   
Poblacion.genetic_operator()
            
            
            
        
        