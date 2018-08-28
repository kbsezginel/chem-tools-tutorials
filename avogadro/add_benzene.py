"""
Avogadro 2 basic plug-in example for generating molecules.
- Add a benzene molecule
"""
import os
import sys
import json
import argparse

# Some globals:
debug = True
benzene_xyz = """12
benzene
C  -0.0000  1.4027  0.0000
H  -0.0000  2.4903  0.0000
C  -1.2148  0.7014  0.0000
H  -2.1567  1.2451  0.0000
C  -1.2148 -0.7014  0.0000
H  -2.1567 -1.2451  0.0000
C  -0.0000 -1.4027  0.0000
H  -0.0000 -2.4903  0.0000
C   1.2148 -0.7014  0.0000
H   2.1567 -1.2451  0.0000
C   1.2148  0.7014  0.0000
H   2.1567  1.2451  0.0000"""


def get_options():
    return {}


def run_command():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = {'append': True,
              'moleculeFormat': 'xyz',
              'xyz': benzene_xyz}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Add a benzene molecule')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Add Benzene")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_command()))
