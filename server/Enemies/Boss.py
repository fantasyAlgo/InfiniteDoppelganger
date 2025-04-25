from .Enemy import Enemy
from helpers import *
import math

class Boss(Enemy):
    def __init__(self, pos, uid, max_health=100) -> None:
        super().__init__(pos, uid, max_health)
        self.enemyType = 2
        self.phase = 0
        self.needSpawn = False
        self.turnAttack = 0


    def update(self, players, dt, map, arrowHandler, enemies):
        finalDir, playerId, minDistance, dir, faceDir, force = self.getDirection(dt, players, enemies)
        if (self.phase == 0 and self.health < 80) or (self.phase == 1 and self.health < 10):
            self.phase += 1
            self.needSpawn = True

        if minDistance > 8:
            return

        self.sprite_state = columnPositionEnemy(faceDir, int(self.state/40), False, self.health-1)
        if faceDir == -1:
            return 0
        if self.health < 60 and self.turnAttack > 2.0:
            for i in range(0, 360, 30):
                angle = (2*math.pi * i)/360
                arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [math.cos(angle), math.sin(angle)], 2)
            self.turnAttack = 0



        if arrowHandler.canShoot(self.uid) and self.timeShot > 0.2:
            arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [dir[0], dir[1]], 2)
            self.timeShot = 0

        if minDistance < 1.2:
            finalDir = [-finalDir[0], -finalDir[1]]

        
        finalDir = [finalDir[0]+ 0.5*force[0]*dt, finalDir[1] + 0.5*force[1]*dt]

        newPos = [self.pos[0]+finalDir[0], self.pos[1]+finalDir[1]]
        if not self.checkCollision([self.pos[0], newPos[1]], map):
            #self.pos[0] += dt*dirX/minDistance
            self.pos[1] += 0.75*finalDir[1]
        if not self.checkCollision([newPos[0], self.pos[1]], map):
            self.pos[0] += 0.75*finalDir[0]
            #self.pos[1] += dt*dirY/minDistance
        self.turnAttack += dt

