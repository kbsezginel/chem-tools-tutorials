# Open Babel
Open Babel is a chemical toolbox designed to speak the many languages of chemical data.
-   [Open Babel website][obabel-website]
-   [Open Babel GitHub repository][obabel-github]

## Installation
Open Babel is available for Windows, Linux and MacOSX.
See [Open Babel installation][obabel-installation] for more information.

### Command Line Interface
The command line interface for openbabel can be installed from [Open Babel website][obabel-website].
For usage information:

```bash
obabel --help
```
Single file conversion example from xyz to pdb format for benzene molecule:

```bash
obabel -ixyz benzene.xyz -opdb -O benzene.pdb
```

### Python bindings
Python bindings for openbabel is available through pip.

```python
pip install openbabel
```

[Here is an example Jupyter Notebook that shows how to use `openbabel` Python bindings.](https://github.com/kbsezginel/chem-tools-tutorials/blob/master/openbabel/openbabel.ipynb)

### Python wrapper (pybel)
There is also a python wrapper for openbabel which is also available through pip.
Usage information is available on [Pybel website][pybel-website].

```python
pip install pybel
```

## Useful Commands

#### Converting symmetry to P1 (filling unit cell)

The following command can be used to convert any crystal with symmetry to P1 non-symmetric crystal filling unit cell with all atoms.
```
obabel -icif non-P1.cif -ocif -O P1.cif --fillUC strict
```
#### Exporting rendered molecule image

Using the following command 2D rendering of given atomic coordinates of molecule in any format (`my-molecule.xyz`) is used to produce an image file (`my-molecule.svg`).
```
obabel my-molecule.xyz -O my-molecule.svg -xS -xd -xb none
```

----------------------------------------------------------------------------------------------------
[obabel-website]: http://openbabel.org/
[obabel-github]: https://github.com/openbabel/openbabel
[obabel-installation]: http://openbabel.org/wiki/Category:Installation
[pybel-website]: https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html
