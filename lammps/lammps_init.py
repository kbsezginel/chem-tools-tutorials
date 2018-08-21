"""
Helper functions for initializing LAMMPS simulations.
"""
import os


def change_job_name(input_lines, job_name):
    """
    Change slurm job name.
    """
    job_lines = []
    for i, line in enumerate(input_lines):
        new_line = line
        if '#SBATCH --job-name' in line:
            new_line = '#SBATCH --job-name=%s\n' % job_name
        job_lines.append(new_line)
    return job_lines


def change_seed(input_lines, seed=None):
    """
    Change seed number of Lammps input.
    """
    if seed is None:
        seed = random.randint(100000, 999999)
    for i, line in enumerate(input_lines):
        if 'seed equal' in line:
            seed_index = i
    input_lines[seed_index] = 'variable        seed equal %i\n' % seed
    return input_lines


def write_lines(file_lines, new_file):
    """
    Write a list of lines to a file.
    """
    with open(new_file, 'w') as f:
        for l in file_lines:
            f.write(l)


def read_lines(filename):
    """
    Read a file and return a list of lines.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def replace_lines(file_path, idx=[0], new_lines=['Hello!\n'], dest=None):
    """
    Replace lines in given indices with new given lines
    Indexing:
     - to change line 5, use -> idx=[4]
     - to change line 2 and 3 use -> idx=(1, 3)
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if len(idx) == len(new_lines):
        for i, nl in zip(idx, new_lines):
            lines[i] = nl

        if dest is None:
            dest = os.path.split(file_path)[0]
            os.remove(file_path)

        new_file = os.path.join(dest, os.path.basename(file_path))
        with open(new_file ,'w') as nf:
            for line in lines:
                nf.write(line)
    else:
        print('Requested indices do not match given number of lines!!!')
