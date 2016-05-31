#!/usr/bin/env python
# from  ajaymenon.k
# http://code.activestate.com/recipes/578169-extremely-strong-password-generator/?in=lang-python
from os import urandom
from random import choice
from subprocess import Popen, PIPE
import sys

char_set = {'small': 'abcdefghijklmnopqrstuvwxyz',
            'nums': '0123456789',
            'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'special': '^!\$%&/()=?{[]}+~#-_.:,;<>|\\'
            }


def generate_pass(length=21):
    """Function to generate a password"""

    password = []

    while len(password) < length:
        key = choice(char_set.keys())
        a_char = urandom(1)
        if a_char in char_set[key]:
            if check_prev_char(password, char_set[key]):
                continue
            else:
                password.append(a_char)
    return ''.join(password)


def check_prev_char(password, current_char_set):
    """Function to ensure that there are no consecutive
    UPPERCASE/lowercase/numbers/special-characters."""

    index = len(password)
    if index == 0:
        return False
    else:
        prev_char = password[index - 1]
        if prev_char in current_char_set:
            return True
        else:
            return False


def usage(good_args=True):
    if not good_args:
        print "Please check your arguments"

    print '''help:
    {f} -h \t# show this help
    {f} -c \t# copy password to clipboard
    {f} -s \t# show password in stdout
    '''.format(f=__file__)


def paste_clip(generate_pass):
    print "Password is copied into your clipboard"
    p = Popen(['xsel', '-bi'], stdin=PIPE)
    p.communicate(input=generate_pass())


def paste_stdout(generate_pass):
    print "Password:"
    print generate_pass()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage(False)
        exit(-1)

    switcher = {
        '-h': lambda: usage(True),
        '-s': lambda: paste_stdout(generate_pass),
        '-c': lambda: paste_clip(generate_pass)
    }
    func = switcher.get(sys.argv[1], lambda: usage(False))
    func()
