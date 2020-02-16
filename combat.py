import random

from console import parse_command, print_slowly
from enemies import create_enemy
from player import create_player


def determine_combat_order(player, enemy):
    # put everyone into a list
    if random.randint(0, 1) == 0:
        return [player, enemy]
    else:
        return [enemy, player]


def hit(ac):
    return random.randint(1, 20) > ac


def get_stat(entity, stat):
    base = entity[stat]
    if 'inventory' in entity:
        for inventory_item in entity['inventory'].values():
            if stat in inventory_item:
                base += inventory_item[stat]
    return base


def process_attack(attacker, defender):
    if defender['hp'] <= 0:
        # defender is already dead
        return

    # get the ac from the defender
    ac = get_stat(defender, 'ac')

    if hit(ac):
        damage = 0
        num_damage_die = get_stat(attacker, 'damage_die')
        for die in range(0, num_damage_die):
            damage += random.randint(1, 6)
        print_slowly("{} attacks {} and deals {} damage!".format(attacker['name'], defender['name'], damage))
        defender['hp'] -= damage
        if defender['hp'] <= 0:
            defender['hp'] = 0
            print_slowly("{} died".format(defender['name']))
    else:
        print_slowly("{} attacks {} and misses".format(attacker['name'], defender['name']))


def process_combat(player, enemy):
    print_slowly("A {} has appeared!  You must do battle!".format(enemy['name']))
    # determine the order that everyone attacks
    combat_list = determine_combat_order(player, enemy)

    while player['hp'] > 0 and enemy['hp'] > 0:
        for participant in combat_list:
            if participant['hp'] > 0:
                # player is alive
                if participant['type'] is 'player':
                    user_input = input("[attack|run] > ")
                    if user_input == 'attack':
                        process_attack(player, enemy)
                    elif user_input == 'run':
                        return "run"
                    else:
                        print("sorry, you can't do that")
                else:
                    process_attack(enemy, player)
        print("{} has {} hp remaining".format(player['name'], player['hp']))
        print("{} has {} hp remaining".format(enemy['name'], enemy['hp']))

    return 'complete'
