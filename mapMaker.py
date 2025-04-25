from pyray import *
import numpy as np
import os

from raylib.defines import KEY_DOWN, KEY_RIGHT

width, height = (800, 600)
camera = [0, 0]
block_scale = 20 

map_name = input("Choose the map name: ")
map = np.zeros((10,10))
def load(map, name):
    global camera
    path = "maps/" + name
    if not os.path.exists(path):
        width = int(input("Insert the width: "))
        height = int(input("Insert the height: "))
        map = np.random.randint(0, 1, (width, height))
        map[0][:] = 1
        map[-1][:] = 1
        map[:, 0] = 1
        map[:,-1] = 1
    else:
        map = np.load(path)
    camera = [map.shape[0]*block_scale/2, map.shape[1]*block_scale/2]
    return map

colors = [
    (0, 0, 0, 255), # 0 empty tile
    (200, 200, 200, 255), # 1 Wall tile
    (255, 0, 255, 255), # 2 Spawn tile (where the player spawn)
    (100, 100, 100, 255), # 3 Floor tile,
    (100, 0, 0, 255), # 4 Enemy division
    (100, 200, 0, 255), # 5 Boss spawn
    (0, 100, 255, 255), # 6 Small boss spawn
    (200,150, 200, 255), # Inner wall
]

def drawMap(camera, map):
    size = map.shape
    scale = block_scale
    for i in range(size[0]):
        for j in range(size[1]):
            pos = (-camera[0]+i*scale, -camera[1]+j*scale)
            draw_rectangle(int(pos[0]),int(pos[1]), scale, scale, colors[map[i][j]])

def keyHandler(dt, camera, current_color):
    global block_scale
    vel = 100
    if (is_key_down(KEY_RIGHT)):
        camera[0] += dt*vel
    if (is_key_down(KEY_LEFT)):
        camera[0] -= dt*vel
    if (is_key_down(KEY_UP)):
        camera[1] -= dt*vel
    if (is_key_down(KEY_DOWN)):
        camera[1] += dt*vel
    if (is_key_down(KEY_S)):
        np.save("maps/" + map_name, map)
    if (is_key_down(KEY_MINUS)):
        block_scale -= 1
    if (is_key_down(KEY_EQUAL)):
        block_scale += 1

    for i in range(len(colors)):
        if is_key_down(KEY_ONE + i):
            current_color = i
    return current_color

def fillMap(pos):
    global map
    queue = []
    queue.append(pos)
    while len(queue) != 0:
        cPos = queue.pop()
        if (cPos[0] <= 1 or cPos[0] >= map.shape[0]-2 or cPos[1] <= 1 or cPos[1] >= map.shape[1]-2):
            continue

        if map[cPos[0]][cPos[1]] == 1 or map[cPos[0]][cPos[1]] == 3:
            continue
        map[cPos[0]][cPos[1]] = 3
        if map[cPos[0]+1][cPos[1]] == 0:
            queue.append((cPos[0]+1, cPos[1]))
        if map[cPos[0]-1][cPos[1]] == 0:
            queue.append((cPos[0]-1, cPos[1]))
        if map[cPos[0]][cPos[1]+1] == 0:
            queue.append((cPos[0], cPos[1]+1))
        if map[cPos[0]][cPos[1]-1] == 0:
            queue.append((cPos[0], cPos[1]-1))






       
def main():
    global map
    global camera
    global block_scale
    map = load(map, map_name)
    current_color = 0
    mousePos = (0,0)
    scrollSpeed = 2
    init_window(width, height, "raylib [core] example - basic window")

    set_target_fps(60)

    prevMousePos = get_mouse_position();
    while not window_should_close():
        dt = get_frame_time()        
        current_color = keyHandler(dt, camera, current_color)

        mousePos = get_mouse_position();

        if (is_key_pressed(KEY_P)):
            fillMap((int(camera[0]/block_scale+mousePos.x/block_scale), int(camera[1]/block_scale+mousePos.y/block_scale)))

        if (is_mouse_button_down(MOUSE_BUTTON_LEFT)):
            map[int(camera[0]/block_scale+mousePos.x/block_scale)][int(camera[1]/block_scale+mousePos.y/block_scale)] = current_color
        if (is_mouse_button_down(MOUSE_BUTTON_RIGHT)):
            camera = [camera[0]-(mousePos.x-prevMousePos.x), camera[1]-(mousePos.y - prevMousePos.y)]
        block_scale += (int)(get_mouse_wheel_move() * scrollSpeed);
        prevMousePos = mousePos


            
        begin_drawing()
        clear_background(BLACK)
        drawMap(camera, map)
        end_drawing()

    close_window()


if __name__ == '__main__':
    main()

np.save("maps/" + map_name, map)
