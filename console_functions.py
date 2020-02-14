import os
import sys
import time

TEXT_DELAY = 0.03  # seconds

def print_slowly(text):
    for character in text:
        # This will occur throughout the intro code.  It allows the string to be typed gradually - like a typerwriter
        # effect.
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(TEXT_DELAY)
    sys.stdout.write('\n')
    sys.stdout.flush()


def cls():
    os.system(('cls' if os.name == 'nt' else 'clear'))
