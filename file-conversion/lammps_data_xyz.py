"""
Converts LAMMPS data file to xyz format.

Example:
 >>> python lammps_data_xyz.py data.IRMOF-1 IRMOF-1.xyz

Author: Kutay B. Sezginel
Date: October 2017
"""
import os
import sys


atoms = {'1': 'O',
         '2': 'C',
         '3': 'H',
         '4': 'Zn',
         '5': 'O'
         }


def lammps_data_xyz(lammps_data_file, xyz_file, atoms=atoms):
    """ Converts lammps.data file to xyz format
    Arguments:
        - lammps_data_file (str): LAMMPS data file to convert
        - xyz_file (str): xyz file

    Returns:
        - None: Writes xyz file
    """
    with open(lammps_data_file, 'r') as d:
        data_lines = d.readlines()

    for line_index, line in enumerate(data_lines):
        if 'Atoms' in line:
            start = line_index + 2
        if 'Bonds' in line:
            end = line_index - 1

    coordinates = data_lines[start:end]
    num_of_atoms = len(coordinates)
    new_coordinates = []
    for c in coordinates:
        atom = atoms[c.split()[2]]
        x, y, z = c.split()[4:7]
        new_coordinates.append([atom, x, y, z])

    with open(xyz_file, 'w') as xyz:
        xyz.write('%i\n' % num_of_atoms)
        xyz.write('lammps_data\n')
        for c in new_coordinates:
            xyz.write('%s %s %s %s\n' % (c[0], c[1], c[2], c[3]))


if __name__ == '__main__':
    print('Converting %s -> %s...' % (sys.argv[1], sys.argv[2]))
    print('Using atoms names:')
    for atom in atoms:
        print('%3s : %3s' % (atom, atoms[atom]))
    lammps_data_xyz(sys.argv[1], sys.argv[2], atoms=atoms)
    print('Done!')
