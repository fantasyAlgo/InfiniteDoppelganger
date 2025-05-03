import pyray as rl
from textureHandler import TextureHandler
from Settings import *
import numpy as np
import math

class SimpleRectangle:
    def __init__(self, x, y, width_base, height_base, indxSprite="", spritePos=(40, 40, 1024-40, 1024-40), color = rl.WHITE) -> None:
        self.x = int(x/100)
        self.y = int(y/100)
        self.width = int(width_base)
        self.height = int(height_base)
        self.rect = (int(x), int(y), self.width, self.height)
        self.indxSprite = indxSprite
        self.spritePos = spritePos
        self.color = color
    def setPos(self, x, y):
        self.x = x
        self.y = y
    def draw(self, camera, spritePos = None):
        usedSpritePos = self.spritePos
        if spritePos != None:
            usedSpritePos = spritePos

        #print(self.x, self.y)
        adjusted_x = int((self.x - camera[0])*100) + int(width/2)
        adjusted_y = int((self.y - camera[1])*100) + int(height/2)
        rect = (adjusted_x, adjusted_y, self.width, self.height)
        #rl.draw_rectangle(adjusted_x, adjusted_y, self.width, self.height, rl.BLACK)  # Left border
        #print(self.spritePos, rect)
        rl.draw_texture_pro(TextureHandler.get(self.indxSprite),
                            usedSpritePos, 
                            rect, (0,0), 0, self.color)

textures = [
    SimpleRectangle(0,0,block_width,block_height, indxSprite="worldTiles", spritePos=(6*16, 10*16, 16, 16), color = (125, 125, 125, 255)),
    SimpleRectangle(0,0,block_width,block_height, indxSprite="worldTiles", spritePos=(10*16, 3*16, 16, 16), color = (125,125,125,255)),
    SimpleRectangle(0,0,block_width,block_height, indxSprite="worldTiles", spritePos=(5*16, 13*16, 16, 16), color = (125,125,125,255)),
    SimpleRectangle(0,0,block_width,block_height, indxSprite="worldTiles", spritePos=(0, 0, 0, 10), color = (50,50,50,200))

]
class Dungeon:
    def __init__(self, map_name) -> None:
        self.blocks = np.zeros((width, height))
        self.load(mapDir / map_name)
        self.shape = self.blocks.shape
        self.doorsClosed = True
        self.inPassage = True
    def getSpawnPoint(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.blocks[i][j] == 2:
                    return i*block_width, j*block_height
        return 0, 0

    def load(self, path : str):
        self.blocks = np.load(path)
    def getBlock(self, i, j):
        if i < 0 or j < 0 or i >= self.blocks.shape[0] or j >= self.blocks.shape[1]:
            return -1
        return self.blocks[i][j]
    def draw(self, camera):
        frame_x = (math.floor(100*camera[0]/block_width-width/block_width/2), math.ceil(100*camera[0]/block_width+width/block_width/2))
        frame_y = (math.floor(100*camera[1]/block_height-height/block_height/2), math.ceil(100*camera[1]/block_height+height/block_height/2))
        for i in range(max(frame_x[0],0), min(frame_x[1], self.shape[0])):
            for j in range(max(frame_y[0],0), min(frame_y[1], self.shape[1])):
                if self.blocks[i][j] == 0 and (self.getBlock(i+1, j) == 1 or self.getBlock(i-1, j) == 1 or self.getBlock(i, j+1) == 1 or self.getBlock(i, j-1) == 1 or 
                                               self.getBlock(i+1, j+1) == 1 or self.getBlock(i-1, j-1) == 1 or self.getBlock(i+1, j-1) == 1 or self.getBlock(i-1, j+1)):
                    textures[3].setPos((i*block_width)/100, (j*block_height)/100)
                    textures[3].draw(camera)

                if self.blocks[i][j] == 1:
                    textures[0].setPos((i*block_width)/100, (j*block_height)/100)
                    if self.blocks[i+1][j+1] == 0 and self.blocks[i+1][j] == 0 and self.blocks[i][j+1] == 0:
                        textures[0].draw(camera, (15*16, 10*16, 16, 16))
                    elif self.blocks[i-1][j+1] == 0 and self.blocks[i][j+1] == 0 and self.blocks[i-1][j] == 0:
                        textures[0].draw(camera, (12*16, 10*16, 16, 16))
                    elif self.blocks[i+1][j-1] == 0 and self.blocks[i+1][j] == 0 and self.blocks[i][j-1] == 0:
                        textures[0].draw(camera, (15*16, 10*16, 16, 16))
                    elif self.blocks[i-1][j-1] == 0 and self.blocks[i][j-1] == 0 and self.blocks[i-1][j] == 0:
                        textures[0].draw(camera, (12*16, 10*16, 16, 16))
                    else:
                        textures[0].draw(camera)

                if self.blocks[i][j] == 3 or self.blocks[i][j] == 2 or self.blocks[i][j] == 5:
                    textures[1].setPos((i*block_width)/100, (j*block_height)/100)
                    textures[1].draw(camera, (8*16, 12*16, 16, 16))

                if self.blocks[i][j] == 4:
                    if not self.doorsClosed:
                        textures[1].setPos((i*block_width)/100, (j*block_height)/100)
                        textures[1].draw(camera, (8*16, 12*16, 16, 16))
                    else:
                        textures[2].setPos((i*block_width)/100, (j*block_height)/100)
                        textures[2].draw(camera)

                if self.blocks[i][j] == 6:
                    textures[1].setPos((i*block_width)/100, (j*block_height)/100)
                    if self.blocks[i-1][j-1] == 3 and self.blocks[i-1][j] == 3 and self.blocks[i+1][j] == 3:
                        textures[1].draw(camera, (4*16, 7*16,16,16))
                    elif self.blocks[i-1][j-1] == 3 and self.blocks[i][j-1] != 6 and self.blocks[i-1][j] != 6:
                        textures[1].draw(camera, (5*16, 7*16,16,16))
                    elif self.blocks[i+1][j-1] == 3 and self.blocks[i][j-1] != 6 and self.blocks[i+1][j] != 6:
                        textures[1].draw(camera, (7*16, 7*16,16,16))
                    elif self.blocks[i-1][j+1] == 3 and self.blocks[i][j+1] != 6 and self.blocks[i-1][j] != 6:
                        textures[1].draw(camera, (5*16, 7*16,16,-16))
                    elif self.blocks[i+1][j+1] == 3 and self.blocks[i][j+1] != 6 and self.blocks[i+1][j] != 6:
                        textures[1].draw(camera, (7*16, 7*16,16,-16))
                    elif self.blocks[i][j+1] == 3:
                        textures[1].draw(camera, (6*16, 7*16,16,-16))
                    elif self.blocks[i-1][j] == 3:
                        textures[1].draw(camera, (5*16, 8*16,16,16))
                    elif self.blocks[i+1][j] == 3:
                        textures[1].draw(camera, (7*16, 8*16,16,16))
                    elif self.blocks[i][j-1] == 3:
                        textures[1].draw(camera, (6*16, 7*16,16,16))
                        



    def connectChambers(self, indx1, indx2):
        pass

    def getType(self, rect):
        pIndx = (rect[0]*100)/block_width, (rect[1]*100)/block_height
        return self.blocks[int(pIndx[0])][int(pIndx[1])]

    def checkCollision(self, rect):
        pIndx = (rect[0]*100)/block_width, (rect[1]*100)/block_height
        if not self.doorsClosed:
            #print("type: ", self.blocks[int(pIndx[0])][int(pIndx[1])])
            if self.blocks[int(pIndx[0])][int(pIndx[1])] == 4:
                #print("bobobobob")
                #print(self.blocks[int(pIndx[0])][int(pIndx[1])])
                self.inPassage = True
            return self.blocks[int(pIndx[0])][int(pIndx[1])] in [1,6] #or self.blocks[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] in [1,6]
        else:
            if self.inPassage and (self.blocks[int(pIndx[0])][int(pIndx[1])] == 4 or self.blocks[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] == 4):
                #print("skibidi")
                return False
            self.inPassage = False
            return self.blocks[int(pIndx[0])][int(pIndx[1])] in [1,6,4] or self.blocks[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] in [1,6,4]








