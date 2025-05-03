import pyray as rl
from Settings import *
from ParticleSystem import ParticleSystem
from helpers import dirFromVec, distanceV, normDiff
from textureHandler import TextureHandler
import math
import random

class EnemyHandler:
    def __init__(self) -> None:
        self.enemies = {}
        self.bossUid = None

    def draw(self, camera, particleSystem : ParticleSystem):
        uidsToDelete = []
        for enemy in self.enemies.values():
            enemy.draw(camera, particleSystem)
            if not enemy.used:
                uidsToDelete.append(enemy.uid)
            enemy.used = False
        for uid in uidsToDelete:
            del self.enemies[uid]


    def update(self, info, dt=0):
        #print("info: ", info)
        for i in range(len(info)):
            tl = info[i]
            if tl["uid"] not in self.enemies.keys():
                self.enemies[tl["uid"]] = Enemy(tl["x"], tl["y"], 50, 50, tl["uid"], 100, tl["enemyType"])
                self.enemies[tl["uid"]].health = tl["health"]
            else:
                self.enemies[tl["uid"]].setPos((tl["x"], tl["y"]))
                self.enemies[tl["uid"]].sprite_state = tl["column"]
                if tl["health"] < self.enemies[tl["uid"]].health:
                    self.enemies[tl["uid"]].damageTaken = 1.0
                self.enemies[tl["uid"]].health = tl["health"]

            self.enemies[tl["uid"]].dir = tl["dir"]
            self.enemies[tl["uid"]].used = True
            self.enemies[tl["uid"]].damageTaken -= dt*4
            if tl["enemyType"] == 2:
                self.bossUid = tl["uid"]


    def takeHit(self, pos, dir, dt):
        for enemy in self.enemies.values():
            enemyPos = [enemy.x, enemy.y]
            dist = distanceV(pos, [enemyPos[0], enemyPos[1]])
            if dist < 1:
                vec = normDiff(pos, [enemyPos[0], enemyPos[1]])
                enemyDir = dirFromVec([-vec[0], -vec[1]])
                if dir == enemyDir:
                    enemy.health = max(0, enemy.health-dt*50.0)

    def getInfo(self):
        info = []
        for enemy in self.enemies.values():
            info.append({"uid" : enemy.uid, "health" : enemy.health})
        return info


class Enemy:
    def __init__(self, x, y, width, height, uid, max_health=100, typeOfEnemy=0) -> None:
        self.uid = uid
        self.x = x
        self.y = y
        self.rect = (x, y, width, height)
        self.max_health = max_health
        self.health = max_health
        self.sprite_state = [0,0]
        self.used = False
        self.typeOfEnemy = typeOfEnemy
        self.damageTaken = -1 # When there damage is being taken, a red offset should appear in the drawing
        self.dir = [1.0, 0.0]
    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pos + self.rect[2:]
    def draw(self, camera, particleSystem : ParticleSystem):
        if self.dir != [0.0, 0.0]:
            particleSystem.addParticle([self.x, self.y], [-self.dir[0], -self.dir[1]], 0.01 if self.typeOfEnemy == 0 else 0.2, (125, 125,125,255) if self.typeOfEnemy == 0 else (191, 64, 191, 255))

        adjusted_x = int((self.rect[0]-camera[0])*100)
        adjusted_y = int((self.rect[1]-camera[1])*100)
        coaf = 2
        if self.typeOfEnemy == 4:
            coaf = 3
        newSize = (self.rect[2]*coaf, self.rect[3]*coaf)
        newRect = (int(adjusted_x-newSize[0]/2 + width/2),
                   int(adjusted_y-newSize[1]/2 + height/2),
                   newSize[0], 
                   newSize[1])

        #print("rect: ", newRect)
        #rl.draw_rectangle(int(newRect[0]), int(newRect[1]), int(newRect[2]), int(newRect[3]), rl.RED)
        if self.typeOfEnemy == 0 or self.typeOfEnemy == 3:
            if self.typeOfEnemy == 0:
                color = (125,125,125,255) if self.damageTaken < 0 else (255, 0, 0, 255)
            else:
                color = (82, 37, 90, 255) if self.damageTaken < 0 else (255, 0 ,0, 255)
            rl.draw_texture_pro(TextureHandler.getEnemyAtlas(),
                                self.sprite_state, 
                                newRect, (0,0), 0, color)

            arrowRect = [newRect[0]+newRect[2]/2, newRect[1]+newRect[3]/2, newRect[2]/1.9, newRect[3]/1.9]
            angle = math.atan2(self.dir[1], self.dir[0])*(180/math.pi)
            rl.draw_texture_pro(TextureHandler.get("skeleton_bow"), [0,0,710,710], arrowRect, (-arrowRect[2]/8,arrowRect[3]/2), angle, 
                                [255,255,255,255] if self.typeOfEnemy == 0 else [0,255,0,255])

        elif self.typeOfEnemy == 1:
            rl.draw_texture_pro(TextureHandler.get("slime"),
                                self.sprite_state, 
                                newRect, (0,0), 0, [255, 125, 252, 255] if self.damageTaken < 0 else [255, 0, 0, 255])
        elif self.typeOfEnemy == 2:

            rl.draw_texture_pro(TextureHandler.get("bossTexture") if self.health > 60 else TextureHandler.get("bossTexture2"),
                                (0,0, 187, 200), 
                                newRect, (0,0), 0, [255, 255, 255, 255] if self.damageTaken < 0 else [255, 0, 0, 255])
        elif self.typeOfEnemy == 4:
            rl.draw_texture_pro(TextureHandler.get("knightTex"),
                                self.sprite_state, 
                                newRect, (0,0), 0, [255, 255, 255, 255] if self.damageTaken < 0 else [255, 0, 0, 255])


        rl.draw_rectangle(int(newRect[0]+newRect[2]/4), newRect[1], int(newRect[2]/2), 10, (80,80,80,200))
        rl.draw_rectangle(int(newRect[0]+newRect[2]/4), newRect[1], int(self.health*(newRect[2]/self.max_health)/2), 10, (69*2,12*2,19*2,255))



