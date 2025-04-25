from .Enemy import Enemy
from helpers import *

class Slime(Enemy):
    def __init__(self, pos, uid, max_health=100) -> None:
        super().__init__(pos, uid, max_health)
        self.stayStill = 0
        self.enemyType = 1
        self.jumpDirection = [-10000, -10000]
        self.attackTime = 0


    def update(self, players, dt, map, arrowHandler, enemies):
        finalDir, playerId, minDistance, dir, faceDir, force = self.getDirection(dt, players, enemies)
        #finalDir = [finalDir[0]+force[0]*dt, finalDir[1] + force[1]*dt]
        if minDistance > 8:
            return

        self.sprite_state = columnPositionEnemy(faceDir, int(self.state/20), False, self.health-1)
        if faceDir == -1:
            return 0
        self.stayStill += dt*100
        if minDistance < 0.5 and self.stayStill >= 240 and self.attackTime > 1:
            players[playerId].health -= 30
            self.attackTime = 0.0
        self.attackTime += dt

        if self.stayStill <= 120:
            self.state = 0
            self.playerDir = [0.0, 0.0]
            return 0

        if self.jumpDirection[0] != -10001:
            if abs(minDistance) < -5.0:
                self.jumpDirection = [-finalDir[0], -finalDir[1]]
            else:
                self.jumpDirection = finalDir
            self.jumpDirection = [self.jumpDirection[0]*2.0, self.jumpDirection[1]*2.0]

        if self.stayStill >= 240:
            self.stayStill = 0.0
            for i in range(0, 360, 90):
                angle = (2*math.pi * i)/360
                arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [math.cos(angle), math.sin(angle)], 2)
            self.turnAttack = 0

            self.jumpDirection = [-10000, -10000]
            return 0


        newPos = [self.pos[0]+self.jumpDirection[0], self.pos[1]+self.jumpDirection[1]]
        if not self.checkCollision([self.pos[0], newPos[1]], map):
            #self.pos[0] += dt*dirX/minDistance
            self.pos[1] += 0.75*self.jumpDirection[1]
        if not self.checkCollision([newPos[0], self.pos[1]], map):
            self.pos[0] += 0.75*self.jumpDirection[0]
            #self.pos[1] += dt*dirY/minDistance

