from sys import thread_info
import threading
import numpy as np
import math
from ArrowHandler import ArrowHandler

from Enemies.Skeleton import Skeleton
from Enemies.Slime import Slime
from Enemies.Boss import Boss 
from Enemies.DarkSkeleton import DarkSkeleton
from Enemies.Knight import Knight

from helpers import *
import random
enemyId = 0


def vectorAdded(lst, x, y):
    return [lst[0]+x, lst[1]+y]

def blocksWith1(map, visited, pos, mapInts, typeIsl = 0):
    queue = []
    queue.append(pos)
    result = []
    spawnPoint = -1
    while len(queue) != 0:
        cPos = queue.pop()
        if (cPos[0] <= 1 or cPos[0] >= map.shape[0]-2 or cPos[1] <= 1 or cPos[1] >= map.shape[1]-2):
            continue
        if map[cPos[0]+1][cPos[1]] == 2 or map[cPos[0]-1][cPos[1]] == 2 or map[cPos[0]][cPos[1]+1] == 2 or map[cPos[0]][cPos[1]-1] == 2:
            spawnPoint = 0
        if map[cPos[0]+1][cPos[1]] == 5 or map[cPos[0]-1][cPos[1]] == 5 or map[cPos[0]][cPos[1]+1] == 5 or map[cPos[0]][cPos[1]-1] == 5:
            spawnPoint = 1


        if map[cPos[0]][cPos[1]] == 1 or map[cPos[0]][cPos[1]] == 4 or visited[cPos[0]][cPos[1]]:
            continue

        result.append(cPos)
        visited[cPos[0]][cPos[1]] = True
        mapInts[cPos[0]][cPos[1]] = typeIsl
        if map[cPos[0]+1][cPos[1]] == 3:
            queue.append((cPos[0]+1, cPos[1]))
        if map[cPos[0]-1][cPos[1]] == 3:
            queue.append((cPos[0]-1, cPos[1]))
        if map[cPos[0]][cPos[1]+1] == 3:
            queue.append((cPos[0], cPos[1]+1))
        if map[cPos[0]][cPos[1]-1] == 3:
            queue.append((cPos[0], cPos[1]-1))

    return result, spawnPoint




class EnemyHandler:
    def __init__(self) -> None:
        self.enemies = {}
        self.islands = []
        self.centers = []
        self.bossIsland = []

        self.loadMap("map3.npy")
        print(self.centers)
        #self.takePossibleSpawns()
        self.arrowHandler = ArrowHandler()
        self.lock = threading.Lock()
        self.time = 0
        self.unfreePlaces = []
        self.addEnemy(self.bossIsland, True)

    def takePossibleSpawns(self):
        size = self.map.shape
        #print(size)
        self.spawns = []
        for i in range(size[0]):
            for j in range(size[1]):
                if self.map[i,j] == 3:
                    self.spawns.append((i,j))

    def updateHealth(self, info):
        #print(info)
        with self.lock:
            for i in range(len(info)):
                tl = info[i]
                if not tl["uid"] in self.enemies.keys():
                    continue
                self.enemies[tl["uid"]].health = min(tl["health"], self.enemies[tl["uid"]].health)
                if self.enemies[tl["uid"]].health <= -4 or self.enemies[tl["uid"]].isInBadTile(self.map):
                    del self.enemies[tl["uid"]]
    def takeCenter(self, island):
        center = [0.0, 0.0]
        length = len(island)
        for pos in island:
            center[0] += pos[0]
            center[1] += pos[1]
        center = [center[0]/length, center[1]/length]
        return center


    def loadMap(self, mapName):
        self.map = np.load(mapDir / mapName)
        self.islands = []
        visited = np.zeros(self.map.shape, dtype=bool)
        mapInts = np.zeros(self.map.shape, dtype=int)

        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if not visited[i][j] and self.map[i][j] == 3:
                    islands, spawnPoint = blocksWith1(self.map, visited, [i, j], mapInts, len(self.islands))
                    if spawnPoint == 0:
                        continue
                    if spawnPoint == 1:
                        self.bossIsland = islands
                        continue
                    self.islands.append(islands)
                    if len(self.islands[-1]) < 50:
                        self.islands = self.islands[:-1]
                    else:
                        self.centers.append(self.takeCenter(self.islands[-1]))
        self.mapInts = mapInts
        print(self.map.shape)

    def addEnemy(self, island, isBoss=False):
        global enemyId
        pos = island[random.randint(0, len(island)-1)]
        pos = [pos[0]*block_width/100, pos[1]*block_height/100]
        typeEnemy = random.randint(0,12)
        if isBoss:
            print("boss made")
            self.enemies[str(enemyId)] = Boss(pos, str(enemyId), 100)
            self.bossId = str(enemyId)
            print(self.enemies[str(enemyId)].enemyType)
            print("####")
        elif typeEnemy < 5:
            self.enemies[str(enemyId)] = Skeleton(pos, str(enemyId), 100)
        elif typeEnemy < 9:
            self.enemies[str(enemyId)] = Slime(pos, str(enemyId), 100)
        elif typeEnemy < 11:
            self.enemies[str(enemyId)] = DarkSkeleton(pos, str(enemyId), 100)
        else:
            self.enemies[str(enemyId)] = Knight(pos, str(enemyId), 100)



        enemyId += 1

    def updateArrows(self, dt, players):
        self.arrowHandler.update(dt, players, self.map, self.enemies)

    def checkCollision(self, rect):
        pIndx = (rect[0]*100)/block_width, (rect[1]*100)/block_height
        return self.map[int(pIndx[0])][int(pIndx[1])] == 1 or self.map[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] == 1

    def generation(self, island, isBoss = False):
        nEnemies = int(len(island)/120) if not isBoss else 2
        for _ in range(nEnemies):
            self.addEnemy(island)

    def checkIfNeedGeneration(self, players):
        if self.bossId in self.enemies.keys() and self.enemies[self.bossId].needSpawn:
            self.generation(self.bossIsland, True)
            self.enemies[self.bossId].needSpawn = False

        for player in players.values():
            for i in range(len(self.centers)):
                pos = self.centers[i]
                transPos = [player.pos[0]*100/block_width, player.pos[1]*100/block_height]
                dist = math.sqrt((transPos[0]-pos[0])**2 + (transPos[1]-pos[1])**2)
                if dist < 30 and len(self.islands[i]) > 1:
                    self.unfreePlaces.append(i)
                    self.generation(self.islands[i])
                    self.islands[i] = []
                    self.centers[i] = [10000000, 10000000]




    def updateEnemies(self, players, dt):
        self.checkIfNeedGeneration(players)
        active_islands = []
        for player in players.values():
            transPos = [player.pos[0]*100/block_width, player.pos[1]*100/block_height]
            player.current_island = int(self.mapInts[int(transPos[0]), int(transPos[1])])
            active_islands.append(player.current_island)

        needCheckIslands = self.unfreePlaces[:]
        for pid, enemy in self.enemies.items():
            pIndx = (enemy.pos[0]*100)/block_width, (enemy.pos[1]*100)/block_height
            needCheckIslands = [x for x  in needCheckIslands if x != self.mapInts[int(pIndx[0]), int(pIndx[1])]]
            if not self.mapInts[int(pIndx[0]), int(pIndx[1])] in active_islands:
                continue
            enemy.update(players, dt, self.map, self.arrowHandler, self.enemies.items())
        for el in needCheckIslands:
            self.unfreePlaces.remove(el)


        self.time += dt

    def getPositions(self, playerPos, max_distance=7):
        is_close = lambda enemy_pos : math.hypot(playerPos[0] - enemy_pos[0], playerPos[1]-enemy_pos[1]) <= max_distance
        return [
            enemy.getInfo()
            for pid, enemy in self.enemies.items()
            if is_close(enemy.pos)
        ]    
    def getArrows(self, playerPos):
        return self.arrowHandler.getInfo(playerPos)

