#########################
# player data structure #
#########################
import random

from console import print_slowly

player_templates = {
    'fighter': {
        'type': 'player',
        'name': '',
        'hp': [10, 12],
        'ac': [5, 10],
        'damage_die': [1,1],
        'inventory': {}
    }
}


def set_stat(enemy, stat):
    min = enemy[stat][0]
    max = enemy[stat][1]
    enemy[stat] = random.randint(min, max)

def create_player(player_name = None, player_type = None):

    if player_name is None:
        print_slowly("Hello, what is your name?")
        player_name = input("> ")

    while player_type not in player_templates:
        print_slowly("What type of player are you?")
        player_type = input("{} > ".format(" -*- ".join(list(player_templates.keys()))))

    player = player_templates[player_type].copy()
    player['name'] = player_name
    # replace ac, strength, and hp with values
    set_stat(player, 'ac')
    set_stat(player, 'damage_die')
    set_stat(player, 'hp')
    return player

# def print_player(enemy):
#     print("{}\t{} / {} / {}".format(enemy['description_text'], enemy['hp'], enemy['strength'], enemy['ac']))

def print_player(player):
    print("###################################")
    print("# Player     : " + player['name'])
    print("# HP         : " + str(player['hp']))
    print("# AC         : " + str(player['ac']))
    print("# Damage Die : " + str(player['damage_die']))
    print("# Inventory ")
    for item in player['inventory']:
        print("#   " + item)
    print("###################################")


# @test
# player = create_player(player_name='Frank', player_type='fighter')
# print_player(player)
