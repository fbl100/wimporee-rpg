#########################
# player data structure #
#########################
import random

from items import items_list
from combat import process_combat, process_attack
from console import print_slowly, parse_command
from enemies import create_enemy
from player import create_player, print_player


world = {
    'outside': {
        'description': "You are standing outside what appears to be an abandoned gold mine",
        'items': ['helmet'],
        'possible_enemies' : [],
        # list of actual enemies in the room
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
        # list of possible enemies
        'possible_enemies' : [{
            'type': 'gnome',
            'spawn_chance': 50
        }],
        # list of actual enemies in the room
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
        'description': "You are standing in the darkness..",
        'items': [],
        'possible_enemies' : [{
            'type': 'dragon',
            'spawn_chance': 100
        }],
        # list of actual enemies in the room
        'enemies': [],
        'exits': {
            'inside': {
                'require': [],
            }
        }
    }
}

##### GAME STATE VARIABLES #####
CURRENT_ROOM = 'outside'
player = create_player('Frank', 'fighter')


##### GAME STATE VARIABLES #####

def command_go(to_room):
    global CURRENT_ROOM
    # is the destination room in the list of exists?
    if to_room in world[CURRENT_ROOM]['exits']:
        next_room = world[CURRENT_ROOM]['exits'][to_room]
        # check to make sure that we have any required items to use this exit
        for required_item in next_room['require']:
            if required_item not in player['inventory']:
                print_slowly("You do not have a " + required_item)
                return


        if len(world[to_room]['enemies']) == 0:
            # there are no enemies in the room
            # spawn some
            for enemy_type in world[to_room]['possible_enemies']:
                if random.randint(0,100) < enemy_type['spawn_chance']:
                    print('spawned {}'.format(enemy_type['type']))
                    world[to_room]['enemies'].append( create_enemy(enemy_type['type']))

        CURRENT_ROOM = to_room
    else:
        print_slowly("that isn't really an option")

def give_item(item):
    player['inventory'][item] = items_list[item].copy()

def command_pickup(item):
    if item in world[CURRENT_ROOM]['items']:
        give_item(item)
        world[CURRENT_ROOM]['items'].remove(item)
    else:
        print_slowly("I don't see a " + item)


def command_drop(item_name):
    if item_name in player['inventory']:
        player['inventory'].remove(item_name)
        world[CURRENT_ROOM]['items'].append(item_name)
    else:
        print_slowly("you don't have a " + item_name)


def command_look(arg):
    if arg is None:
        # list the item descriptions
        print_slowly("what do you want to look at?")
    elif arg not in world[CURRENT_ROOM]['items']:
        print_slowly("I don't see one of those")
    else:
        item = items_list[arg]
        print_slowly(item['description'])


def command_stats(args):
    print_player(player)


def command_quit(arg):
    print_slowly("Abandon ye all hope, for you have quit...")
    exit(0)


command_dispatch = {
    'go': command_go,
    'look': command_look,
    'stats': command_stats,
    'pickup': command_pickup,
    'drop': command_drop,
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
    room_enemies = world[CURRENT_ROOM]['enemies']
    combat_result = process_combat(player, room_enemies[0])
    if combat_result == 'run':
        next_room = list(world[CURRENT_ROOM]['exits'].keys())[0]
        CURRENT_ROOM = next_room
    elif combat_result == 'complete':
        # combat is complete
        if player['hp'] <= 0:
            return
        if room_enemies[0]['hp'] <= 0:
            room_enemies.clear()

def process_user_input(user_input):
    # split the first word out, that is our action
    (command, arguments) = parse_command(user_input)
    command_dispatch[command]((arguments))


def prompt():
    if len(world[CURRENT_ROOM]['enemies']) > 0:
        # combat!
        do_combat()
        if player['hp'] <= 0:
            return

    print_situation()
    user_input = input("{} > ".format(", ".join(list(command_dispatch.keys()))))

    process_user_input(user_input)


def game_loop():

    while player['hp'] > 0:
        prompt()
        if len(world[CURRENT_ROOM]['enemies']) > 0:
            do_combat()

#test
player = create_player()
# give_item('helmet')
# give_item('axe')
# enemy = create_enemy('gnome')
#
# process_attack(player, enemy)

game_loop()
#
# player = create_player('Frank', 'fighter')
# enemy = create_enemy('gnome')
# process_combat(player, [enemy])
# # CURRENT_ROOM = 'outside'
#
# game_loop()
