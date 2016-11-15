# Lasso

Lasso catches datasets.

Lasso is a data access toolkit for Australian environmental data, indexed through the National Environmental Information Infrastructure (NEII).

With Lasso, you can search various data catalogs to discover data services, then access those data services to retrieve data into data structures compatible with popular Python data analysis libraries, such as numpy, pandas, shapely and geopandas.

Lasso can currently work with Web Catalog Service (CSW), Web Feature Services and OpenDAP services. In accessing these services, much of the heavy lifting is performed by other open source libraries (see [dependencies](#dependencies)). While each of these libraries shields the user from the lower level details of their respective services, the intent of Lasso is take this a step further by making different service types queryable through a common API and to 'connect the dots', between catalogs, services and data in a consistent way. The emphasis is on retrieving the data and then analysing it with Python, so Lasso returns the data to you as Python objects, using established Python data analysis libraries, rather than worrying about on-disk representation of the data: WFS queries come back as [GeoPandas](http://geopandas.org/) Dataframes rather than pure [GML](http://www.opengeospatial.org/standards/gml).

## Installation

You can install Lasso directly from Github using pip

```
pip install git+https://github.com/flowmatters/lasso
```

We don't reference _any_ [dependencies](#dependencies)) in the Python packaging, so nothing else will get installed. This is because, for most people, the core dependencies are better installed as part of a scientific Python distribution, while other dependencies are optional depending on what type of data you're searching for and retrieving.

For more detailed information on configuring a data analysis environment for accessing NEII data using Lasso, see [INSTALLATION.md](INSTALLATION.md).

## Dependencies

Lasso has been developed and tested on Python 3.

You will almost certainly want [numpy](http://www.numpy.org/) and [pandas](http://pandas.pydata.org/).

Lasso uses the following packages to access data catalogs and services

* [OWSLib](https://geopython.github.io/OWSLib/) for accessing OGC services, including CSW catalogs, WFS and WCS
* [Siphon](https://github.com/Unidata/siphon) for querying THREDDS data servers (for OpenDAP)
* [Pydap](http://www.pydap.org/) for querying OpenDAP services

Lasso can use the following packages for reading data from services (eg for parsing the GML from a WFS)

* [OGR/GDAL](https://pypi.python.org/pypi/GDAL/) for reading GML (and we really should swap this out!)
* [Shapely](https://pypi.python.org/pypi/Shapely) and [GeoPandas](http://geopandas.org/) for processing vector data

The example Notebooks use the following packages

* [python-rasterstats](https://github.com/perrygeo/python-rasterstats)

Overall, that's quite a few dependencies. You don't necessarily need them all - it depends on what data you try to access.

## Getting started


```python
import lasso as l

results.search('solar')


```

## Contributions

Are most welcome.




