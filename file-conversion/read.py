"""
--- Ångström ---
Methods for reading chemical file formats.
"""
import numpy as np


def read_xyz(filename):
    """Read xyz file format

    Args:
        - filename (str): xyz file name

    Returns:
        - dict: atom names and coordinates
            -> {'atoms': ['C', ...], 'coordinates': [[x1, y1, z1], ...]}
    """
    with open(filename, 'r') as xyz_file:
        xyz_lines = xyz_file.readlines()
    n_atoms = int(xyz_lines[0].strip())
    header = xyz_lines[1].strip()
    atoms, coordinates = np.empty((n_atoms,), dtype='U2'), np.empty((n_atoms, 3))
    for i, line in enumerate(xyz_lines[2:]):
        atoms[i] = line.split()[0]
        coordinates[i] = [float(i) for i in line.split()[1:4]]
    return dict(atoms=atoms, coordinates=coordinates, header=header)


def read_cif(filename):
    """Read cif file format (baed on CoRE MOF cif files - might not work for all cif files!!!)

    Args:
        - filename (str): cif file name

    Returns:
        - dict: atom names, coordinates, and cell parameters
            -> {'atoms': ['C', ...], 'coordinates': [[x1, y1, z1], ...], 'cell': [a, b, c, alpha, beta, gamma]}
    """
    with open(filename, 'r') as cif_file:
        cif_lines = cif_file.readlines()
    cell_lines = ['_cell_length_a', '_cell_length_b', '_cell_length_c', '_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma']
    atomidx = cif_lines.index('_atom_site_type_symbol\n')
    xidx = cif_lines.index('_atom_site_fract_x\n')
    yidx = cif_lines.index('_atom_site_fract_y\n')
    zidx = cif_lines.index('_atom_site_fract_z\n')
    atoms, coordinates, cellpar, i, header, read_atoms = [], [], [0] * 6, 0, 'angstrom', False
    for line_idx, line in enumerate(cif_lines):
        if not read_atoms:
            if line == 'loop_\n':
                loopidx = line_idx + 1
            if 'data_' in line:
                header = line.strip().split('data_')[1]
            for cidx, cl in enumerate(cell_lines):
                if cl in line:
                    cellpar[cidx] = float(line.split()[1])
        ls = line.split()
        if len(ls) > 3:
            read_atoms = True
            atoms.append(ls[atomidx - loopidx])
            x = float(ls[xidx - loopidx])
            y = float(ls[yidx - loopidx])
            z = float(ls[zidx - loopidx])
            coordinates.append([x, y, z])
    return dict(atoms=np.array(atoms), coordinates=np.array(coordinates), cell=np.array(cellpar), header=header)
