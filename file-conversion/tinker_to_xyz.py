"""
Converts tinker xyz format to regular xyz format.

Usage:
 >>> python tinker_to_xyz.py tinkerFile.xyz
"""
import sys
import os


def read_tinker_xyz(txyz_file):
    """ This assumes the first two lines are info and the rest are all coordinates """
    with open(txyz_file, 'r') as txyz:
        txyz_lines = txyz.readlines()
    atoms, coors = [], []
    for line in txyz_lines[2:]:
        atom, x, y, z = line.split()[1:5]
        atoms.append(read_atom_name(atom))
        coors.append([float(i) for i in [x, y, z]])
    return atoms, coors


def read_atom_name(tinker_atom):
    """ Convert atom force field type to element name """
    if len(tinker_atom) == 1:
        atom = tinker_atom
    elif len(tinker_atom) > 1:
        if tinker_atom[1].isupper():
            atom = tinker_atom[0]
        elif tinker_atom[2].islower():
            atom = tinker_atom[:2]
    return atom


def write_xyz(file_name, atoms, coordinates, header='mol'):
    """ Write given atomic coordinates to file in xyz format """
    with open(file_name, 'w') as xyz_file:
        xyz_file.write(str(len(coordinates)) + '\n')
        xyz_file.write(header + '\n')
        format = '%-2s %7.4f %7.4f %7.4f\n'
        for atom, coor in zip(atoms, coordinates):
            xyz_file.write(format % (atom, coor[0], coor[1], coor[2]))


if __name__ == "__main__":
    txyz_file = os.path.abspath(sys.argv[1])
    print('Reading tinker xyz file -> %s' % txyz_file)
    atoms, coors = read_tinker_xyz(txyz_file)
    xyz_file = input('Enter output xyz file name: ')
    write_xyz(xyz_file, atoms, coors, header=os.path.basename(txyz_file))
    print('Done! Saved as -> %s' % os.path.abspath(xyz_file))
