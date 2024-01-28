import pygame
import numpy as np
import keyboard
import sys


mapdata_file = 'maps/map1/map.dat'
itemdata_file = 'maps/map1/item.dat'
map_data = np.loadtxt(mapdata_file, dtype=int)

print(np.array(map_data))
print("Swap x & y:")
print(np.array(map_data).T)
map_data = np.array(map_data).T
# mapdata[x, y]で取得できる
print(map_data[7, 13])

def search(p: np.array):
    x = p[0]
    y = p[1]
    map_5x5 = map_data[x-2:x+3, y-2:y+3]
    return map_5x5

print (search([2,2]))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 40, 40

WINDOW_SIZE = [680, 680]

MARGIN = 5

# 行動の集合
ACTIONS = {
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT": 3}

# フレーム数
clock = pygame.time.Clock()
# フレームレートの上限設定
fps_limit = 30

def is_in_grid(x, y):
    """
        x, yがグリッドワールド内かの確認
    """
    if len(grid) > y >= 0:
        if len(grid[0]) > x  >= 0:
            return True
    return False

def update_agent_pos(x, y):
    """
        エージェントの位置の更新 
    """
    while True:
        to_y, to_x = y, x
        action = np.random.randint(4)
        if action == ACTIONS["UP"]:
            to_y += -1
        elif action == ACTIONS["DOWN"]:
            to_y += 1
        elif action == ACTIONS["LEFT"]:
            to_x += -1
        elif action == ACTIONS["RIGHT"]:
            to_x += 1

        if is_in_grid(to_y, to_x) is True:
            return to_x, to_y

def draw_grid_world():
    """
        grid world自体の再描画
    """
    for row in range(15):
        for column in range(15):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

if __name__ == '__main__':

    # pygameの初期化
    pygame.init()

    # grid情報の初期化
    grid = []
    for row in range(15):
        grid.append([])
        for column in range(15):
            grid[row].append(0)

    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("15x15 Grid")

    clock = pygame.time.Clock()

    # エージェントの初期位置
    x, y = 1, 5
    grid[y][x] = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if keyboard.is_pressed('escape'):
            pygame.quit()
            sys.exit()
        
        screen.fill(BLACK)

        # grid worldの描画
        draw_grid_world()

        # 再描画
        pygame.display.update()

        # エージェントの位置の更新
        to_x, to_y = update_agent_pos(x, y)

        grid[y][x] = 0
        grid[to_y][to_x] = 1
        x, y = to_x, to_y

        clock.tick(1)


