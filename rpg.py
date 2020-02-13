import sys
import time
import random

TEXT_DELAY = 0.01  # seconds

CURRENT_ROOM = 'entry_hall'

#########################
# player data structure #
#########################
player = {
    'name': '',
    'row': 0,
    'col': 0,
    'won': False,
    'hp': 10,
    'victories': 0
}

enemies = {
    'jello_cube': {
        'description_text': 'A cube of jello stands before you... jiggling',
        'attack_text': 'The jello jiggles at you... and jiggles',
        'flee_text': 'The jello quietly oozes away, never to be seen again',
        "kill_text": "You vanquish the jello, aren't you proud of yourself?",
        'damage': 0,
        'critical_damage': 0,
        'hp': 1,
    }
}

map = {
    'entry_hall': {
        'description': "You are standing in the entry hall",
        'info': "You can go into the parlor, the library, or upstairs",
        'actions': {
            'parlor': 'parlor',
            'library': 'library',
            'upstairs': 'upstairs',
        },
        'encounter_probability': 0.0
    },
    'parlor': {
        'description': "Hey look, it's a parlor",
        'info': "You can go into the entry hall or the kitchen",
        'actions': {
            'entry hall': 'entry_hall',
            'kitchen': 'kitchen'
        },
        'encounter_probability': 0.0
    },
    'library': {
        'description': "You're in the library, and it smells like books",
        'info': "nothing to see here",
        'actions': {
            'parlor': 'parlor',
            'library': 'library',
            'upstairs': 'upstairs',
        },
        'encounter_probability': 0.0
    },
    'upstairs': {
        'description': "Upstairs is nice.. you kinda wish you were downstairs though",
        'info': "There is a rug in the middle of the floor",
        'actions': {
            'downstairs': 'entry_hall'
        },
        'encounter_probability': 0.0
    },
    'kitchen': {
        'description': "you are in the kitchen",
        'info': "you can go back to the parlor from here",
        'actions': {
            'parlor': 'parlor'
        },
        'encounter_probability': 1.0
    }

}

# this function will print text slowly, with a delay of 0.05 seconds
def print_slowly(text):
    for character in text:
        # This will occur throughout the intro code.  It allows the string to be typed gradually - like a typerwriter
        # effect.
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(TEXT_DELAY)
    sys.stdout.write('\n')
    sys.stdout.flush()


def setup_game():
    print_slowly("Hello there, what is your name?")
    player['name'] = input("> ")
    print_slowly("Hi " + player['name'] + ", how are you feeling today?")
    player['mood'] = input("> ")

def encounter():
    enemy = enemies['jello_cube'].copy()
    print_slowly("An Encounter!")
    print_slowly(enemy['description_text'])
    encounter_over = False
    while encounter_over is False:
        # player goes first
        print_slowly("Actions: attack, run")
        player_move = input("> ")
        if player_move == "attack":
            if random.uniform(0,1) > 0.5:
                enemy['hp'] -= 1
                print_slowly("Hit!  Enemy now has " + str(enemy['hp']) + " hp")
            else:
                print_slowly("you missed")
        if player_move == "run":
            print_slowly("coward")
            encounter_over = True
            map[CURRENT_ROOM]['encounter_probability'] = 0.0

        if enemy['hp'] <= 0:
            print_slowly(enemy['kill_text'])
            encounter_over = True
            map[CURRENT_ROOM]['encounter_probability'] = 0.0
        else:
            # monster moves
            if random.uniform(0,1) > 0.05:
                print_slowly(enemy['attack_text'])
                player['hp'] -= 1
            else:
                print_slowly(enemy['flee_text'])

def process_go(arg):
    print("going " + arg)

def process_look(arg):
    print("looking at " + arg)

def process_combat(arg):
    print("combat")


command_dispatch = {
    'go' : process_go,
    'look' : process_look
}

def prompt():
    global CURRENT_ROOM
    rand = random.uniform(0.0,1.0)
    if map[CURRENT_ROOM]['encounter_probability'] > rand:
        encounter()
    print_slowly(map[CURRENT_ROOM]['description'])
    user_input = input("> ")
    tokens = user_input.split(' ', 1)
    action = tokens[0]

    if tokens[0] in command_dispatch:
        command_dispatch[tokens[0]](tokens[1])

    if user_input == "look":
        print_slowly(map[CURRENT_ROOM]['info'])
    elif user_input in map[CURRENT_ROOM]['actions']:
        CURRENT_ROOM = map[CURRENT_ROOM]['actions'][user_input]
    else:
        print_slowly("I'm sorry, I don't know what you want to to...")

    for room in map.keys():
        map[room]['encounter_probability'] += 0.10

def game_loop():
    while player['won'] is False:
        CURRENT_ROOM = prompt()


setup_game()
game_loop()
