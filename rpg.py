import sys
import time
import random

import os
import sys
import time

###################
# Useful Functions
###################


TEXT_DELAY = 0.03  # seconds
# This function will print text slowly, with a TEXT_DELAY (in seconds) delay between characters
# it mimics a typewriter effect, and adds a nice narrative effect to the game
def print_slowly(text):
    # for each character in the text
    for character in text:
        # write the caracter and flush() stdout to make sure it actually prints to the screen
        sys.stdout.write(character)
        sys.stdout.flush()
        # then wait TEXT_DELAY seconds
        time.sleep(TEXT_DELAY)

    # when finished, write a newline character (and flush)
    sys.stdout.write('\n')
    sys.stdout.flush()

# Clears the screen.  In Python is matters if you're running on Windows vs Mac (or Linux)
# which is why you check the os.name ('nt' is Windows)
def cls():
    os.system(('cls' if os.name == 'nt' else 'clear'))


#########################
# player data structure #
#########################
player = {
    'name': '',
    'hp': 10,
    'inventory': [],
    'damage': 0,
    'shield': 0
}

items = {
    'helmet': {
        'description': "Safety First!",
        'modifiers': {
            'shield': 5
        }
    },
    'axe': {
        'description': "This axe looks like it might be useful",
        'modifiers': {
            'damage': 5
        }
    },
    'lamp': {
        'description': "This isn't the type of lamp that Alladin found...",
        'modifiers': {}
    },
    'healing potion': {
        'description': "Restores 5 hp of health",
        'modifiers': {
            'hp': 5
        }
    }
}

enemies = {
    'gnome': {
        'description_text': 'an angry gnome',
        'attack_text': 'the gnome whacks your kneecaps',
        'damage': 5,
        'hp': 10,
    }

}

world = {
    'outside': {
        'description': "You are standing outside what appears to be an abandoned gold mine",
        'items': ['helmet'],
        'enemies': [],
        'exits': {
            'inside': {
                'require': ['helmet'],
            }
        }
    },
    'inside': {
        'description': "You are standing in the entrance to the mine",
        'items': ['axe', 'lamp'],
        'enemies': [],
        'exits': {
            'outside': {
                'require': [],
            },
            'into the darkness': {
                'require': ['lamp']
            }
        }
    },
    'into the darkness': {
        'description': "You are standing the darkness..",
        'items': [],
        'enemies': ['gnome'],
        'exits': {
            'inside': {
                'require': [],
            }
        }
    }
}

##### GAME STATE VARIABLES #####
CURRENT_ROOM = 'outside'
##### GAME STATE VARIABLES #####

#
def setup_game():
    print_slowly("Hello there, what is your name?")
    player['name'] = input("> ")


def process_go(arg):
    global CURRENT_ROOM
    if arg in world[CURRENT_ROOM]['exits']:
        next_room = world[CURRENT_ROOM]['exits'][arg]

        for required_item in next_room['require']:
            if required_item not in player['inventory']:
                print_slowly("You do not have a " + required_item)
                return

        CURRENT_ROOM = arg
    else:
        print_slowly("that isn't really an option")


def pickup_item(item):
    if item in world[CURRENT_ROOM]['items']:
        player['inventory'].append(item)
        world[CURRENT_ROOM]['items'].remove(item)

        for stat in items[item]['modifiers'].keys():
            increment = items[item]['modifiers'][stat]
            player[stat] += increment

    else:
        print_slowly("I don't see a " + item)


def drop_item(item):
    if item in player['inventory']:
        player['inventory'].remove(item)
        world[CURRENT_ROOM]['items'].append(item)

        for stat in items[item]['modifiers'].keys():
            increment = items[item]['modifiers'][stat]
            player[stat] -= increment

    else:
        print_slowly("you don't have a " + item)


def process_look(arg):
    if arg is None:
        # list the item descriptions
        print_slowly("what do you want to look at?")
    elif arg not in items:
        print_slowly("I don't see one of those")
    else:
        item = items[arg]
        print_slowly(item['description'])


def print_player(args):
    print("###############################")
    print("# Player : " + player['name'])
    print("# HP     : " + str(player['hp']))
    print("# Damage : " + str(player['damage']))
    print("# Shield : " + str(player['shield']))
    print("# Inventory ")
    for item in player['inventory']:
        print("#   " + item)
    print("###############################")

def command_quit(arg):
    print_slowly("Abandon ye all hope, for you have quit...")
    exit(0)

command_dispatch = {
    # syntax: go [exit]
    'go': process_go,
    # syntax: look
    'look': process_look,
    'stats': print_player,
    'pickup': pickup_item,
    'drop': drop_item,
    'quit': command_quit
}


def print_situation():
    print("######################################")
    print_slowly(world[CURRENT_ROOM]['description'])
    print("")
    print_slowly("You see:")
    for item in world[CURRENT_ROOM]['items']:
        print_slowly("    " + item)

    exits = list(world[CURRENT_ROOM]['exits'].keys())

    print_slowly("exits: " + ", ".join(exits))


def do_combat():
    global CURRENT_ROOM
    print("An Encounter!")

    for enemy_type in world[CURRENT_ROOM]['enemies']:
        print("You must do battle with a " + enemy_type + "!!!")
        enemy = enemies[enemy_type].copy()

        while enemy['hp'] > 0 and player['hp'] > 0:
            command = input("[attack|run] > ")
            if command == 'attack':
                damage = player['damage']
                print("you attack the {} dealing {} damage".format(enemy_type, damage))
                enemy['hp'] -= damage
            elif command == 'run':
                print("you make a run for it!")
                exit = list(world[CURRENT_ROOM]['exits'].keys())[0]
                CURRENT_ROOM = exit
                return

            if enemy['hp'] > 0:
                # monster attacks
                enemy_damage = enemy['damage']
                print("{} dealing {} damage".format(enemy['attack_text'], enemy_damage))
                player['hp'] -= enemy_damage

            print("{} has {} hp".format(player['name'], player['hp']))
            print("{} has {} hp".format(enemy_type, enemy['hp']))

        if player['hp'] <= 0:
            print("you died")
        elif enemy['hp'] <= 0:
            print("you killed the {}".format(enemy_type))
            # maybe give the player some gold?
            world[CURRENT_ROOM]['enemies'].remove(enemy_type)

        print()


def prompt():
    if len(world[CURRENT_ROOM]['enemies']) > 0:
        # combat!
        do_combat()
        if player['hp'] <= 0:
            return

    print_situation()
    user_input = input("{} > ".format(", ".join(list(command_dispatch.keys()))))
    # split the first word out, that is our action
    tokens = user_input.split(' ', 1)  # the 1 splits only the first instance of ' '
    command = tokens[0]
    if command not in command_dispatch:
        print("unknown command")
    else:
        arguments = None
        if len(tokens) > 1:
            arguments = tokens[1]
        command_dispatch[command]((arguments))


def game_loop():
    while player['hp'] > 0:
        prompt()


setup_game()
game_loop()
