# Packmol
PACKMOL creates an initial point for molecular dynamics simulations by packing molecules in defined regions of space.
The packing guarantees that short range repulsive interactions do not disrupt the simulations.
-   [Open Babel website](https://www.ime.unicamp.br/~martinez/packmol/home.shtml)
-   [Packmol GitHub repository](https://github.com/mcubeg/packmol)
-   [Packmol paper](http://onlinelibrary.wiley.com/doi/10.1002/jcc.21224/abstract)

## Installation
The [official user guide for Packmol](https://www.ime.unicamp.br/~martinez/packmol/userguide.shtml)
does a really good job of explaining how to install and use Packmol.
Basically, you need to download Packmol [here](https://www.ime.unicamp.br/~martinez/packmol/download.shtml).
Unpack the *tar* file and compile:

```
tar -xvzf packmol.tar.gz

cd packmol
make
```

### Running packmol

```
packmol < packmol.inp
```

### Python wrapper

[virtualzx-nad/pypackmol](https://github.com/virtualzx-nad/pypackmol) is a decent Python wrapper for Packmol.

Alternatively I have been working on a wrapper myself which is still in development.
See `packmol.py` [here](https://github.com/kbsezginel/chem-tools-tutorials/blob/master/packmol/packmol.py)
