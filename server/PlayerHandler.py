class PlayerHandlder:
    def __init__(self) -> None:
        self.players = {}
    def updateData(self, uid, data): #, pos, sprite_state, isInvincible, weapon):
        self.players[uid].pos = [data["x"], data["y"]]
        self.players[uid].sprite_state = data["sprite_state"] 
        self.players[uid].isInvincible = data["isInvincible"]
        self.players[uid].weapon = data["weapon"]
        self.players[uid].bowDirAngle = data["bowDirAngle"]
    def update(self, dt):
        toDelete = []
        for uid in self.players.keys():
            self.players[uid].time += dt
            if self.players[uid].time > 1:
                toDelete.append(uid)
        for uid in toDelete:
            del self.players[uid]





    def addPlayer(self, uid):
        self.players[uid] = Player((0,0), uid)
    def deletePlayer(self, uid):
        del self.players[uid]
    def getPlayerData(self, mainUid):
        return [p.getData(mainUid==pid) for pid, p in self.players.items()]

class Player:
    uid = ""
    pos = (0,0)
    sprite_state = (0,0, 48, 48)
    isInvincible = False
    def __init__(self, pos, uid) -> None:
        self.pos = pos
        self.uid = uid
        self.sprite_state = (0,0, 48, 48)
        self.health = 100
        self.enemyType = -1
        self.isInvincible = False
        self.weapon = 0
        self.dir = [0,0]
        self.bowDirAngle = 0
        self.current_island = 0
        self.free_islands = []
        self.time = 0
    def getData(self, isMain):
        return {"uid": self.uid, "x": round(self.pos[0], 2), "y": round(self.pos[1], 2), "column" : self.sprite_state, 
                "health" : self.health, "isMain" : isMain, "weapon" : self.weapon, "bowDirAngle" : self.bowDirAngle,
                "current_island" : self.current_island}



