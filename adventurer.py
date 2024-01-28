import pygame
import numpy as np
import keyboard
import sys

map_data_file = 'maps/map1/map.dat'
item_data_file = 'maps/map1/item.dat'
map_data = np.loadtxt(map_data_file, dtype=int)
item_data = np.loadtxt(item_data_file, dtype=int)
mob_data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])

map_data = np.array(map_data)
print("Swap x & y:")
print(map_data.T)
map_data = map_data.T
# mapdata[x, y]で取得できる

# 5x5で探索するメソッド
# 返り値はマップ情報、アイテム情報、モブ（プレイヤー、妨害キャラクターの座標）
def search(point: np.array):
    x = point[0]
    y = point[1]
    map_5x5 = map_data[x-2:x+3, y-2:y+3]
    item_5x5 = item_data[x-2:x+3, y-2:y+3]
    mob_5x5 = mob_data[x-2:x+3, y-2:y+3]

    return map_5x5, item_5x5, mob_data

print(search([2,2]))

PLAYER1 = []
PLAYER2 = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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

def is_in_grid(x, y):
    """
        x, yがグリッドワールド内かの確認
    """
    if len(map_data) > y >= 0:
        if len(map_data[0]) > x  >= 0:
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
    for x in range(15):
        for y in range(15):
            color = WHITE
            if [x, y] == PLAYER1:
                print("LOGGER:  PLAYER1_POSITION: ", [x, y])
                color = RED
            elif [x, y] == PLAYER2:
                print("LOGGER:  PLAYER2_POSITION: ", [x, y])
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * x + MARGIN,
                              (MARGIN + HEIGHT) * y + MARGIN,
                              WIDTH,
                              HEIGHT])

if __name__ == '__main__':

    # pygameの初期化
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("15x15 Grid")

    clock = pygame.time.Clock()

    # プレイヤー1の初期位置
    x1, y1 = np.random.randint(15), np.random.randint(15)
    PLAYER1 = [x1, y1]

    # プレイヤー2の初期位置
    x2, y2 = np.random.randint(15), np.random.randint(15)
    PLAYER2 = [x2, y2]

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

        # プレイヤーの座標の更新
        to_x, to_y = update_agent_pos(PLAYER1[0], PLAYER1[1])

        PLAYER1 = [to_x, to_y]

        to_x, to_y = update_agent_pos(PLAYER2[0], PLAYER2[1])

        PLAYER2 = [to_x, to_y]

        clock.tick(1)


