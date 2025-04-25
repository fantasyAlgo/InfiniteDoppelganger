import socket

from _thread import *
import threading
import sys
import json
import traceback
import uuid
import math

from numpy import add

from helpers import *
from PlayerHandler import *
from EnemyHandler import *
import time
import msgpack

TICK_RATE = 60  # 60 updates per second
TICK_DURATION = 1.0 / TICK_RATE

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

weapon2Arrow = [1,0,4]

server = get_local_ip()
print("ip: ", server)
port = 5555
enemyId = 0

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # FOR TCP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.bind(("0.0.0.0", port))
    print("binded")
except socket.error as e:
    str(e)

#s.listen(3)
print("Waiting for a connection, Server Started")

def str2Pos(str_pos):
    s = str_pos.split(",")
    return (float(s[0]), float(s[1]))

#players = {}
playerHandlder = PlayerHandlder()
enemyHandler = EnemyHandler()


import threading

def game_loop():
    TICK_RATE = 60  # 60 ticks per second
    TICK_DURATION = 1.0 / TICK_RATE
    last_time = time.time()

    while True:
        now = time.time()
        dt = now - last_time
        last_time = now

        # Update game logic (independent of networking)
        enemyHandler.updateEnemies(playerHandlder.players, dt)
        enemyHandler.updateArrows(dt, playerHandlder.players)

        time.sleep(max(0, TICK_DURATION - (time.time() - now)))


def server_loop():
    #global s
    while True:
        try:
            #print("⏳ Waiting for data...")
            reply, addr = s.recvfrom(16384)
            uid = addr[0]
            if not uid in playerHandlder.players.keys():
                print("Idiot with addr: ", addr, " is here")
                playerHandlder.addPlayer(uid)

            # Attempt to parse JSON
            try:
                reply = msgpack.unpackb(reply, raw=False) #json.loads(reply)
            except msgpack.exceptions.UnpackException as e:
                print("JSON Decode Error:", e)
                print("Raw Data Received:", repr(reply))
                continue

            playerReply = reply["player"][0]
            if reply["type"] != "START":
                playerHandlder.updateData(uid, playerReply)
                enemyHandler.updateHealth(reply["enemies"])
                if playerReply["weapon"] in [0,2] and playerReply["isThrowing"] and enemyHandler.arrowHandler.canShoot(uid):
                    enemyHandler.arrowHandler.add(uid, [playerReply["x"], playerReply["y"]], 
                                                  [playerReply["dir"][0]*1.5, playerReply["dir"][1]*1.5], weapon2Arrow[playerReply["weapon"]], uid)
            elif reply["type"] == "STOP":
                continue
            else:
                print("started")
                playerHandlder.players[uid].health = 100

            enemyData = enemyHandler.getPositions(playerHandlder.players[uid].pos)
            arrowsData = enemyHandler.getArrows(playerHandlder.players[uid].pos)
            playerData = playerHandlder.getPlayerData(uid)
            #playerData["free_islands"] = enemyHandler.unfreePlaces


            response = msgpack.packb({"players": playerData, "enemies" : enemyData, "arrows" : arrowsData, "free_islands" : enemyHandler.unfreePlaces}, use_bin_type = True)
            s.sendto(response, addr)  # convert to json string

        except Exception as e:
            print("Error occurred:", e)
            traceback.print_exc()  # Prints the full error traceback
            break

threading.Thread(target=game_loop, daemon=True).start()
server_loop()
#threading.Thread(target=server_loop, daemon=True).start()
#while True:
#    continue



#start_new_thread(threaded_client, (conn, currentplayer))
'''
currentplayer = 0
while True:
    conn, addr = s.accept()
    print("connected to:", addr)
    start_new_thread(threaded_client, (conn, currentplayer))
    currentplayer += 1
'''




