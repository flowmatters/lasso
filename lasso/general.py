import sys
import logging
import lasso.catalog_sets as catalog_sets
logger = logging.getLogger('lasso')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

class LogOptions(): pass

log_options=LogOptions()
log_options.dropped=True
log_options.expand=True
log_options.path=True

_default_catalog_set=catalog_sets.DEFAULT

def set_default_catalogs(catalog_set='DEFAULT'):
    '''
    Change the default set of catalogs to be searched (for the current session)

    catalog_set - A list of catalog factory functions, 
                  OR the name of a known catalog set

    Available catalog sets:

    * DEFAULT - Search the main NEII catalog and the Geoscience Australia catalog
    * NEII    - Only search the NEII catalog
    '''
    global _default_catalog_set
    if isinstance(catalog_set,str):
        _default_catalog_set = getattr(catalog_sets,catalog_set.upper())
    else:
        _default_catalog_set = catalog_set

def search(text,catalog_set=None):
    '''
    Search for 'text' across a given set of catalogs (or the default set)

    text - Free text to search for in each catalog

    catalog_set - Set of catalogs to use.
                  Defaults to the user's default catalog set if not provided or None
                  User's default catalog set can be configured with `set_default_catalogs` function.
    '''
    if not catalog_set:
        catalog_set = _default_catalog_set

    from .catalogs import neii,ga
    from .results import CSWQueryResult
    from owslib.fes import PropertyIsLike
    q = PropertyIsLike('csw:AnyText',text)

    catalogs = [c() for c in catalog_set]
    for cat in catalogs:
        cat.getrecords2([q],esn='full')
    results = {k:v for cat in catalogs for k,v in cat.records.items()}
    logger.info('Found %d results for search "%s"'%(len(results),text))
    return CSWQueryResult(results,text)

def connect_wfs(url):
    from .ogc import WFSResult
    return WFSResult(url,parent=None)
