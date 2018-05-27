# Bash scripting tips

## Changing a line from a file using `sed`

#### Change given string in given line

To change *old* to *new* in line *N* of file *file_name*:
```bash
sed -i 'Ns/old/new/' file_name
```

#### Change complete line

To change line *N* of file *file_name* with *replacement_line*:

```bash
# Change in-place
sed -i 'Ns/.*/replacement-line/' file_name

# Write to a new file
sed 'Ns/.*/replacement-line/' file_name > new_file
```

## Loops

#### Submit all jobs in all directories under directory

Assuming your job submission file is *job.something* and you are using SLURM scheduler:
```bash
for i in `ls`
do
sbatch $i/job.*
done
```

## String and path stuff

#### Split path
```bash
$ mypath='this/is/a/path/to/somewhere'

$ basename $mypath
somewhere

$ dirname $mypath
this/is/a/path/to
```
