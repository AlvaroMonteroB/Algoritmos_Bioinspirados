import random as rd
P=.80#Probabilidad


dict_names={#Name, weight, price, minimum,max
    0:("Decoy Detonators",4,10,0,10),
    1:("Love potion",4,8,3,10),
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
        
        
        
        
class Pop():
    def __init__(self,num_pop,generations) -> None:
        self.individuals=list()
        self.num_pop=num_pop
        self.generations=generations
        
    def pop_init(self):
        self.min=list()
        self.max=list()
        for g in range(self.num_pop):#For para generar individuos
            for i in range(7):
                name,weight,price,min,max=dict_names[i]
                self.min.append(min)
                self.max.append(max)
                quantity=rd.randint(min,max)
                aux_gen=Gen(name,price,weight,quantity)
                self.individuals.append(aux_gen)
        for a in self.individuals:
            print(a.name+" "+str(a.quantity)+"\n")
                

Poblacion=Pop(10,50)
Poblacion.pop_init()         
            
            
            
        
        