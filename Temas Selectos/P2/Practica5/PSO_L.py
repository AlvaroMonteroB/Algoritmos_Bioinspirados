#Montero Barraza Alvaro David
#Ingenieria en IA
#6BV1
#inteligencia de enjambre


import math
import random


def obj_funct(vals):
    #print(vals)
    x=vals[0]
    y=vals[1]
    z=vals[2]
    
    return x**2+y**2+z**2


class Particle:
    def __init__(self,ls,li):
        self.pos = [random.uniform(li[i],ls[i]) for i in range(len(ls))]#Generamos posiciones en el rango deseado 
        #print(self.pos)
        dj=[ls[i]-li[i] for i in range(len(ls))]
        
        self.vel =[-dj[i]+2*(random.uniform(0,1)*dj[i]) for i in range(len(dj))]#Generamos la velocidad en el rango deseado

        self.pbest = self.pos.copy()#Por ahora este es el best
        self.fpbest= self.evaluate()
        self.evaluate()
        
    def evaluate(self):
        return obj_funct(self.pos)

            
        
    def print_vars(self):
        print(f"Pos {self.pos}, vel {self.vel}")
        
        
    def update_vel(self,inert,c1,c2,xpbest):
        r1,r2 = random.uniform(0,1), random.uniform(0,1)
        
        inercia= [inert * v for v in self.vel]
        
        local_atraction = [c1 * r1 * (pb - pos) for pb,pos in zip(self.pbest,self.pos)]
        global_atraction = [c2 * r2 *(gb - pos) for gb,pos in zip(xpbest,self.pos)]
        new_vel = [v + local + global_ for v,local,global_ in zip(inercia,local_atraction,global_atraction)]
        
        self.vel=new_vel

    def rectify(self,ls,li):
        for i in range(len(ls)):
            if (self.pos[i]<li[i] or self.pos[i]>ls[i]):
                self.pos[i]= li[i] + random.uniform(0,1)*(ls[i]-li[i])
                d=(ls[i]-li[i])
                self.vel[i]=-d + 2*random.uniform(0,1)*d
                
    def update_pbest(self):
        pbest=[]
    
  
        
def enjambre(iterations,num_particles,ls,li,inertia,c1,c2):#Pasamos ls,li ya qur tienen forma [5,5] y [-5,-5] respectivamente
    particles=[Particle(ls,li) for i in range(num_particles)]
    
    #Matriz topológica
    nbh=[]#Vecindario
    for i in range(num_particles):#Actual, siguiente, anterior, Mejor posicion, mejor fitness
        if i==0:
            nbh.append([i,i+1,num_particles-1,particles[i].pos])
        if i==num_particles-1:
            nbh.append([i,0,i-1,particles[i].pos])
        else:
            nbh.append([i,i+1,i-1,particles[i].pos])
            
    
    """for i in particles:
        i.print_vars()"""
    
    #fitnes_part=[[particle.fpbest,particle.pos] for particle in particles]
    
    particle_best= min(particles, key=lambda p: p.fpbest)
    xpbest=particle_best.pos#x position best
    #best_fitness=particle_best.fpbest
    
    for iteration in range(iterations):
        
        for i in (nbh):
            for j in range(3):
                particle=nbh[i]
                particle.update_vel(inertia,c1,c2,nbh[i][3])
                
                particle.pos = [pos + vel for pos,vel in zip(particle.pos,particle.vel)]#Actualizar posicion
                #Xgebest de cada vecindario
                
                #Rectificacion de violaciones
                particle.rectify(ls,li)#Rectificar
                
                
                if obj_funct(particle.pos)<obj_funct(particle.pbest):#Actualizamos el pbest de la particula
                    particle.pbest=particle.pos.copy()
                if obj_funct(particle.pos)<obj_funct(nbh[i][3]):
                    nbh[i][3]=particle.pos.copy()
    
    print(obj_funct(xpbest)) 
    print(xpbest)
    
    
    
    
if __name__ == "__main__":  
    enjambre(100,200,[100,100,100],[-100,-100,-100],.8,.7,.1)