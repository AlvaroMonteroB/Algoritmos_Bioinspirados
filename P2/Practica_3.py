import math
import random

def funct(x, y):
    return x**2 + y**2 + 25 * (math.sin(x) + math.sin(y))

class Particle:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.pbest = self.pos.copy()

def update_velocity(particle, gbest, a, b1, b2):#Actualización de velocidad
    r1, r2 = random.uniform(0, 1), random.uniform(0, 1)

    inercia = [a * v for v in particle.vel]
    atraccion_local = [b1 * r1 * (pb - pos) for pb, pos in zip(particle.pbest, particle.pos)]#Atracción en terminos del best de la particula
    atraccion_global = [b2 * r2 * (gb - pos) for gb, pos in zip(gbest, particle.pos)]#Atraccion global

    new_vel = [v + local + global_ for v, local, global_ in zip(inercia, atraccion_local, atraccion_global)]

    return new_vel

def enjambre(iterations, num_particles, a, b1, b2):
    particles = [Particle(random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(num_particles)]#Poblacion en posiciones iniciales
    gbest = min(particles, key=lambda p: funct(*p.pos)).pos

    for iteration in range(iterations):
        print(f"Iteration {iteration + 1}:")
        for i, particle in enumerate(particles):
            vel = update_velocity(particle, gbest, a, b1, b2)

            
            particle.pos = [pos + vel for pos, vel in zip(particle.pos, vel)]

            #act particle best
            if funct(*particle.pos) < funct(*particle.pbest):
                particle.pbest = particle.pos.copy()

            # act global best
            if funct(*particle.pos) < funct(*gbest):
                gbest = particle.pos.copy()

            print(f"Particula {i + 1}:")
            print(f"  Posicion: {particle.pos}")
            print(f"  Velocidad: {vel}")
            print(f"  pbest: {particle.pbest}")
            print(f"  gbest: {gbest}") #Mejor posición
            print()
    print(f"Evaluacion de la funcion {funct(particle.pos[0],particle.pos[1])}")


enjambre(iterations=50, num_particles=20, a=0.8, b1=0.7, b2=1)