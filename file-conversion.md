# File Conversion
There are hundreds of chemical file formats...
[Here](https://github.com/kbsezginel/chem-tools-tutorials/tree/master/file-conversion)
is a compilation of some Python scripts to convert between common file formats.

## Write
This contains functions to write atomic coordinates files.
The functions are formatted as:
```
write_file(file_name, atoms, coordinates)
```
where `file_name` is the output file name, `atoms` is a list of elements and `coordinates` is a 2D list
of atomic coordinates.

**Example (writing a water molecule in pdb format):**
```
filename = 'water.pdb'
atoms = ['O', 'H', 'H']
coordinates = [[0.0, 0.0, 0.0],
               [0.757, 0.586, 0.0],
               [-0.757, 0.586, 0.0]]

write_pdb(filename, atoms, coordinates)
```

## xyz/cif conversion
This conversion is important for defining a unit cell for a given structure.
The tricky part for this conversion is converting cartesian coordinates to fractional coordinates.
This script currently only works for orthogonal cells, however using [IPMOF](https://github.com/kbsezginel/IPMOF)
library a P1 version can be generated easily.

**Example:**
```
python xyz2cif.py mymolecule.xyz
```
This would prompt the user to enter cell dimensions and an output file name for the cif file.

## Fill unit cell (P1 conversion)
This script allows converting a unit cell to P1 space group using OpenBabel. This means that the cell would be
filled with all atoms by applying all the symmetry operations. This is necessary for some software
such as [lammps_interface](https://github.com/kbsezginel/lammps_interface) which is used to assign
force field parameters.

**Example:**
```
python fill_unit_cell.py non-P1.cif P1.cif
```

## [Tinker](https://dasher.wustl.edu/tinker/)
There are two scripts that allow conversion of tinker xyz file to regular xyz file.
One (`tinker_to_xyz.py`) is for converting a single file and the other (`tinker_traj_xyz.py`) is
for converting a set of tinker xyz files in a directory and collect them into a single xyz trajectory file.

**Usage:**

```
# Convert single file to xyz (output file name is prompted)
>>> python tinker_to_xyz.py

# Convert multiple files to xyz trajectory
# Input file basename, number of frames and output file name are prompted
>>> python tinker_to_xyz.py
```
