import math

def columnPosition(lastDir, running, isSwinging = False):
    directions = [
        (0, 48*2+8,  48, 48),
        (0, 48*1+8,  48, 48),
        (0, 48*0+8,  48, 48),
        (0, 48*1+8, -48, 48),
    ]
    if running >= 0 and not isSwinging:
        directions = [(el[0]+48*(running%5), el[1]+144, el[2], el[3]) for el in directions]
    elif isSwinging:
        directions = [(el[0]+48*(running%4), el[1]+48*6, el[2], el[3]) for el in directions]
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
