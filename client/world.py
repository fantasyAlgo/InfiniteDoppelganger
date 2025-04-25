from os import get_blocking
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
       
    def checkCollision(self, rect):
        pIndx = (rect[0]*100)/block_width, (rect[1]*100)/block_height
        if not self.doorsClosed:
            return self.blocks[int(pIndx[0])][int(pIndx[1])] in [1,6] #or self.blocks[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] in [1,6]
        else:
            return self.blocks[int(pIndx[0])][int(pIndx[1])] in [1,6,4] or self.blocks[int(pIndx[0])][math.ceil(pIndx[1]-0.2)] in [1,6,4]








'''
import pyray as rl
from textureHandler import TextureHandler
from Settings import *

class SimpleRectangle:
    def __init__(self, x, y, width_base, height_base, indxSprite=2, spritePos=(40, 40, 1024-40, 1024-40)) -> None:
        self.x = int(x/100)
        self.y = int(y/100)
        self.width = int(width_base)
        self.height = int(height_base)
        self.rect = (int(x), int(y), self.width, self.height)
        self.indxSprite = indxSprite
        self.spritePos = spritePos
    def draw(self, camera):
        adjusted_x = int((self.x - camera[0])*100) + int(width/2)
        adjusted_y = int((self.y - camera[1])*100) + int(height/2)
        rect = (adjusted_x, adjusted_y, self.width, self.height)
        #rl.draw_rectangle(adjusted_x, adjusted_y, self.width, self.height, rl.BLACK)  # Left border
        #print(self.spritePos, rect)
        rl.draw_texture_pro(TextureHandler.getTextureByIdx(self.indxSprite),
                            self.spritePos, 
                            rect, (0,0), 0, rl.WHITE)

    def checkCollision(self, pos):
        adjusted_x = int((self.x - pos[0])*100) + int(width/2)
        adjusted_y = int((self.y - pos[1])*100) + int(height/2)

        rect_pos = (adjusted_x, adjusted_y, self.rect[2], self.rect[3])
        pos_base = (width/2-pos[2]/2, height/2-pos[3]/2, pos[2], pos[3])
        #print(rect_pos, pos_base)
        if rl.check_collision_recs(rect_pos, pos_base):
            return True
        return False




class Chamber:
    def __init__(self, x=0, y=0, width_base=40, height_base=40) -> None:
        self.x = int(x)
        self.y = int(y)
        self.outline = 40
        self.width = int(width_base)
        self.height = int(height_base)
        self.rect = (self.x,self.y,self.width,self.height)
        self.rects = [
            SimpleRectangle(self.x, self.y, self.outline, self.height),
            SimpleRectangle(self.x, self.y, self.width, self.outline),
            SimpleRectangle(self.x+self.width, self.y, self.outline, self.height),
            SimpleRectangle(self.x, self.y+self.height, self.width+self.outline-1, self.outline),
        ]
        self.backgroundRect = SimpleRectangle(self.x, self.y, self.width, self.height, 1, (0, 0, 48, 48))

        self.doors = [False,False,False,False]

    def addDoor(self, doorIdx):
        self.doors[doorIdx] = True
        if doorIdx == 0:  # Left door
            self.rects[0] = SimpleRectangle(self.x, self.y, self.outline, self.height / 2 - self.outline / 2)
            self.rects.append(SimpleRectangle(self.x, self.y + self.height / 2 + self.outline * 2, self.outline, self.height / 2 - self.outline / 2))
        elif doorIdx == 1:  # Top door
            self.rects[1] = SimpleRectangle(self.x, self.y, self.width / 2 - self.outline / 2, self.outline)
            self.rects.append(SimpleRectangle(self.x + self.width / 2 + self.outline * 2, self.y, self.width / 2 - self.outline / 2, self.outline))
        elif doorIdx == 2:  # Right door
            self.rects[2] = SimpleRectangle(self.x + self.width + self.outline, self.y, self.outline, self.height / 2 - self.outline / 2)
            self.rects.append(SimpleRectangle(self.x + self.width + self.outline, self.y + self.height / 2 + self.outline * 2, self.outline, self.height / 2 - self.outline / 2))
        elif doorIdx == 3:  # Bottom door
            self.rects[3] = SimpleRectangle(self.x, self.y + self.height, self.width / 2 - self.outline / 2, self.outline)
            self.rects.append(SimpleRectangle(self.x + self.width / 2 + self.outline / 2, self.y + self.height, self.width / 2 - self.outline/2, self.outline))


    def draw(self, camera):
        self.backgroundRect.draw(camera)
        for rect in self.rects:
            rect.draw(camera)
    
    def checkCollision(self, pos):
        for rect in self.rects:
            if rect.checkCollision(pos):
                return True
        return False


class Dungeon:
    chambers = []
    connections = []
    def __init__(self) -> None:
        self.chambers = []
        self.connections = []
    def createChamber(self, x, y, width, height):
        self.chambers.append(Chamber(x, y, width, height))
        self.chambers[-1].addDoor(3)

    def draw(self, camera):
        for chamber in self.chambers:
            chamber.draw(camera)
        for connection in self.connections:
            connection.draw(camera)
    def connectChambers(self, indx1, indx2):
        connection = Connection(self.chambers[indx1], self.chambers[indx2])
        self.connections.append(connection)
       
    def checkCollision(self, rect):
        for chamber in self.chambers:
            if chamber.checkCollision(rect):
                return True
        for connection in self.connections:
            if connection.checkCollision(rect):
                return True
        return False
        #for connection in self.connections:
        #    connection.draw(camera)




class Connection:
    def __init__(self, chamber1, chamber2):
        self.chamber1 = chamber1
        self.chamber2 = chamber2
        self.pathway_rects = []
        self.create_pathway()
        print(self.pathway_rects)
    
    def create_pathway(self):
        # Determine chamber positions
        c1_center_x = self.chamber1.x + self.chamber1.width / 2
        c1_center_y = self.chamber1.y + self.chamber1.height / 2
        c2_center_x = self.chamber2.x + self.chamber2.width / 2
        c2_center_y = self.chamber2.y + self.chamber2.height / 2
        
        # Determine which doors to use based on relative positions
        door1_idx = self.determine_door_idx(c1_center_x, c1_center_y, c2_center_x, c2_center_y)
        door2_idx = self.determine_door_idx(c2_center_x, c2_center_y, c1_center_x, c1_center_y)
        
        # Make sure the doors exist
        if not self.chamber1.doors[door1_idx]:
            self.chamber1.addDoor(door1_idx)
        if not self.chamber2.doors[door2_idx]:
            self.chamber2.addDoor(door2_idx)
        
        # Create pathway based on door positions
        self.create_pathway_rects(door1_idx, door2_idx)
    
    def determine_door_idx(self, from_x, from_y, to_x, to_y):
        # Determine which door to use based on direction
        dx = to_x - from_x
        dy = to_y - from_y
        
        # Determine predominant direction
        if abs(dx) > abs(dy):
            # Horizontal predominant
            if dx > 0:
                return 2  # Right door
            else:
                return 0  # Left door
        else:
            # Vertical predominant
            if dy > 0:
                return 3  # Bottom door
            else:
                return 1  # Top door
    
    def create_pathway_rects(self, door1_idx, door2_idx):
        path_width = 40  # Same as door width
        
        # Get door positions
        door1_pos = self.get_door_position(self.chamber1, door1_idx)
        door2_pos = self.get_door_position(self.chamber2, door2_idx)
        print(door1_pos, door2_pos)
        
    def get_door_position(self, chamber, door_idx):
        # Calculate door position based on chamber and door index
        if door_idx == 0:  # Left
            return (chamber.x, chamber.y + chamber.height/2)
        elif door_idx == 1:  # Top
            return (chamber.x + chamber.width/2, chamber.y)
        elif door_idx == 2:  # Right
            return (chamber.x + chamber.width, chamber.y + chamber.height/2)
        elif door_idx == 3:  # Bottom
            return (chamber.x + chamber.width/2, chamber.y + chamber.height)
    
    def draw(self, camera):
        for rect in self.pathway_rects:
            rect.draw(camera)
    
    def checkCollision(self, pos):
        for rect in self.pathway_rects:
            if rect.checkCollision(pos):
                return True
        return False

'''
