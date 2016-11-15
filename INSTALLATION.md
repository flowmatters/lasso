# Setting up a Python data analysis environment with _Lasso_

Lasso is a Python package designed to help you discover, retrieve and use catalogued environmental information.

One of the goals for Lasso is to demonstrate how cross platform, open source, tools can support analysis of standards-based, web hosted datasets. Its expected that some users won't have experience with Python (and won't have an existing Python-based data analysis environment).

This document outlines the key steps for setting up a data analysis environment using Python, with a particular emphasis on configuring the environment to using Lasso to access Australian National Environment Information Infrastructure (NEII) compliant web servers.


## Data analysis in the Jupyter/IPython Notebook

It's expected that most users will use Lasso from within the [Jupyter notebook](http://jupyter.org/) environment - indeed, all the examples are implemented as notebooks.

A Notebook is a _document_ that can contain live code, data, documentation and visualisations. The Jupyter Notebook is a web application for creating and running Notebooks backed by Python or one of many other programming languages.

For most users, the easiest way to setup the Notebook environment is to install [Anaconda Python](https://www.continuum.io/downloads). Anaconda is a _distribution_ of Python, targeted at the scientific and data analysis community. Anaconda includes the IPython/Jupyter notebook and many of the key data analysis packages for Python.

Anaconda Python is currently distributed in separate packages for Python 3 (3.5 at the time of writing) and Python 2 (2.7). Download and install the appropriate version of Anaconda for Python 3 for your system.

## Installing other dependencies

Anaconda Python will install a number of the packages needed by Lasso, such as [numpy](http://www.numpy.org/) and [pandas](http://pandas.pydata.org/).

Other packages can be installed using `pip` (the recommended tool for installing Python packages) or `conda`, the package manager for Anaconda. You run `pip` and `conda` from the command line (Terminal in OSX or Anaconda Command Prompt in Windows). `conda` can also run from the Anaconda Navigator application.

A basic installation of Lasso requires [OWSLib](https://geopython.github.io/OWSLib/), [Siphon](https://github.com/Unidata/siphon) and [Pydap](http://www.pydap.org/):

```
pip install https://github.com/pacificclimate/pydap/archive/develop.zip OWSLib https://github.com/Unidata/siphon/archive/master.zip
```
**Windows Note:** If the above command fails, try explicitly installing `pyproj` with `conda` first, before repeating the above `pip install`.

```
conda install pyproj
```
Most (if not all) of the data services you will access through Lasso will return some form of spatial data, in which case Lasso will require [OGR/GDAL](https://pypi.python.org/pypi/GDAL/)  (although we will remove this dependency in the future), [Shapely](https://pypi.python.org/pypi/Shapely) and [GeoPandas](http://geopandas.org/):

```
conda install GDAL shapely
pip install geopandas
```
**Windows Note:** Some users encounter difficulties installing `GDAL` and `shapely` using `conda` on Windows. An alternative is to use the copies of these (and a few other) Python packages, maintained by Christoph Gohlke at [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/). You would need to download the following packages from that site:

* `GDAL` (several versions are available, download the latest version from the 2.0. line -- currently 2.0.3)
* `shapely`
* `fiona` (dependency of `geopandas` and other packages)
* `rasterio` (dependency of `rasterstats`)

Make sure you download the file appropriate to your version of Python (eg 3.5, 3.6) and the architecture of Windows (`win32` vs `win_amd64`). You will then need to install the downloaded wheel (`.whl` file) using pip. For example:

```
cd \Users\me\Downloads
pip install GDAL‑2.1.2‑cp35‑cp35m‑win_amd64.whl
pip install Shapely‑1.5.17‑cp35‑cp35m‑win_amd64.whl
pip install Fiona‑1.7.0‑cp35‑cp35m‑win_amd64.whl
pip install rasterio‑1.0a3‑cp35‑cp35m‑win_amd64.whl
```

(Where the exact filenames may differ depending on the version of Python and Windows)

You will also need the Microsoft Visual C++ 2015 runtime libraries (which these Windows builds of GDAL/Fiona/etc need). Download and install the runtime from [https://www.visualstudio.com/downloads/download-visual-studio-vs#d-visual-c](https://www.visualstudio.com/downloads/download-visual-studio-vs#d-visual-c) (searching for 'Runtime' in the Search Downloads box to find the most recent release for your Windows architecture - 32/64 bit).

After these commands have run, `pip install geopandas` should work.

Finally, the examples use [python-rasterstats](https://github.com/perrygeo/python-rasterstats) to perform zonal statistics:

```
pip install rasterstats
```

Of course, you need to install Lasso as well:

```
pip install https://github.com/flowmatters/lasso/archive/master.zip
```

