import logging
logger = logging.getLogger('lasso')

from .general import log_options

MAX_EXPANSION=50
_aborted_search=False

class SearchResult(object):
    def __init__(self):
        self._parent = None

    def _expand(self,results,recursive):
        global _aborted_search
        _aborted_search = False
        if recursive:
            if log_options.expand:
                logger.info('Expanding %d results within "%s "'%(len(results),self.title()))
            count = 0
            nested_expanded = []
            for res in results:
                expanded_result = res.expand(recursive)
                count += len(expanded_result)
                nested_expanded.append(expanded_result)
                if _aborted_search:
                    break
                if count >= MAX_EXPANSION:
                    _aborted_search = True
                    logger.warn('Hit maximum number of results to expand (%d). Aborting. Refine search before expanding'%MAX_EXPANSION)
                    break
            return [item for result in nested_expanded for item in result]

        return results

    def refine(self,text):
        '''
        Search for additional text in an existing set of results.

        WARNING: Behaviour of this method is dependent upon the types of results found.

        This method is provided as a quick option for sifting through a large number of results,
        without re-searching the source catalogs. However refine can only use information retrieved
        from the catalog. Searching for the exampled search in the original catalogs will be more
        conclusive.
        '''
        keep = []
        for res in self.expand(recursive=False):
            if text.lower() in res.describe().lower():
                keep.append(res)
                logger.info('Keeping %s'%res.describe())
            else:
                logger.info('Discarding %s'%res.describe())
        return RefinedSearchResult(keep,parent=self)

    def has_data(self):
        return False

    def title(self):
        return self.__class__.__name__

    def titles(self):
        return '\n'.join([r.title() for r in self.expand(recursive=False)])

    def describe_all(self):
        return '\n'.join([str(r.describe()) for r in self.expand(recursive=False)])

    def path(self):
        '''
        Describes where a particular result comes from in terms of an original catalog search and
        a progressive expansion of results.
        '''
        path = []
        item = self
        while item is not None:
            path.insert(0,item.title())
            item = item._parent

        if log_options.path:
            logger.info('\n > '.join(path))
        return path

    def __getitem__(self,ix):
        return self.expand(recursive=False)[ix]

class RefinedSearchResult(SearchResult):
    def __init__(self,results,parent=None):
        self._parent = parent
        self._results = results

    def expand(self,recursive=False):
        return self._expand(self._results,recursive)

    def describe(self):
        if len(self._results)==1:
            return self._results[0].describe()

        if log_options.expand:
            for r in self.expand(recursive=False):
                logger.info('* %s'%r.describe())
        return '%d results'%len(self._results)

class CSWQueryResult(SearchResult):
    def __init__(self,records,search=''):
        self._parent = None
        self._search = search
        self._records = records

    def title(self):
        return 'Search results for "%s"'%(self._search)

    def expand(self,recursive=False):
        expanded = [CSWResult(v,parent=self) for v in self._records.values()]
        return self._expand(expanded,recursive)

    def describe(self):
        if len(self._records)==1:
            return self.expand(recursive=False)[0].describe()

        for r in self.expand(recursive=False):
            logger.info('* %s'%r.describe())
        return '%d results'%len(self._records)

class CSWResult(SearchResult):
    def __init__(self,res,parent=None):
        self._parent = parent
        self._res = res

    def title(self):
        return 'Search result "%s"'%self.describe()

    def make_result(self,uri):
        return URIResult(uri,parent=self)

    def real_data_uri(self,uri):
        protocol = uri['protocol']
        if not protocol:
            return False
        
        if protocol.startswith('OGC:WMS'):
            return False

        if protocol=='WWW:LINK-1.0-http--link':
            return False
            # Unless its a known file type - json, kml, etc?

        return True

    def expand(self,recursive=False):
        expanded = [self.make_result(uri) for uri in self._res.uris if self.real_data_uri(uri)]

        if log_options.dropped:
            for uri in [u for u in self._res.uris if not self.real_data_uri(u)]:
                logger.info('Dropped %s - Not a recognised data protocol (%s)'%(uri['url'],uri['protocol']))

        return self._expand(expanded,recursive)

    def describe(self):
        return self._res.title

class URIResult(SearchResult):
    def __init__(self,res,parent=None):
        self._parent = parent
        self._res = res

    def title(self):
        return "URI(%s,%s)"%(self._res['url'],self._res['protocol'])

    def expand(self,recursive=False):
        protocol = self._res['protocol']
        if protocol.endswith('opendap'):
#            import siphon.catalog as thredds

#            tds = thredds.TDSCatalog(self._res['url'])
#            expanded = [OpenDAPResult(ds,parent=self) for _,ds in tds.datasets.items()]
#            return self._expand(expanded,recursive)
            from .dap import OpenDAPCatalog
            return self._expand([OpenDAPCatalog(self._res['url'],parent=self)],recursive)
        elif protocol=='OGC:WCS':
            from .ogc import WCSResult
            return self._expand([WCSResult(self._res['url'],parent=self)],recursive)
        elif protocol=='OGC:WFS':
            from .ogc import WFSResult
            return self._expand([WFSResult(self._res['url'],parent=self)],recursive)
        elif protocol.upper()=='GEOJSON':
            from .geojson import GeoJSONResult
            return self._expand([GeoJSONResult(self._res['url'],parent=self)],recursive)
        return [self]

    def describe(self):
        return self._res

    def connect(self):
        return self.expand(recursive=False)[0]

# nsw_solar.__class__.y = x
