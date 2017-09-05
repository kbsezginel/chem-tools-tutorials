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
### Python wrapper (pybel)
There is also a python wrapper for openbabel which is also available through pip.
Usage information is available on [Pybel website][pybel-website].

```python
pip install pybel
```

----------------------------------------------------------------------------------------------------
[obabel-website]: http://openbabel.org/
[obabel-github]: https://github.com/openbabel/openbabel
[obabel-installation]: http://openbabel.org/wiki/Category:Installation
[pybel-website]: https://openbabel.org/docs/dev/UseTheLibrary/Python_Pybel.html
