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
benzene_xyz = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'benzene.xyz')
mol_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mol')
mol_list = [i.split('.')[0] for i in os.listdir(mol_dir)]


def get_options():
    """User interface options."""
    user_options = {}
    user_options['mol'] = {'label': 'Molecules',
                           'type': 'stringList',
                           'default': 'C60',
                           'values': mol_list}
    return {'userOptions': user_options }


def add_molecule(opts):
    """Read xyz file and return as string."""
    mol_xyz = os.path.join(mol_dir, '%s.xyz' % opts['mol'])
    with open(mol_xyz, 'r') as f:
        newmol = f.readlines()
    return ''.join(newmol)


def run_command():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = {'append': True,
              'moleculeFormat': 'xyz',
              'xyz': add_molecule(opts)}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Add a molecule')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Add Molecule List")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_command()))
