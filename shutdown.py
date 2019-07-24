## shutdown script ##
import re, subprocess, operator
from functools import reduce

verbose_regex = re.compile(r"^(\d+\s*hours?)?\s*(?:,|and|, and)?\s*(\d+\s+?minutes?)?\s*(?:,|and|, and)?\s*(\d+\s*(?:seconds?)?)?$", re.I)
short_regex = re.compile(r"(?:(?:(\d{2}:)?(\d{2}:))?(\d{2}))$")

def filter_number(text):
    """Filters a number out of a string"""
    lst = [i for i in text if str.isdigit(i)]
    txt = reduce(operator.add, lst, '')
    return int(txt)

def remove_none(iterable, replacement = ""):
    """Removes None from an iterable and replaces it with `replacement`. Returns a map object"""
    return map(lambda s: s if s else replacement, iterable)

def parse_input(text):
    """Parses the input from console and returns the time in seconds"""
    verbose = verbose_regex.match(text)
    simple = short_regex.match(text)

    if verbose:
        groups = verbose.groups()
    elif simple: 
        groups = simple.groups()
    else:
        print("The string", text, "is not a valid time")
        return None

    withoutNone = remove_none(groups, "0")
    digits = tuple(map(filter_number, withoutNone))
    return digits[0] * 3600 + digits[1] * 60 + digits[2]

while True:
    text = input("Shut down in ")

    if text == "help" or text == "?":
        print("Type the time you wish the computer to shut down. These are your options:")
        print("[<number> hours] [<number> minutes] <number> [seconds]")
        print("[[hh:]mm:]ss")
        continue
    elif text == "q" or text == "quit" or text == "exit":
        break

    parsed = parse_input(text)
    if not parsed:
        continue
    # command to run: `shutdown -s -t parsed`
