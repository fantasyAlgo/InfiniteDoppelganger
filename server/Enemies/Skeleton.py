from .Enemy import Enemy
from helpers import *

class Skeleton(Enemy):
    def __init__(self, pos, uid, max_health=100) -> None:
        super().__init__(pos, uid, max_health)
        self.enemyType = 0
        self.sprite_state = columnPositionEnemy(0, int(self.state/40), False, self.health-1)



    def update(self, players, dt, map, arrowHandler, enemies):
        finalDir, playerId, minDistance, dir, faceDir, force = self.getDirection(dt, players, enemies)

        if minDistance > 8:
            return

        self.sprite_state = columnPositionEnemy(faceDir, int(self.state/40), False, self.health-1)
        if faceDir == -1:
            return 0

        if arrowHandler.canShoot(self.uid) and self.timeShot > 1:
            arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [dir[0], dir[1]])
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

