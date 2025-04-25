from helpers import *

class Enemy:
    def __init__(self, pos, uid, max_health=100) -> None:
        self.pos = pos
        self.uid = uid
        self.sprite_state = (0, 0, 48, 48)
        self.state = 0
        self.health = max_health 
        self.timeShot = 0
        self.randomDir = [0.0,0.0]
        self.timeStill = 0.0
        self.enemyType = 0
        self.playerDir = [0.0, 0.0]

        self.prevPlayerPos = [-0.0, 0.0]
        self.idTargetPlayer = 0
        self.havePrevPos = False
        self.isInvincible = False
    def isInBadTile(self, map):
        rect = self.pos
        pIndx = (rect[0]*100)/block_width, (rect[1]*100)/block_height
        if pIndx[0] <= 0 or pIndx[0] > map.shape[0] or pIndx[1] <= 0 or pIndx[1] > map.shape[1] or map[int(pIndx[0])][int(pIndx[1])] == 0:
            return True

    def checkCollision(self, rect, map):
        fakeRect = rect
        if self.enemyType == 1:
            fakeRect = [rect[0], rect[1]]

        pIndx = (fakeRect[0]*100)/block_width, (fakeRect[1]*100)/block_height
        if pIndx[0] <= 0 or pIndx[0] > map.shape[0] or pIndx[1] <= 0 or pIndx[1] > map.shape[1]:
            return True
        if self.enemyType == 1:
            return map[int(pIndx[0])][int(pIndx[1])] in [1,4,5,6]
        return map[int(pIndx[0])][int(pIndx[1])] in [1,4,5,6] or map[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] in [1,4,5,6]

    def totalForce(self, enemies):
        force = [0.0,0.0]
        for pid, enemy in enemies:
            dirX = self.pos[0] - enemy.pos[0]
            dirY = self.pos[1] - enemy.pos[1]
            distance = abs(distanceV(self.pos, enemy.pos))
            if distance != 0 and distance < 10:
                force[0] += 0.2*dirX/distance
                force[1] += 0.2*dirY/distance
        return force
    def getDirection(self, dt, players, enemies):
        self.timeShot += dt
        self.timeStill += dt

        minPos = [0, 0]
        minDistance = 1000000000
        playerId = 0
        for player in players.values():
            pos = player.pos
            dist = math.sqrt((self.pos[0]-pos[0])**2 + (self.pos[1]-pos[1])**2) 
            if dist < minDistance:
                minDistance = dist
                minPos = pos
                playerId = player.uid
        if playerId != self.idTargetPlayer:
            self.havePrevPos = False

        minDistance = minDistance if minDistance != 0 else 0.001

        predPos = minPos
        predDist = minDistance
        if self.enemyType != 1 and self.havePrevPos:
            howMuch = 70
            predPos = [(howMuch+1)*minPos[0] - howMuch*self.prevPlayerPos[0], (howMuch+1)*minPos[1] - howMuch*self.prevPlayerPos[1]]
            predDist = math.sqrt((self.pos[0]-predPos[0])**2 + (self.pos[1]-predPos[1])**2) 


        self.prevPlayerPos = minPos
        self.havePrevPos = True
        self.idTargetPlayer = playerId

        minPos = predPos
        dirX = -self.pos[0]+minPos[0]
        dirY = -self.pos[1]+minPos[1]
        fakeDir = [-self.pos[0] + self.prevPlayerPos[0], -self.pos[1] + self.prevPlayerPos[1]]


        dir = 0 if abs(dirY) > abs(dirX) else 1
        if dir == 0:
            dir = 0 if dirY < 0 else 2
        else:
            dir = 1 if dirX > 0 else 3

        self.state += dt*100
        if (self.health <= 0):
            if self.health == 0:
                self.state = 0
                self.health -= 2
            if self.state >= 160:
                self.health = -100
            return 0, -1, 0, [0,0], -1, [0,0]



        '''self.randomDir = [self.randomDir[0]*0.9999, self.randomDir[1]*0.9999]
        if random.randint(0,100)/100 > 0.7 and abs(self.randomDir[0]) < 0.001 and abs(self.randomDir[1]) < 0.001:
            self.randomDir = [2 - random.randint(0,100)/25, 2 - random.randint(0,100)/25]'''
        self.randomDir = [0,0]
        self.playerDir = [fakeDir[0]/minDistance, fakeDir[1]/minDistance]
        finalDir = [dt*((dirX/predDist)+self.randomDir[0]), dt*(dirY/predDist + self.randomDir[1])]
        force = self.totalForce(enemies)
        #force = [0,0] # just a test to see the removal of the "don't go near your friends idiot" force
        #finalDir = [finalDir[0]+force[0]*dt, finalDir[1] + force[1]*dt]

        return finalDir, playerId, minDistance, [dirX/predDist, dirY/predDist], dir, force

    def getInfo(self):
        return {"uid" : self.uid, 
                "x" : round(self.pos[0],2), 
                "y" : round(self.pos[1],2), "column" : self.sprite_state, "health" : self.health, "enemyType" : self.enemyType, 
                "dir" : [round(self.playerDir[0],2), round(self.playerDir[1], 2)]}
    def checkArrows(self):
        pass




