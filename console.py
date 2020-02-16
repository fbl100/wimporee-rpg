import os
import sys
import time

TEXT_DELAY = 0.02  # seconds


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

def parse_command(command_string):
    tokens = command_string.split(' ', 1)  # the 1 splits only the first instance of ' '
    command = tokens[0]
    arguments = None
    if len(tokens) > 1:
        arguments = tokens[1]

    return (command, arguments)


