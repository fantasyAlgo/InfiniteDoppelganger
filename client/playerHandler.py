import math
from typing import Never
from numpy import pi
import pyray as rl
import random
from ParticleSystem import ParticleSystem
from MusicHandler import MusicHandler
from ArrowHandler import ArrowHandler
from world import Dungeon 
from enemyHandler import EnemyHandler
from textureHandler import *
from Settings import *
from helpers import *

def createPortalFunction(startPos, endPos, lastDir=0):
    dist = math.dist(startPos, endPos)
    maxDist = 2.7
    if dist > maxDist:
        diff = [(endPos[0]-startPos[0])/dist, (endPos[1]-startPos[1])/dist]
        endPos = [startPos[0] + diff[0]*maxDist, startPos[1] + diff[1]*maxDist]
    smoothstep = lambda t : 3*t**2 - 2*t**3
    def f(t):
        t = smoothstep(t)
        x = startPos[0]*(1-t) +  endPos[0]*t + (math.sin(math.pi*t) if lastDir != 3 else -math.sin(math.pi*t))
        y = startPos[1]*(1-t) +  endPos[1]*t
        return (x, y)
    return f
def createPortalDerivative(startPos, endPos, lastDir=0):
    dist = math.dist(startPos, endPos)
    maxDist = 2.7
    if dist > maxDist:
        diff = [(endPos[0]-startPos[0])/dist, (endPos[1]-startPos[1])/dist]
        endPos = [startPos[0] + diff[0]*maxDist, startPos[1] + diff[1]*maxDist]
    smoothstepd = lambda t : 6*t - 6*t**2
    smoothstep = lambda t : 3*t**2 - 2*t**3
    def f(t):
        dt = smoothstepd(t)
        t = smoothstep(t)
        x = startPos[0]*dt +  endPos[0]*dt + math.cos(math.pi*t)*dt
        y = startPos[1]*dt +  endPos[1]*dt
        return (x, y)
    return f



class PlayerHandler:
    def __init__(self, pos, musicHandler) -> None:
        print(pos)
        self.basePos = pos
        self.mainPlayer = Player(pos[0]/100, pos[1]/100,50,50, (0,255,0), 0, True)
        self.players = {}
        self.musicHandler = musicHandler
        self.areDoorsClosed = False
        #self.free_islands = 
    def restart(self):
        self.mainPlayer.x = self.basePos[0]/100
        self.mainPlayer.y = self.basePos[1]/100
        self.mainPlayer.health = 100

    def getCamera(self):
        mouse_pos = rl.get_mouse_position()
        mouse_pos = [(mouse_pos.x-width/2)/(width/2), (mouse_pos.y-height/2)/(height/2)]
        return (self.mainPlayer.x + mouse_pos[0]/4, self.mainPlayer.y + mouse_pos[1]/4)

    def addPlayer(self, info):
        pass

    def update(self, info, free_islands=[]):
        #print("info: ", info)
        for i in range(len(info)):
            tl = info[i]
            if tl["isMain"]:
                if self.mainPlayer.health > tl["health"]:
                    self.musicHandler.addDamage()
                self.mainPlayer.health = tl["health"]
                self.mainPlayer.current_island = tl["current_island"]

                continue

            if tl["uid"] not in self.players.keys():
                self.players[tl["uid"]] = Player(tl["x"], tl["y"], 50, 50, (random.randint(0, 255) ,random.randint(0, 255),random.randint(0,255)), 0)
            else:
                self.players[tl["uid"]].setPos((tl["x"], tl["y"]))
                self.players[tl["uid"]].sprite_state = tl["column"]
            self.players[tl["uid"]].health = tl["health"]
            self.players[tl["uid"]].weapon = tl["weapon"]
            self.players[tl["uid"]].bowDirAngle = tl["bowDirAngle"]
            self.players[tl["uid"]].used = True
            self.players[tl["uid"]].current_island = tl["current_island"]
        print(self.mainPlayer.current_island, free_islands)
        if self.mainPlayer.current_island != 0:
            self.areDoorsClosed = self.mainPlayer.current_island in free_islands

    def updateMain(self, dt, dungeon : Dungeon, enemyHandler: EnemyHandler, particleSystem : ParticleSystem, musicHandler : MusicHandler, arrowHandler : ArrowHandler):
        dungeon.doorsClosed = self.areDoorsClosed
        #print("dt: ", dt)
        self.mainPlayer.move(dt, dungeon, particleSystem, musicHandler, arrowHandler)
        if self.mainPlayer.isSwinging:
            enemyHandler.takeHit([self.mainPlayer.x, self.mainPlayer.y], self.mainPlayer.lastDir, dt)
    def drawUI(self, camera):
        self.mainPlayer.drawUI(camera)


    def draw(self, camera, arrowHandler):
        uidToCancel = []
        for uid in self.players.keys():
            #print(player.x, player.y)
            self.players[uid].draw(camera)
            if not self.players[uid].used:
                uidToCancel.append(uid)
            self.players[uid].used = False
        for uid in uidToCancel:
            del self.players[uid]
        self.mainPlayer.draw(camera, arrowHandler.isBoomerangActive)




class Player():
    def __init__(self, x, y, width, height, color, texture, isMain=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.texture = texture 

        self.vel = 2.5
        self.used = False
        self.id = 0
        self.rect = (x, y, self.width, self.height)
        self.sprite_state = (0,0, 48, 48)
        self.lastDir = 0
        self.running = -1
        self.health = 100
        self.isMain = isMain
        self.isShifting = -100
        self.timeLapse = 0
        self.bowDirAngle = 0
        self.current_island = -1

        self.isSwinging = False
        self.mouseDir = [0.0,0.0]
        self.mousePos = rl.get_mouse_position()
        self.weapon = 1
        self.canFire = True
        self.timeLastArrow = 0.0

        self.portalFunction = None
        self.portalDer = None
        self.timePortal = 0

    def drawUI(self, camera, isBoomerangActive = True):
        ## Draw UI
        rl.draw_circle_lines(int(self.mousePos.x), int(self.mousePos.y), 10, (255, 255, 255, 255))
        rl.draw_circle_lines(int(self.mousePos.x), int(self.mousePos.y), 1, (255, 255, 255, 255))
        lst = ["wooden_bow", "swordArrow", "boomerang"]
        scale = 30
        sPosX = int(width - 3*int(width/scale) - 20)
        rl.draw_rectangle(sPosX, 10, 3*int(width/scale), int(width/scale)+10, (10, 10, 10, 255))
        rl.draw_rectangle_lines(sPosX, 10, 3*int(width/scale), int(width/scale)+10, (255, 255, 255, 255))
        for i in range(len(lst)):
            el = lst[i]
            rect = [int(sPosX + i*width/scale + width/(scale*2))-30, 15, int(width/scale), int(width/scale)]
            if i == self.weapon:
                rl.draw_rectangle(rect[0], rect[1], rect[2], rect[3], [200, 200, 200, 100])
            rl.draw_texture_pro(TextureHandler.get(el), [0,0,500,500], rect, (0,0), 0, [255,200,200,255])

    def draw(self, camera, isBoomerangActive = False):
        #print(self.current_island)
        adjusted_x = int((self.rect[0]-camera[0])*100)
        adjusted_y = int((self.rect[1]-camera[1])*100)
        coaf = 2
        newSize = (self.rect[2]*coaf, self.rect[3]*coaf)
        newRect = (int(adjusted_x-newSize[0]/2 + width/2),
                   int(adjusted_y-newSize[1]/2 + height/2),
                   newSize[0], 
                   newSize[1])
        #print("rect: ", newRect)
        #rl.draw_rectangle(int(newRect[0]), int(newRect[1]), int(newRect[2]), int(newRect[3]), rl.RED)
        if self.isMain:
            if rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
                rl.draw_circle(int(newRect[0]+newRect[2]/2), int(newRect[1]+newRect[3]/2), 300, (125, 125, 125, 30))
                if math.dist([width/2, height/2], [self.mousePos.x ,self.mousePos.y]) < 300:
                    rl.draw_texture_pro(TextureHandler.getPlayerAtlas(),
                                        self.sprite_state, 
                                        [self.mousePos.x-newRect[2]/2, self.mousePos.y-newRect[3]/2, newRect[2], newRect[3]], (0,0), 0, [125, 125, 225, 200])


            rl.draw_rectangle(10, 10, 100*2, 20, (80, 80, 80,200))
            rl.draw_rectangle(10, 10, self.health*2, 20, (69*2,12*2,19*2,255))

            rl.draw_rectangle(10, 50, 100, 20, (80, 80, 80,200))
            rl.draw_rectangle(10, 50, int(-self.timePortal*100), 20, (30,12*1,19*5,255))


        else:
            rl.draw_rectangle(int(newRect[0]+newRect[2]/4), int(newRect[1]), int(100/2), 10, (80, 80, 80,200))
            rl.draw_rectangle(int(newRect[0]+newRect[2]/4), int(newRect[1]), int(self.health/2), 10, (69*2,12*2,19*2,255))

        if self.weapon == 0:
            arrowRect = [newRect[0]+newRect[2]/2, newRect[1]+newRect[3]/2, newRect[2]/2.2, newRect[3]/2.2]
            rl.draw_texture_pro(TextureHandler.getWoodenBow(), [0,0,500,500], arrowRect, (-arrowRect[2]/8,arrowRect[3]/2), self.bowDirAngle, [255,200,200,255])
        if self.weapon == 2 and not isBoomerangActive:
            arrowRect = [newRect[0]+newRect[2]/2, newRect[1]+newRect[3]/2, newRect[2]/2.2, newRect[3]/2.2]
            rl.draw_texture_pro(TextureHandler.get("boomerang"), [0,0,500,500], arrowRect, (-arrowRect[2]/8,arrowRect[3]/2), self.bowDirAngle, [255,200,200,255])


        playerColor = rl.WHITE
        if self.portalFunction != None:
            playerColor = (125, 125, 225, 200)
            newRect = [newRect[0], newRect[1], newRect[2]/1.1, newRect[3]/1.1]

        rl.draw_texture_pro(TextureHandler.getPlayerAtlas(),
                            self.sprite_state, 
                            newRect, (0,0), 0, playerColor)




    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x,self.y,self.width,self.height)

    def updateArrow(self):
        mouse_pos_i = rl.get_mouse_position()
        mouse_pos = [(mouse_pos_i.x-width/2)/(width/2), (mouse_pos_i.y-height/2)/(height/2)]
        camera = width/2 + mouse_pos[0]/4 , height/2 + mouse_pos[1]/4
        mouse_pos = [(mouse_pos_i.x-camera[0]), (mouse_pos_i.y-camera[1])]
        angle = math.atan2(mouse_pos[1], mouse_pos[0])*(180.0/math.pi)
        magn = math.sqrt(mouse_pos[0]**2 + mouse_pos[1]**2)
        if magn == 0:
            magn = 0.01
        self.mouseDir = [mouse_pos[0]/magn, mouse_pos[1]/magn]
        self.bowDirAngle = angle

    def updatePortal(self, dungeon, dt):
        if self.portalFunction != None:
            predPos = self.portalFunction(self.timePortal)
            if not dungeon.checkCollision(predPos):
                self.x, self.y = predPos
            else:
                self.portalFunction = None
                self.timePortal = -dt
            self.timePortal += 2*dt
            if self.timePortal > 1:
                self.portalFunction = None
                self.portalDer = None
                self.timePortal = 0
        else:
            self.timePortal = max(self.timePortal-dt, -1)




    def move(self, dt = 0, dungeon = None, particleSystem=None, musicHandler = None, arrowHandler = None):
        self.mousePos = rl.get_mouse_position()
        self.updateArrow()
        self.updatePortal(dungeon, dt)

        if (self.weapon == 0 or self.weapon == 2) and self.isSwinging:
            self.isSwinging = False

        self.timeLapse += dt
        getRect = lambda sx,sy : (self.x+sx*self.vel*dt, self.y+sy*self.vel*dt, self.width, self.height)
        moved = False
        pressed_mouse = False
        #dt = 0.1


        dir = [0.0,0.0]
        dirs = [[0.0, -0.5], [0.5, 0.0], [0.0, 0.5], [-0.5, 0.0]]
        if rl.is_key_down(rl.KEY_ONE):
            self.weapon = 0
        if rl.is_key_down(rl.KEY_TWO):
            self.weapon = 1
        if rl.is_key_down(rl.KEY_ONE + 2):
            self.weapon = 2


        if self.portalFunction == None: #and (self.weapon == 0 or not self.isSwinging):
            if (rl.is_key_down(rl.KEY_A)) and not dungeon.checkCollision(getRect(-1, 0)):
                self.x -= self.vel*dt
                dir[0] = -0.5
                self.lastDir = 3
                moved = True
            if (rl.is_key_down(rl.KEY_D)) and not dungeon.checkCollision(getRect(1, 0)):
                self.x += self.vel*dt
                dir[0] = 0.5
                self.lastDir = 1
                moved = True
            if (rl.is_key_down(rl.KEY_W)) and not dungeon.checkCollision(getRect(0,-1)):
                self.y -= self.vel*dt
                self.lastDir = 0
                dir[1] = -0.5
                moved = True
            if (rl.is_key_down(rl.KEY_S)) and not dungeon.checkCollision(getRect(0, 1)):
                self.y += self.vel*dt
                self.lastDir = 2
                dir[1] = 0.5
                moved = True

            if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                if self.weapon == 1 or (self.weapon == 2 and not arrowHandler.isBoomerangActive) or (self.weapon != 2 and self.canFire and self.timeLastArrow > 0.4):
                    self.isSwinging = True
                    if self.weapon == 2:
                        arrowHandler.isBoomerangActive = True
                    self.timeLastArrow = 0.0
                    if self.weapon == 0 or self.weapon == 2:
                        musicHandler.addArrow()
                    for _ in range(100):
                        particleSystem.addParticle([self.x+dirs[self.lastDir][0]/3, self.y+dirs[self.lastDir][1]/3], dirs[self.lastDir])

                if self.weapon == 1:
                    mouse_pos = rl.get_mouse_position()
                    mouse_pos = [(mouse_pos.x-width/2)/(width/2), (mouse_pos.y-height/2)/(height/2)]
                    self.lastDir = dirFromVec(mouse_pos)
                    self.running = 0

            if self.timePortal <= -1 and rl.is_mouse_button_released(rl.MOUSE_BUTTON_RIGHT):
                mouse_pos = rl.get_mouse_position()
                mouse_pos = [(mouse_pos.x-width/2)/100, (mouse_pos.y-height/2)/100]
                mousePos = [self.x + mouse_pos[0], self.y + mouse_pos[1]]
                self.portalFunction = createPortalFunction([self.x, self.y], mousePos, self.lastDir)
                self.portalDer = createPortalDerivative([self.x, self.y], mouse_pos, self.lastDir)
                self.timePortal = 0
                musicHandler.addWhoosh()
            

        if self.weapon in [0,2]:
            mouse_pos = rl.get_mouse_position()
            mouse_pos = [(mouse_pos.x-width/2)/(width/2), (mouse_pos.y-height/2)/(height/2)]
            self.lastDir = dirFromVec(mouse_pos)


        if moved or self.isSwinging:
            self.running += dt*10* (self.vel/3)
        else:
            self.running = -1

        if self.weapon == 1 and self.isSwinging and self.running >= 4:
            self.isSwinging = False


        if moved and int(self.timeLapse*100)%2 == 0:
            particleSystem.addParticle([self.x, self.y], dir, 0.3 if self.vel == 5 else 0.125)


        self.rect = (self.x, self.y, self.width, self.height)
        self.sprite_state = columnPosition(self.lastDir, int(self.running), self.weapon == 1 and self.isSwinging)
        self.timeLastArrow += dt
        #print("sprite state: ", self.sprite_state)
    def getInfo(self):
        return {"x" : self.x, "y" : self.y, "sprite_state" : self.sprite_state, "dir" : self.mouseDir, "weapon" : self.weapon, 
                "isThrowing" : self.isSwinging, "isInvincible" : self.portalFunction != None, "bowDirAngle" : self.bowDirAngle},




