from .results import SearchResult
import logging
logger = logging.getLogger('lasso')

from .general import log_options

class OpenDAPCatalog(SearchResult):
    def __init__(self,url,parent=None):
        import siphon.catalog as thredds

        self._parent = parent
        self._url = url

        self._tds = thredds.TDSCatalog(self._url)

    def title(self):
        return "OpenDAP Catalog at %s "%self._url

    def describe(self):
        ds = self._tds.datasets
        cats = self._tds.catalog_refs

        if (len(ds)+len(cats))==1:
            if len(ds)==1:
                return self._expand_dataset(list(ds.values())[0]).describe()
            else:
                return self._expand_catalog(list(cats.values())[0]).describe()

#        if log_options.expand:
#            for d in ds.values():
#                logger.info('* %s'%self._expand_dataset(d).describe())
#            for c in cats.values():
#                logger.info('* %s'%self._expand_catalog(c).describe())

        return '[%s] %d datasets, %d catalogs'%(self._url,len(ds),len(cats))

    def _expand_dataset(self,ds):
        return OpenDAPResult(ds,parent=self)

    def _expand_catalog(self,cat):
        return OpenDAPCatalog(cat.href,self)

    def expand(self,recursive=False):
        expanded =  [self._expand_dataset(ds) for _,ds in self._tds.datasets.items()]
        expanded += [self._expand_catalog(cat) for _,cat in self._tds.catalog_refs.items()]
        return self._expand(expanded,recursive)

class OpenDAPResult(SearchResult):
    def __init__(self,res,parent=None):
        self._parent = parent
        import pydap.client as dap
        self._res = res
        self._valid = False
        self._status = None
        self._url = self._res.access_urls['OPENDAP']
        self._client = None

        try:
            self._client = dap.open_url(self._url)
            self._valid = True
        except Exception as e:
            logger.warn("Couldn't connect to OpenDAP service at %s"%self._url)
            logger.warn(e)
            self._status = "Cannot connect to OpenDAP service"

    def title(self):
        return "OpenDAP Dataset at %s"%self._url

    def describe(self):
        if self._valid:
            return '[%s] %s' %(self._url,self._client.attributes.get('NC_GLOBAL',{}).get('title',self._client.name))
        return '[%s] %s' %(self._url,self._status)

    def expand(self,recursive=False):
        return [self]

    def has_data(self):
        return self._valid

    def main_variable(self):
        if not self._valid: return None

        for k in self._client.keys():
            if self.is_main_variable(self._client[k]):
                return k

    def variables(self):
        if not self._valid: return []

        return self._client.keys()

    def is_main_variable(self,variable):
        dims = variable.dimensions
        
        # Not a main variable if its only dimension is itself (eg latitude, longitude, time)
        if (len(dims) <= 1) or (variable.name in dims):
            return False
        
        # Assuming the variable has other dimensions, look for a NetCDF/OpenDAP attribute named `standard_name`
        # 
        return ('standard_name' in variable.attributes) or ('cell_methods' in variable.attributes)

    def extents(self,dimension=None):
        if not self._valid: return {}

        if dimension:
            var = self._client[dimension]
            return var[::(var.shape[0]-1)]

        variable = self._client[self.main_variable()]
        return {d:self.extents(d) for d in variable.dimensions}

    def _range_to_slice(self,arr,lower=None,upper=None):
        import numpy as np
        if lower is None:
            mask = np.full_like(arr,True,bool)
        else:
            mask = arr>lower

        if upper is not None:
            mask = mask & (arr<upper)

        indices = sorted(np.where(mask))
        return slice(indices[0][0],indices[0][-1])

    def make_geotransform(self,data):
        import numpy as np
        if ('latitude' in data) and ('longitude' in data):
            width_var = data['longitude']
            height_var = data['latitude']
        elif ('x' in data) and ('y' in data):
            width_var = data['x']
            height_var = data['y']
        else:
            raise Exception('Cannot determine spatial coordinates')

        if (len(width_var.shape)!=1) or (len(height_var.shape)!=1):
            raise Exception('Expecting 1D coordinate variables')

        geotransform = [0]*6
        geotransform[1] = (np.max(width_var) - np.min(width_var))/(width_var.shape[0]-1)
        geotransform[0] = np.min(width_var)-geotransform[1]/2.0

        geotransform[5] = (np.min(height_var) - np.max(height_var))/(height_var.shape[0]-1)
        geotransform[3] = np.max(height_var)-geotransform[5]/2.0
        return np.array(geotransform)

    def retrieve(self,variable=None,**kwargs):        
        from collections import OrderedDict

        if not variable:
            variable = self.main_variable()

        dap_variable = self._client[variable]
        dims = dap_variable.dimensions
        constraints = OrderedDict()
        for d in dims:
            constraints[d] = self._range_to_slice(self._client[d],*sorted(kwargs.pop(d,[])))

        if len(kwargs):
            raise Exception('Invalid dimensions: %s'%str(list(kwargs.keys())))

        result = dap_variable[tuple(constraints.values())]
        result.attributes['geotransform'] = self.make_geotransform(result)
        return result

