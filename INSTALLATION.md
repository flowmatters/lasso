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
ow

```
pip install git+https://github.com/pacificclimate/pydap.git@develop OWSLib git+https://github.com/Unidata/siphon.git
```

Most (if not all) of the data services you will access through Lasso will return some form of spatial data, in which case Lasso will require [OGR/GDAL](https://pypi.python.org/pypi/GDAL/)  (although we will remove this dependency in the future), [Shapely](https://pypi.python.org/pypi/Shapely) and [GeoPandas](http://geopandas.org/):

```
conda install GDAL shapely
```

Finally, the examples use [python-rasterstats](https://github.com/perrygeo/python-rasterstats) to perform zonal statistics:

```
pip install python-rasterstats
```

Of course, you need to install Lasso as well:

```
pip install https://github.com/flowmatters/lasso/archive/master.zip
```

**Once its uploaded**


### Notes to self...

```
pip install git+https://github.com/pacificclimate/pydap.git@develop
pip install git+https://github.com/Unidata/siphon.git
```


