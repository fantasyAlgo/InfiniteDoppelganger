

from .Enemy import Enemy
from helpers import *

class KnightBoss(Enemy):
    def __init__(self, pos, uid, max_health=100) -> None:
        super().__init__(pos, uid, max_health)
        self.enemyType = 4
        self.health = 80
        self.directFight = False


    def update(self, players, dt, map, arrowHandler, enemies):
        finalDir, playerId, minDistance, dir, faceDir, force = self.getDirection(dt, players, enemies)
        try:
            if minDistance > 8:
                return

            if playerId != -1 and players[playerId].pos[0] < self.pos[0]:
                faceDir = 1
            else:
                faceDir = 0
            if faceDir == -1:
                return 0
            if not self.directFight and minDistance < 2.5:
                self.state = 0
                self.directFight = True
            if self.directFight and minDistance > 2.5:
                self.directFight = False

            if minDistance < 2.5 and self.timeShot > 0.5:
                if self.state/20 <= 6:
                    self.sprite_state = columnPositionKhight(faceDir, int(self.state/20), True, self.health-1)
                #print("bob: ", self.sprite_state)
            else:
                self.sprite_state = columnPositionKhight(faceDir, int(self.state/40), False, self.health-1)

            if arrowHandler.canShoot(self.uid) and self.timeShot > 1:
                if minDistance > 2.5:
                    if faceDir == 1:
                        arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [-1, 1], 5)
                        arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [1, -1], 5)
                    else:
                        arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [1, 1], 5)
                        arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], [-1, -1], 5)
                else:
                    arrowHandler.add(self.uid, [self.pos[0], self.pos[1]], dir, 5.5)
                    self.state = 0

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
        except Exception as e:
            print(e)

