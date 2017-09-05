# [HostDesigner](https://github.com/kbsezginel/HostDesigner)
A Program for the de Novo Structure-Based Design of Molecular Receptors with Binding Sites that Complement Metal Ion Guests
[<sup>1</sup>](http://pubs.acs.org/doi/full/10.1021/ic0202920)
## Installation
**1. HostDesigner Installation**

HostDesigner V3.0 source code can be downloaded [here](https://sourceforge.net/projects/hostdesigner-v3-0/). The source code is also provided in this repository. Detailed installation instructions are provided with the source code under *00_Documentation* folder. Below a summarized version of the instructions are provided.

**- Compiling the code:**

HostDesigner is provided as Fortran source code. The code can be compiled using [gfortran](https://gcc.gnu.org).
The downloaded directory *01_Source* contains the files needed to create the HostDesigner executable.
Assuming that that both *gfortran* and *make* executables are available in the user’s path, simply open a terminal window, enter the *01_Source* directory, and run *make*. This should produce the executable named *hd3.0* in less than a minute.

```
cd HD_3.0/01_Source
make
```

**- Configuring the environment**

HostDesigner is a command line executable and, once the system is properly configured, the
user should be able to invoke it from any directory. After *hd3.0* has been successfully compiled,
there are two additional things that must be done for this to happen.

First, the executable must be placed in a location that is in the user’s path.

Second, the executable must be provided the location of two required data files – *CONSTANTS* and *LIBRARY*.

For a bash user with username *hay* the steps are as follows:

1.  Put the executable *hd3.0* in a directory that is part of the user’s default path
2.  Add the following lines to *.bashrc* file:

```
export PATH=“PATH:/Users/hay/bin”
export HD_DIR=“/Users/hay/bin/hd_dir”
```

After completing the above steps, the configuration should be tested by opening a new terminal
window and issuing a couple simple commands. Issuing the command:

```
which hd3.0
```

Should return the response:

```
path_to_the_executable/hd3.0
```

To verify that the environmental variable has been properly set, issue the command:

```
echo $HD_DIR
```

**- Running test cases**

Directory *03_Examples* in the download package contains eight test cases that can be run to
verify that HostDesigner has been correctly compiled and that the system has been correctly
configured. Each test case consists of a control file, input fragment(s), and a prior summary file
obtained when the test was last run.

To run any of the test cases, open a terminal window, enter one of the subdirectories containing the input files (named case#), type *hd3.0* on the command line, and hit return.
The code should execute and begin printing information to the screen.
All the test cases should complete within a couple of minutes and produce several output files.
To verify expected performance, compare the output file with the .summ extension to the provided file named prior.summ, which is output obtained when the authors previously ran the example.
The timings will be machine specific, but the number of links read, the number of links used, the total number of structures examined, and the number of structures stored should be identical.


**2. Python Interface Installation**

HostDesigner python interface allows the user to create and run HostDesigner simulations with python scripts. Moreover, resulting structures can be visualized with Jupyter notebooks.

To install the interface run:

```
python setup.py install
```

### Terms of Use
Copyright © 2015 Benjamin Hay

Supramolecular Design Institute

All rights reserved.


Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

1.  Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.
2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

HostDesigner is provided by the authors “as is” and any express or implied warranties of
merchantability and fitness for a particular purpose are disclaimed. In no event shall the authors
be liable for any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services; loss of use; data or
profits; or business interruption) however caused and on any theory of liability, whether in
contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the
use of this software, even if advised of the possibility of such damage.
