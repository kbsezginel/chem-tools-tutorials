"""
Converts tinker trajectory frames in current directory to xyz trajectory file.

Usage:
 >>> python tinker_traj_xyz.py
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


def write_xyz(xyz_file, atoms, coordinates, header='mol'):
    """ Write given atomic coordinates to file in xyz format """
    xyz_file.write(str(len(coordinates)) + '\n')
    xyz_file.write(header + '\n')
    format = '%-2s %7.4f %7.4f %7.4f\n'
    for atom, coor in zip(atoms, coordinates):
        xyz_file.write(format % (atom, coor[0], coor[1], coor[2]))


def get_frame_extensions(n_frames):
    width = "0%i" % len(str(n_frames))
    frame_ext = []
    for f in range(1, n_frames + 1):
        frame_ext.append(format(f, width))
    return frame_ext


if __name__ == "__main__":
    txyz_name = input('Please enter name of file without the dot (ex: int1_fix_500): ')
    n_frames = int(input('Please enter number of frames: '))
    traj_file = input('Please enter output file name (ex: traj.xyz): ')
    frame_ext = get_frame_extensions(n_frames)
    with open(traj_file, 'w') as traj_file_obj:
        for f in frame_ext:
            txyz_file = '%s.%s' % (txyz_name, f)
            atoms, coors = read_tinker_xyz(txyz_file)
            write_xyz(traj_file_obj, atoms, coors, header=txyz_file)
        print('Done! Saved as -> %s' % os.path.abspath(traj_file))
