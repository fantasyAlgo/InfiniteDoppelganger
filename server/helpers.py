from pathlib import Path
import math

baseDir = Path(__file__).parent.parent
imageDir = baseDir / "images"
mapDir = baseDir / "maps"

block_width, block_height = 37, 37


def columnPositionEnemy(lastDir, running = -1, fighting = False, health = 10):
    directions = [
        (0, 32*2,  32, 32),
        (0, 32*1,  32, 32),
        (0, 32*0,  32, 32),
        (0, 32*1, -32, 32),
    ]
    if health <= 0:
        directions = [(el[0]+32*(running%4), el[1]+5*32, el[2], el[3]) for el in directions]
        return directions[1 if lastDir == 0 or lastDir == 2 else 3]

    if running >= 0:
        directions = [(el[0]+32*(running%6), el[1]+3*32, el[2], el[3]) for el in directions]
    elif fighting:
        directions = [(el[0]+32*(running%6), el[1]+6*32, el[2], el[3]) for el in directions]
    return directions[lastDir]

def columnPositionSlime(lastDir, running = -1, fighting = False, health = 10):
    directions = [
        (0, 32*2,  32, 32),
        (0, 32*1,  32, 32),
        (0, 32*0,  32, 32),
        (0, 32*1, -32, 32),
    ]
    if health <= 0:
        directions = [(el[0]+32*(running%4), el[1]+5*32, el[2], el[3]) for el in directions]
        return directions[1 if lastDir == 0 or lastDir == 2 else 3]

    if running >= 0:
        directions = [(el[0]+32*(running%6), el[1]+3*32, el[2], el[3]) for el in directions]
    elif fighting:
        directions = [(el[0]+32*(running%6), el[1]+6*32, el[2], el[3]) for el in directions]
    return directions[lastDir]

def columnPositionKhight(lastDir, running = -1, fighting = False, health = 10):
    directions = [
        (25, 100*1+25,  50,  50),
        (25, 100*1+25,  -50, 50),
        (25, 100*1+25,  50,  50),
        (25, 100*1+25, -50,  50),
    ]
    if health <= 0:
        print("bbbbffuua")
        directions = [(el[0]+100*(running%4), el[1]+100*12, el[2], el[3]) for el in directions]
        return directions[1 if lastDir == 0 or lastDir == 2 else 3]


    if fighting:
        directions = [(el[0]+100*(running%6), el[1] + 100*2, el[2], el[3]) for el in directions]
    elif running >= 0:
        directions = [(el[0]+100*(running%8), el[1], el[2], el[3]) for el in directions]
    return directions[lastDir]



def dirFromVec(pos):
    angle = -math.atan2(pos[1], pos[0])*(180/math.pi) + 180 + 90
    if angle > 45 and angle < 135:
        lastDir = 3
    elif angle < 45 or angle > 315:
        lastDir = 0
    elif angle > 135 and angle < 225:
        lastDir = 2
    else: #angle > 225 and angle < 315:
        lastDir = 1
    return lastDir

def distanceV(vec1, vec2):
    dist = math.sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)
    return dist
def normDiff(vec1, vec2):
    dist = distanceV(vec1, vec2)
    diff = [vec1[0]-vec2[0], vec1[1]-vec2[1]]
    return [diff[0]/dist, diff[1]/dist]
