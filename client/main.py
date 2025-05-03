#from pyray import *

import pyray as rl

from ParticleSystem import ParticleSystem
from MusicHandler import MusicHandler
from textureHandler import TextureHandler

from playerHandler import Player, PlayerHandler
from enemyHandler import *
from ArrowHandler import *



from world import Dungeon
from network import Network
import random
from Settings import *

from UI import UI

#rl.set_window_state(rl.FLAG_WINDOW_RESIZABLE)
rl.init_window(width, height, "Infinite doppleganger")
rl.init_audio_device()
rl.set_target_fps(144)

rl.hide_cursor()
clientNumber = 0
handler = TextureHandler()

def sendData(network, player, enemyHandler, typeRequest="CLIENT"):
    if not typeRequest in ["CLIENT", "START", "SERVER"]:
        return
    ps = network.send({
        "type" : typeRequest,
        "player" : player.getInfo(),
        "enemies" : enemyHandler.getInfo(),
    })

    return ps


class Game:
    def __init__(self) -> None:
        self.run = True
        self.n = Network()
        self.dungeon = Dungeon("map3.npy")
        self.musicHandler = MusicHandler()
        self.playerHandler = PlayerHandler(self.dungeon.getSpawnPoint(), self.musicHandler)
        self.enemyHandler = EnemyHandler()
        self.particleSystem = ParticleSystem()
        self.arrowHandler = ArrowHandler()
        self.arrowsInfo = []
        self.UI = UI()
        self.serverWorking = 0

        print(self.playerHandler.mainPlayer.x, self.playerHandler.mainPlayer.y)
    def initialize(self):
        self.playerHandler.restart()
        ps = sendData(self.n, self.playerHandler.mainPlayer, self.enemyHandler, "START")
        if ps == None:
            print("None")
            return
        self.enemyHandler.update(ps["enemies"])
        self.arrowsInfo = ps["arrows"]
        
    def update(self):
        self.musicHandler.update()
        if (self.UI.isOn):
            r = self.UI.update()
            if r == 0:
                self.n.start()
                self.initialize()
                self.musicHandler.stopUIAndPlay()
            elif r == 1:
                self.currentShow = 1
            elif r == 2:
                self.run = False
            return 

        dt = rl.get_frame_time()
        self.playerHandler.updateMain(dt, self.dungeon, self.enemyHandler, self.particleSystem, self.musicHandler, self.arrowHandler)
        self.particleSystem.update(dt)

        ps = sendData(self.n, self.playerHandler.mainPlayer, self.enemyHandler)
        if ps == None:
            print("None")
            return
        if not "enemies" in ps.keys():
            return

        self.playerHandler.update(ps["players"], self.dungeon, ps["free_islands"])
        self.enemyHandler.update(ps["enemies"], dt)
        self.arrowsInfo = ps["arrows"]

        if self.playerHandler.mainPlayer.health <= 0:
            ps = sendData(self.n, {}, {}, "STOP")
            self.musicHandler.addGameOver()
            self.UI.deadPlayer = True
            self.UI.isOn = True
            # todo, main player death

        #print("first: ", len(self.arrowsInfo))


    def draw(self):
        camera = self.playerHandler.getCamera()
        rl.begin_drawing()
        rl.clear_background((12,10,18,255))
        if self.UI.isOn:
            self.UI.draw()
        else:
            self.dungeon.draw(camera)
            self.particleSystem.draw(camera)
            self.playerHandler.draw(camera, self.arrowHandler)
            self.enemyHandler.draw(camera, self.particleSystem)
            self.playerHandler.drawUI(camera)

            self.arrowHandler.draw(camera, self.arrowsInfo, self.particleSystem)
        rl.draw_fps(width-50, 10)
        rl.end_drawing()

    def gameLoop(self):
        while not rl.window_should_close() and self.run:
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.gameLoop()


rl.close_window()
