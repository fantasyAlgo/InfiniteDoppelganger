import math
from os import wait

from helpers import *


class ArrowHandler:
    def __init__(self) -> None:
        self.arrows = {}

    def add(self, id, enemyPos, dir, foe = 0, ownerId = -1):
        if foe == 0:
            arrow = BasicArrow(enemyPos, dir, 5, False)
        elif foe == 1:
            arrow = BasicArrow(enemyPos, dir, 5, True)
        elif foe == 2:
            arrow = VomitArrow(enemyPos, dir, 5, False)
        elif foe == 3:
            arrow = RotatingArrow(enemyPos, dir, 5, False)
        elif foe == 4:
            arrow = BoomerangArrow(enemyPos, dir, 50, True, ownerId)
        elif foe == 5:
            arrow = CompleteRotationArrow(enemyPos, dir, 5, False)
        elif foe == 5.5:
            arrow = CompleteRotationArrow(enemyPos, dir, 5, False, -1, False)
        else:
            arrow = BasicArrow(enemyPos, dir, 5, False)

        if id in self.arrows.keys():
            self.arrows[id].append(arrow)
        else:
            self.arrows[id] = [arrow]

    def update(self, dt, players, maps, enemies = None):
        toDelete = []
        for pid, arrows in self.arrows.items():
            for i in range(len(arrows)):
                arrow = arrows[i]
                if arrow.update(dt, players, enemies):
                    toDelete.append((pid, i))
                if arrow.isDead:
                    toDelete.append((pid, i))


                #print(maps[int(arrow.pos[0])][int(arrow.pos[1])])
                pIndx = [int(arrow.pos[0]*100/block_width), int(arrow.pos[1]*100/block_height)]
                if (pIndx[0] < 0 or pIndx[0] >= maps.shape[0] or pIndx[1] <= 0 or pIndx[1] >= maps.shape[1]) or (arrow.time > 0.01 and maps[pIndx[0]][pIndx[1]] != 3):
                    toDelete.append((pid, i))

        for id in toDelete:
            if len(self.arrows[id[0]]) > id[1]:
                self.arrows[id[0]].pop(id[1])
            #if id in self.arrows.keys():
            #    del self.arrows[id]

    def getInfo(self, playerPos):
        info = []
        for pid, arrows in self.arrows.items():
            for arrow in arrows:
                if math.dist(arrow.pos, playerPos) < 7:
                    info.append(arrow.getInfo(pid))
        return info
        #return [arrow.getInfo(pid) for pid, arrow in self.arrows.items()]

    def canShoot(self, id):
        #if not id in self.arrows.keys() or self.arrows[id].isDead:
        #    return True
        return True


class GenericArrow:
    arrow_count = 0
    def __init__(self, pos, dir, maxDistance=5, whichFoe=False, ownerId=-1) -> None:
        self.basePos = [pos[0], pos[1]]
        self.baseDir = [dir[0], dir[1]]
        self.pos = pos
        self.dir = dir
        self.maxDistance = maxDistance 
        self.isDead = False
        self.id = GenericArrow.arrow_count
        GenericArrow.arrow_count += 1
        self.time = 0
        self.foe = 0
        self.whichFoe = whichFoe
        self.ownerId = ownerId

    def getInfo(self, pid):
        return {"pid" : pid, 
                "pos" : [round(self.pos[0], 2), round(self.pos[1], 2)], 
                "dir" : [round(self.dir[0], 2), round(self.dir[1], 2)], 
                "foe" : self.foe + int(self.whichFoe), 
                "time" : round(self.time, 3)}

    def checkPlayers(self, players):
        for player in players.values():
            if not player.isInvincible and distanceV(self.pos, player.pos) < 0.3:
                if player.enemyType != 2:
                    player.health -= 10
                else:
                    player.health -= 2 
                return True, player.uid
        return False, -1

    def update(self, dt, players, enemies): 
        self.time += dt
        if self.isDead:
            return
        if math.sqrt((self.pos[0]-self.basePos[0])**2 + (self.pos[1]-self.basePos[1])**2) > self.maxDistance:
            self.isDead = True
        if not self.whichFoe and self.checkPlayers(players)[0]: # If the arrow comes from the enemies
            return True
        if self.whichFoe and self.checkPlayers(enemies)[0]: # If the arrow comes from the player
            return True # Die!!!!!
        self.move(dt, players[self.ownerId].pos if self.ownerId != -1 else None)
        return False


    def move(self, dt, playerPos):
        self.pos = [self.pos[0]+self.dir[0]*dt*2.0, self.pos[1]+self.dir[1]*dt*2.0]



class BasicArrow(GenericArrow):
    def __init__(self, pos, dir, maxDistance=5, whichFoe=False, ownerId=-1) -> None:
        super().__init__(pos, dir, maxDistance, whichFoe, ownerId)
        self.foe = 0
class VomitArrow(GenericArrow):
    def __init__(self, pos, dir, maxDistance=5, whichFoe=False, ownerId=-1) -> None:
        super().__init__(pos, dir, maxDistance, whichFoe, ownerId)
        self.foe = 2

class RotatingArrow(GenericArrow):
    def __init__(self, pos, dir, maxDistance=5, whichFoe=False, ownerId=-1) -> None:
        super().__init__(pos, dir, maxDistance, whichFoe, ownerId)
        self.foe = 4
    def move(self, dt, playerPos):
        self.pos = [self.pos[0]+self.dir[0]*dt*2.0 + math.cos(10*self.time)/300, self.pos[1]+self.dir[1]*dt*2.0 + math.sin(10*self.time)/300]

class BoomerangArrow(GenericArrow):
    def __init__(self, pos, dir, maxDistance=5, whichFoe=False, ownerId=-1) -> None:
        super().__init__(pos, dir, maxDistance, whichFoe, ownerId)
        #self.usedDir = 0
        self.foe = 6
        self.phase = 0
        self.enemiesTaken = []

    def update(self, dt, players, enemies): 
        self.time += dt
        if self.isDead:
            return
        if math.sqrt((self.pos[0]-self.basePos[0])**2 + (self.pos[1]-self.basePos[1])**2) > self.maxDistance:
            self.isDead = True

        r1 = self.checkPlayers(enemies)
        if r1[0]:
            if r1[1] in self.enemiesTaken:
                if enemies[r1[1]].enemyType != 2:
                    enemies[r1[1]].health += 10
                else:
                    enemies[r1[1]].health += 2 
            else:
                self.enemiesTaken.append(r1[1])
                if enemies[r1[1]].enemyType != 2:
                    enemies[r1[1]].health -= 10
                else:
                    enemies[r1[1]].health -= 5 


        if not self.ownerId in players.keys():
            self.isDead = True
            return


        self.move(dt, players[self.ownerId].pos if self.ownerId != -1 else None)
        return False

    def move(self, dt, playerPos):
        df = -2.4*self.time + 1.6
        if df < 0:
            if self.phase == 0:
                self.enemiesTaken = []
            dDir = math.dist(self.pos, playerPos)
            if dDir < 0.2:
                self.isDead = True
            pDir = [(self.pos[0] - playerPos[0])/dDir, (self.pos[1] - playerPos[1])/dDir]
            usedDir = [df*pDir[0], df*pDir[1]]
            self.phase = 1
        else:
            usedDir = [df*self.dir[0], df*self.dir[1]]
        self.pos = [self.pos[0]+usedDir[0]*dt*2.0, self.pos[1]+usedDir[1]*dt*2.0]

class CompleteRotationArrow(GenericArrow):
    def __init__(self, pos, dir, maxDistance=5, whichFoe=False, ownerId=-1, needsSpiral = True) -> None:
        super().__init__(pos, dir, maxDistance, whichFoe, ownerId)
        self.foe = 8
        self.needsSpiral = needsSpiral
    def move(self, dt, playerPos):
        if not self.needsSpiral:
            self.pos = [self.pos[0]+self.dir[0]*dt*2.0, self.pos[1]+self.dir[1]*dt*2.0]
            return

        dist = self.time/2
        self.pos[0] = self.basePos[0] + math.cos(self.baseDir[0]*self.time*4)*dist
        self.pos[1] = self.basePos[1] + math.sin(self.baseDir[1]*self.time*4)*dist
        self.dir = [math.cos(self.baseDir[0]*self.time*4), math.sin(self.baseDir[1]*self.time*4)]


        if self.time > 3:
            self.isDead = False
        #self.pos = [self.pos[0]+self.dir[0]*dt, self.pos[1]+self.dir[1]*dt] 



