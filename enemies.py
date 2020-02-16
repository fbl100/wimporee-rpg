import random

enemies_templates = {
    'gnome': {
        'type': 'enemy',
        'name': 'gnome',
        'attack_text': 'the gnome whacks your kneecaps',
        'ac': [4, 4],
        'damage_die': [1,1],
        'hp': [5, 10],
    },
    'dragon': {
        'type': 'enemy',
        'name': 'dragon',
        'attack_text': 'the gnome whacks your kneecaps',
        'ac': [14, 18],
        'damage_die': [4,4],
        'hp': [50, 100],
    }
}


def set_stat(enemy, stat):
    min = enemy[stat][0]
    max = enemy[stat][1]
    enemy[stat] = random.randint(min, max)


def create_enemy(enemy_type):
    enemy = enemies_templates[enemy_type].copy()
    # replace ac, strength, and hp with values
    set_stat(enemy, 'ac')
    set_stat(enemy, 'damage_die')
    set_stat(enemy, 'hp')
    return enemy

def print_enemy(enemy):
    print("{}\t{} / {} / {}".format(enemy['description_text'], enemy['hp'], enemy['strength'], enemy['ac']))
