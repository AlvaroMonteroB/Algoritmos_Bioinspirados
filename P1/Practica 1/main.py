import random as rd
P=.80#Probabilidad


dict_names={#Name, weight, price, minimum,max
    0:("Decoy Detonators",4,10,0,5),
    1:("Love potion",4,8,3,5),
    2:("Extendable Ears",5,12,0,5),
    3:("Skiving Snackbox",5,6,2,5),
    4:("Fever Fudge",2,3,0,10),
    5:("Puking Pastilles",1.5,2,0,5),
    6:("Nosebleed Nougat",1,2,0,5)
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
                    print("self.individuals[0]= "+str(len(self.individuals[0]))+" si es "+str(len(aux_chromosome)))
                #En cualquier caso vamos a limpiar el cromosoma auxiliar para reescribirlo       
                
                
        if self.individuals:
            print("Si hay "+str(len(self.individuals[0])))
        for cr in self.individuals:#cromosomas
            for gen in cr:#Genes en cromosomas
                       print(gen.name+" "+str(gen.quantity))
        for i in range(7):
            _,_,_,mmin,mmax=dict_names[i]
            self.min.append(mmin)
            self.max.append(mmax)
                
  
            
                

Poblacion=Pop(10,50,30)
Poblacion.pop_init()         
            
            
            
        
        