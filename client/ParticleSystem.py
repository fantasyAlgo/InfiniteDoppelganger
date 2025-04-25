import random
import pyray as rl
from Settings import *

INIT_PARTICLE_SIZE = 6
LIFETIME = 0.3

class ParticleSystem:
    def __init__(self, lifetime=0.2) -> None:
        self.spawners = []
        self.particles = []
        self.lifetime = lifetime
    def addParticleSpawn(self, pos, time=4):
        pass
    def addParticle(self, pos, dir, scaleA=0.125, baseColor = (125, 125,125,255)):
        #n = random.randint(0,255)
        #scaleA = 0.125
        scaleB = 0.75
        randomize = lambda x,y=0.5 : x-((y/2)-random.randint(0,1000)*(y/1000))
        color = [max(min(int(randomize(baseColor[0], 62)), 255),0), 
                 max(min(int(randomize(baseColor[1], 62)), 255),0), 
                 max(min(int(randomize(baseColor[2], 62)), 255),0), 
                     125]

        self.particles.append(Particle([randomize(pos[0],scaleA), randomize(pos[1], scaleA)], color, [randomize(dir[0],scaleB), randomize(dir[1],scaleB)]))

    def update(self, dt):
        toDelete = []
        for i in range(len(self.particles)):
            particle = self.particles[i]
            particle.update(dt)
            if particle.lifetime > self.lifetime:
                toDelete.append(particle)
        for particle in toDelete:
            self.particles.remove(particle)

    def draw(self, camera):
        for particle in self.particles:
            particle.draw(camera)





class ParticleSpawner:
    def __init__(self, pos, time=2, dir = [0,0,0]) -> None:
        self.particles = []
        self.startTime = 0
        self.pos = pos
        self.endTime = time
        self.dir = dir

    def update(self, dt):
        takeColor = lambda x : (x, x, x, 255)
        if self.startTime < self.endTime:
            self.particles.append(Particle(self.pos, takeColor(random.randint(0,255)), self.dir))
        toDelete = []
        for i in range(len(self.particles)):
            particle = self.particles[i]
            particle.update()
            if particle.lifetime > 0.6:
                toDelete.append(i)
        for index in toDelete:
            toDelete.pop(index)
        self.startTime += dt


class Particle:
    def __init__(self, pos, color, dir) -> None:
        self.pos = pos
        self.color = color
        self.dir = dir
        self.basePos = [pos[0], pos[1]]
        self.lifetime = 0
        self.scale = INIT_PARTICLE_SIZE
    def update(self, dt):
        self.pos = [self.pos[0]+self.dir[0]*dt, self.pos[1]+self.dir[1]*dt]
        self.scale = INIT_PARTICLE_SIZE*(1-self.lifetime/LIFETIME)
        self.lifetime += dt
    def draw(self, camera):
        adjusted_x = int((self.pos[0] - camera[0])*100) + int(width/2)
        adjusted_y = int((self.pos[1] - camera[1])*100) + int(height/2)
        rect = (adjusted_x, adjusted_y, self.scale, self.scale)
        rl.draw_rectangle_rec(rect, self.color)
