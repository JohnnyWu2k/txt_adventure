import random
import time
import os

def apply_mod(game_globals):
    # 替换 handle_interaction 函数以添加战斗逻辑
    original_handle_interaction = game_globals['handle_interaction']

    def handle_interaction(y, x):
        global player_health, player_score, current_level, player_inventory
        cell = game_globals['maps'][game_globals['current_level']][y][x]
        if cell == "T":
            game_globals['player_score'] += 10
            game_globals['play_sound'](os.path.join(game_globals['sounds_dir'], "victory.wav"))
            print("You found the treasure!")
            time.sleep(1)
            game_globals['level_up']()
        elif cell == "E":
            game_globals['play_sound'](os.path.join(game_globals['sounds_dir'], "enemy.wav"))
            print("You encountered an enemy!")
            battle()
        elif cell == "K":
            game_globals['player_inventory'].append("Key")
            game_globals['play_sound'](os.path.join(game_globals['sounds_dir'], "key.wav"))
            print("You found a key!")
            time.sleep(1)
            game_globals['update_map'](y, x, " ")
        elif cell == "D":
            if "Key" in game_globals['player_inventory']:
                game_globals['play_sound'](os.path.join(game_globals['sounds_dir'], "door.wav"))
                print("You used a key to open the door!")
                game_globals['player_inventory'].remove("Key")
                time.sleep(1)
                game_globals['update_map'](y, x, " ")
            else:
                print("The door is locked. You need a key.")
                time.sleep(1)
                return False
        return True

    def battle():
        global player_health
        enemy_health = 100
        while game_globals['player_health'] > 0 and enemy_health > 0:
            print("1. Rock\n2. Paper\n3. Scissors")
            player_choice = input("Choose your move: ")
            enemy_choice = random.choice(["1", "2", "3"])
            if player_choice == enemy_choice:
                print("It's a tie!")
            elif (player_choice == "1" and enemy_choice == "3") or (player_choice == "2" and enemy_choice == "1") or (player_choice == "3" and enemy_choice == "2"):
                print("You hit the enemy!")
                enemy_health -= 20
            else:
                print("The enemy hits you!")
                game_globals['player_health'] -= 20
            print(f"Your health: {game_globals['player_health']}, Enemy health: {enemy_health}")
            time.sleep(1)
        if game_globals['player_health'] <= 0:
            print("You were defeated by the enemy! Game Over!")
            exit()
        else:
            print("You defeated the enemy!")

    game_globals['handle_interaction'] = handle_interaction
