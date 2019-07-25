## shutdown script ##
import re, subprocess, operator, platform
from functools import reduce
from typing import Iterator, List, Optional

# matches queries of the format [<number> hours] [,] [and] [<number> minutes] [,] [and] <number> [seconds]
verbose_regex = re.compile(r"^(\d+\s*hours?)?\s*(?:,|and|, and)?\s*(\d+\s+?minutes?)?\s*(?:,|and|, and)?\s*(\d+\s*(?:seconds?)?)?$", re.I)
# matches queries of the format [[hh:]mm:]ss
short_regex = re.compile(r"(?:(?:(\d{2}:)?(\d{2}:))?(\d{2}))$")
# TODO: add ability to shutdown at absolute hour
#abs_regex = re.compile(r"@(?:(?:(\d{2}:)?(\d{2}:))?(\d{2}))$")

def filter_number(text: str) -> int:
    """Filters a number out of a string"""
    lst = [i for i in text if str.isdigit(i)]
    txt = reduce(operator.add, lst, '')

    assert txt != '', 'Make sure the input contains a number!'
    return int(txt)

def remove_none(iterable: Iterator[Optional[str]], replacement = "") -> Iterator[str]:
    """Removes None from an iterable and replaces it with `replacement`. Returns a map object"""
    return map(lambda s: s if s else replacement, iterable)

def parse_input(text: str) -> Optional[int]:
    """Parses the input from console and returns the time in seconds"""
    # This step will be simplified in Python 3.8 when the := syntax gets stabilised
    verbose = verbose_regex.match(text)
    simple = short_regex.match(text)

    if verbose:
        groups = verbose.groups()
    elif simple: 
        groups = simple.groups()
    else:
        return None

    withoutNone = remove_none(iter(groups), "0")
    digits = tuple(map(filter_number, withoutNone))
    return digits[0] * 3600 + digits[1] * 60 + digits[2]

while True:
    text = input("Shut down in ")

    if text in ["help", "?"]:
        print("Type the time you wish the computer to shut down. These are your options:")
        print("[<number> hours] [<number> minutes] <number> [seconds]")
        print("[[hh:]mm:]ss")
        continue
    elif text in ["q", "quit", "exit"]:
        break

    parsed = parse_input(text)
    if not parsed:
        print(f'The string "{text}" is not a valid time')
        continue
    
    system = platform.system()

    if system == 'Windows':
        cmd = f'shutdown /s /t {parsed}'

    elif system == 'Linux':
        cmd = f'sudo shutdown -h -t {parsed}'

    elif system == 'Darwin': # shutdown on OSX doesn't run on seconds
        print('Converting to nearest minutes')
        time = parsed // 60
        # add extra minute in case it's not in whole minutes
        if parsed % 60 > 0:
            time += 1
        cmd = f'sudo shutdown -h +{time}'

    else:
        print(f'Script not supported on {system}.')
        break
    
    print('Running', cmd)
    subprocess.Popen(cmd.split(), stdout = subprocess.PIPE)
    
    # On Windows, keep the terminal window open
    if system == 'Windows':
        input('Press any key to continue...')

    break