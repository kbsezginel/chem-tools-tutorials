# Avogadro
<img src='/assets/img/Avogadro2_Full_Large.png'>

[Avogadro 2](https://www.openchemistry.org/projects/avogadro2/) is a cross-platform powerful molecular editor and visualization application.

## Plug-ins
Avogadro 2 provides an easy to use plug-in interface. You can create your plug-in with just a few lines of Python code. The example below shows how you can use the plug-in interface to create a benzene molecule.

More examples can be seen in this [repository](https://github.com/kbsezginel/chem-tools-tutorials/tree/master/avogadro) as well as in the [OpenChemistry Avogadro 2018 users group meeting repository](https://github.com/OpenChemistry/avogadro-ugm2018).

### Example 1: Add molecule

```python
"""
Avogadro 2 basic plug-in example for adding a benzene molecule.
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
    stdin = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdin)

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

```

## Plug-in structure

Avogadro and your Python code communicates through json files. Basically they send each other some data by reading and writing json files.

### User input: `get_options`
This function allows you to get options from the user.
You can create a window with different input styles.
In the example below there are no options for user to select.

#### List input
The function below creates a drow down list with strings.
The selected entry is sent to the Python code.

```python
def get_options():
    """User interface options."""
    user_options = {}
    user_options['mol'] = {'label': 'Molecules',
                           'type': 'stringList',
                           'default': 'C60',
                           'values': mol_list}
    return {'userOptions': user_options }
```

The selection can be read by:

```python
stdin = sys.stdin.read()
opts = json.loads(stdin)
user_selection = opts['mol']
```

#### Number input
The function below creates a number input.

```python
def get_options():
    """User interface options."""
    user_options = {}
    user_options['num'] = {'label': 'My Number',
                           'type': 'float',
                           'default': 1.0,
                           'precision': 3,
                           'toolTip': 'Some number we want'}
    return {'userOptions': user_options }
```

The selection can be read by:

```python
stdin = sys.stdin.read()
opts = json.loads(stdin)
user_selection = opts['mol']
```

### Return result: `run_command`

#### New molecule
The function below returns a new molecule in xyz format.
```python
def run_command():
    stdin = sys.stdin.read()   # Read options from stdin
    opts = json.loads(stdin)   # Parse the JSON strings

    result = {'append': True,              # Prepare the result
              'moleculeFormat': 'xyz',
              'xyz': string_xyz}
    return result
```

#### Modify current molecule
The function below flattens all the z-coordinates of a molecule.

```python
def run_command():
    stdin = sys.stdin.read()   # Read options from stdin
    opts = json.loads(stdin)   # Parse the JSON strings

    coords = opts['cjson']['atoms']['coords']['3d']
    for i in range(0, len(coords), 3):
        coords[i+2] = 0.0
    return opts
```
