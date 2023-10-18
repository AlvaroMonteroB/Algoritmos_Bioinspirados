import random as rd
from copy import deepcopy
P=.80#Probabilidad


dict_names={#Name, weight, price, minimum,max
    0:("Decoy Detonators",4,10,0,10),
    1:("Love potion",2,8,3,5),
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
    def __init__(self,num_pop,generations,weight_max,genes) -> None:
        self.individuals=list()
        self.fitness=list()
        self.num_pop=num_pop
        self.generations=generations
        self.weight_max=weight_max
        self.genes=genes
        self.best_chrom=tuple#Mejor cromosoma
        
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
                 
        for i in range(self.genes):
            _,_,_,mmin,mmax=dict_names[i]
            self.min.append(mmin)
            self.max.append(mmax)
        self.best_chrom=self.best_individual()
            
    def roulette(self):#Metodo de ruleta
        prob=rd.uniform(0,1)
        fitness=list()        
        for chrom in self.individuals:
            aux=0
            for gen in chrom:
                aux+=(gen.price * gen.quantity)
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
        
            
                
    def best_individual(self):
        indiv=[]
        for chr in self.individuals:
            fitness=0
            for gen in chr:
                fitness+=gen.quantity*gen.price
            indiv.append((fitness,chr))
        
        sorted_list=sorted(indiv,key=lambda x:x[0],reverse=True)
        return sorted_list[0]
            
                      
                
        
        
        
    def genetic_operator(self):#Operador para reproducir una nueva generacion
        sin_mejora=0
        
        for i in range(self.generations):#Generaciones de nuestro algoritmo
            print("Generacion "+str(i))
            new_generation=[]
            for j in range(int((len(self.individuals))/2)):#Crear 5 parejas
                while True:
                    pair1=self.roulette()
                    pair2=self.roulette()
                    while pair1==pair2:#Si los indices son iguales vamos a aplicar la ruleta hasta que cambien
                        pair2=self.roulette()
                    parent1=self.individuals[pair1]
                    parent2=self.individuals[pair2]
                    band=0
                    if rd.uniform(0,1)>.85:#Si el valor supera .85 no se cruzan
                        new_generation.append(deepcopy(parent1)) #se pasan a la siguiente generacion
                        new_generation.append(deepcopy(parent2))
                        band=1
                        break
                    #hacer cruza, mutacion y escoger los mejores individuos
                    
                    #cruza
                    cont=0
                    prospectos=list() 
                    while True:
                        
                        pos_hijos=[]
                        for k in range(self.genes):#Generar hijo
                            pos_hijos.append(rd.uniform(0,1))

                        for k in range(len(pos_hijos)):
                            aux_chr1=[]
                            aux_chr2=[]
                            if pos_hijos[k]>=.5:#Si es mayor a .5 elegimos padre 2
                                aux_chr1.append(deepcopy(parent2[k]))
                            else:
                                aux_chr1.append(deepcopy(parent1[k]))
                                
                            if pos_hijos[k]>=.5:#El hermano es el complemento
                                aux_chr2.append(deepcopy(parent1[k]))
                            else:
                                aux_chr2.append(deepcopy(parent2[k]))
                                
                            #Mutacion    
                        for mut in range(len(aux_chr1)):
                            if rd.uniform(0,1)<.1:#Si es menor a .1 mutamos
                                aux_chr1[mut].quantity=rd.randint(self.min[mut],self.max[mut])
                        for mut in range(len(aux_chr2)):
                            if rd.uniform(0,1)<.1:
                                aux_chr2[mut].quantity=rd.randint(self.min[mut],self.max[mut])
                                        
                           #Checar condicion de peso    
                        if chr_weight(aux_chr1)>self.weight_max and chr_weight(aux_chr2)>self.weight_max:#SI no se cumple la condicion de peso se vuelve a generar
                            continue#SI no cumple volvemos a generar
                        elif 0<chr_weight(aux_chr1)<=self.weight_max and 0<chr_weight(aux_chr2)<=self.weight_max :#si cumple vamos a ponerlo en los hijos
                            prospectos.append(deepcopy(aux_chr1))
                            prospectos.append(deepcopy(aux_chr2))
                            break
                        
                    prospectos.append(parent1)
                    prospectos.append(parent2)
                    

                    fitness_rank=[]#Vamos a rankear los mejores individuos
                    for f in prospectos:#f es cada cromosoma
                        weight_aux=chr_weight(f)
                        aux=0
                        for g in f:#Iterar en genes para sacar el fintess
                            aux+=g.price*g.quantity
                        fitness_rank.append((aux,f)) #Hacemos el fitness y el cromosoma
                if band==1:
                    continue
                fitness_sorted=sorted(fitness_rank,key=lambda x:x[0],reverse=True)#Sorteamos la lista de mayor a menor
                new_generation.append(deepcopy(fitness_sorted[0][1]))#Pasan los 2 mejores individuos
                new_generation.append(deepcopy(fitness_sorted[1][1]))

            self.individuals=new_generation.copy()#Formamos la nueva generacion 
            fitness_gen,generation_best=self.best_individual()
            if i<2:
                print("Generacion "+str(i))
                for m in self.individuals:
                    for n in m:
                        print(str(n.quantity))
                    print("\n")
            
            
            
            
            if fitness_gen>self.best_chrom[0]:
                self.best_chrom=(fitness_gen,generation_best)
                sin_mejora=0
            else:
                sin_mejora+=1
            if sin_mejora>5:
                break
            
                       
            
            
                
  
            
                

Poblacion=Pop(10,50,30,7)
Poblacion.pop_init()   
Poblacion.genetic_operator()
_,chrom=Poblacion.best_chrom
val=0
for gen in chrom:
    print(gen.name + " "+str(gen.quantity))
    val+=gen.price*gen.quantity
print("Con peso de "+str(chr_weight(chrom)))    
print("COn ganancia de "+ str(val))
    
    
            
            
            
        
        