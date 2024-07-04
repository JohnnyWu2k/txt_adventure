import os
import time
import pygame
import importlib.util

# 初始化音效
pygame.mixer.init()

# 获取当前脚本的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建相对路径
maps_dir = os.path.join(current_dir, 'maps')
sounds_dir = os.path.join(current_dir, 'sounds')
mods_dir = os.path.join(current_dir, 'mods')

# 定义游戏元素
player_pos = [2, 4]
player_health = 100
player_score = 0
current_level = 0
player_inventory = []
maps = []
new_item = None
new_item2 = None
additional_menu_options = []

# 清除终端
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# 显示地图
def display_map():
    clear_terminal()
    for y, row in enumerate(maps[current_level]):
        for x, char in enumerate(row):
            if [y, x] == player_pos:
                print("P", end="")
            else:
                print(char, end="")
        print()
    print(f"Health: {player_health}  Score: {player_score}  Inventory: {player_inventory}")

# 播放音效
def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# 移动玩家
def move_player(direction):
    global player_pos, player_health, player_score, current_level
    y, x = player_pos
    new_y, new_x = y, x
    if direction == "w" and y > 0 and maps[current_level][y-1][x] != "#":
        new_y -= 1
    elif direction == "s" and y < len(maps[current_level]) - 1 and maps[current_level][y+1][x] != "#":
        new_y += 1
    elif direction == "a" and x > 0 and maps[current_level][y][x-1] != "#":
        new_x -= 1
    elif direction == "d" and x < len(maps[current_level][y]) - 1 and maps[current_level][y][x+1] != "#":
        new_x += 1

    handle_interaction(new_y, new_x)
    player_pos = [new_y, new_x]

# 处理交互
def handle_interaction(y, x):
    global player_health, player_score, current_level
    cell = maps[current_level][y][x]
    if cell == "T":
        player_score += 10
        play_sound(os.path.join(sounds_dir, "victory.wav"))
        print("You found the treasure!")
        time.sleep(1)
        level_up()
    elif cell == "E":
        player_health -= 20
        play_sound(os.path.join(sounds_dir, "enemy.wav"))
        if player_health <= 0:
            play_sound(os.path.join(sounds_dir, "defeat.wav"))
            print("You were defeated by an enemy! Game Over!")
            exit()
        else:
            print("You encountered an enemy!")
            time.sleep(1)
    elif cell == "K":
        player_inventory.append("Key")
        play_sound(os.path.join(sounds_dir, "key.wav"))
        print("You found a key!")
        time.sleep(1)
        update_map(y, x, " ")
    elif cell == "D":
        if "Key" in player_inventory:
            play_sound(os.path.join(sounds_dir, "door.wav"))
            print("You used a key to open the door!")
            player_inventory.remove("Key")
            time.sleep(1)
            update_map(y, x, " ")
        else:
            print("The door is locked. You need a key.")
            time.sleep(1)
            return False
    return True

# 更新地图
def update_map(y, x, new_char):
    global maps
    maps[current_level][y] = maps[current_level][y][:x] + new_char + maps[current_level][y][x+1:]

# 升级关卡
def level_up():
    global current_level, player_pos
    if current_level < len(maps) - 1:
        current_level += 1
        # 确保地图包含玩家位置
        for y, row in enumerate(maps[current_level]):
            if 'P' in row:
                player_pos = [y, row.index('P')]
                break
    else:
        print("Congratulations! You completed all levels!")
        exit()

# 加载地图
def load_map():
    global maps, player_pos
    map_files = os.listdir(maps_dir)
    print("Available maps:")
    for i, map_file in enumerate(map_files):
        print(f"{i+1}. {map_file}")
    choice = int(input("Select a map to load: ")) - 1
    if choice >= 0 and choice < len(map_files):
        map_file = map_files[choice]
        with open(os.path.join(maps_dir, map_file), "r") as f:
            new_map = [line.replace('P', ' ') for line in f.read().splitlines()]
            maps = [new_map]
        for y, row in enumerate(maps[0]):
            if 'P' in row:
                player_pos = [y, row.index('P')]
                break
        main_game_loop()
    else:
        print("Invalid choice. Returning to main menu.")
        time.sleep(1)
        main_menu()

# 加载mods
def load_mods():
    mod_files = os.listdir(mods_dir)
    for mod_file in mod_files:
        if mod_file.endswith(".py"):
            mod_path = os.path.join(mods_dir, mod_file)
            spec = importlib.util.spec_from_file_location(mod_file[:-3], mod_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.apply_mod(globals())

# 主菜单
def main_menu():
    load_mods()
    while True:
        clear_terminal()
        print("Welcome to Adventure Game!")
        print("1. Start New Game")
        print("2. Load Map")
        for i, option in enumerate(additional_menu_options):
            print(f"{i+3}. {option[0]}")
        print(f"{len(additional_menu_options) + 3}. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            start_new_game()
        elif choice == "2":
            load_map()
        elif choice == str(len(additional_menu_options) + 3):
            exit()
        else:
            for i, option in enumerate(additional_menu_options):
                if choice == str(i + 3):
                    option[1]()
                    break
            else:
                print("Invalid choice, please try again.")
                time.sleep(1)

# 开始新游戏
def start_new_game():
    global player_pos, player_health, player_score, current_level, player_inventory, maps
    map_files = ["map1.txt", "map2.txt"]
    maps = []
    for map_file in map_files:
        with open(os.path.join(maps_dir, map_file), "r") as f:
            maps.append([line.replace('P', ' ') for line in f.read().splitlines()])
    player_pos = [2, 4]
    player_health = 100
    player_score = 0
    current_level = 0
    player_inventory = []
    main_game_loop()

# 主游戏循环
def main_game_loop():
    while True:
        display_map()
        move = input("Move (w/a/s/d): ").lower()
        if move in ["w", "a", "s", "d"]:
            move_player(move)
        else:
            print("Invalid input, use w/a/s/d to move.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
