import pyray as rl
from textureHandler import TextureHandler
from ParticleSystem import *
from Settings import *
import math

class ArrowHandler:
    def __init__(self) -> None:
        self.isBoomerangActive = False
        self.prevInfo = {}

    def draw(self, camera, info, particleSystem : ParticleSystem):
        if self.prevInfo != info:
            self.isBoomerangActive = False
        self.prevInfo = info
        #print("info: ", info)
        for i in range(len(info)):
            tl = info[i]
            self.drawArrow(camera, tl, particleSystem)

    def drawArrow(self, camera, arrow, particleSystem : ParticleSystem):
        angle = math.atan2(arrow["dir"][1], arrow["dir"][0])*(180/math.pi)
        rect = arrow["pos"] + [24,24]
        adjusted_x = int((rect[0]-camera[0])*100)
        adjusted_y = int((rect[1]-camera[1])*100)
        coaf = 2
        newSize = (rect[2]*coaf, rect[3]*coaf)
        newRect = (int(adjusted_x-newSize[0]/2 + width/2),
                   int(adjusted_y-newSize[1]/2 + height/2),
                   newSize[0], 
                   newSize[1])
        time = arrow["time"]
        newRect = (newRect[0]+newRect[2]/2, newRect[1]+newRect[3]/2, newRect[2], newRect[3])
        #rl.draw_rectangle(newRect[0], newRect[1], newRect[2], newRect[3], (255,255,255,255))
        #print(angle+45)
        arrowColor = rl.WHITE
        usedAngle = angle + 45
        if arrow["foe"] == 1: 
            texture = TextureHandler.getWoodenArrow()
            color = ( 255, 87, 51 )
        elif arrow["foe"] == 0 or arrow["foe"] == 4:
            texture = TextureHandler.getArrow()
            color = (125, 125, 125)
            if arrow["foe"] == 4:
                color = ( 0, 125, 51 )
                arrowColor = (0, 125, 0, 255)
        elif arrow["foe"] == 2:
            texture = TextureHandler.get("vomitBall")
            color = (40, 83, 10)
        elif arrow["foe"] == 7:
            self.isBoomerangActive = True
            texture = TextureHandler.get("boomerang")
            color = (193, 154, 107)
            usedAngle += arrow["time"]*400
        elif arrow["foe"] == 8:
            texture = TextureHandler.get("swordArrow")
            color = (193, 154, 107)
        else:
            texture = TextureHandler.getWoodenArrow()
            color = (125,125,125)

        particleSystem.addParticle(arrow["pos"], [-arrow["dir"][0], -arrow["dir"][1]], 0.1 if arrow["foe"] == 2 else 0.01, color)
        rl.draw_texture_pro(texture,
                            (0,0,500,500), 
                            newRect, (newRect[2]/2, newRect[3]/2), usedAngle, arrowColor)


