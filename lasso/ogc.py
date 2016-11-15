from .results import SearchResult

class OGCEnpointResult(SearchResult):
    def __init__(self,url,parent=None):
        self._parent = parent
        self._url = url
        self._valid = False
        self._status = None

        try:
            self._client = self._service()
            self._valid = True
        except:
            self._status = "Cannot connect to service"

    def expand(self,recursive=False):
        return [self]

class WCSResult(OGCEnpointResult):
    def __init__(self,url,parent=None):
        super(WCSResult,self).__init__(url,parent)

    def _service(self):
        from owslib import wcs
        return wcs.WebCoverageService(self._url)

    def has_data(self):
        return self._valid

class WFSResult(OGCEnpointResult):
    def __init__(self,url,wfs_version='1.1.0',parent=None):
        self._wfs_version = wfs_version
        super(WFSResult,self).__init__(url,parent)

    def title(self):
        return "WFS Endpoint at %s"%self._url

    def _service(self):
        from owslib import wfs
        return wfs.WebFeatureService(self._url,version=self._wfs_version)

    def describe(self):
        keys = self.variables()
        if len(keys)>1:
            return '%d items'%len(keys)
        return keys[0]

    def variables(self):
        if not self._valid:
            raise Exception(self._status)

        return [i[0] for i in self._client.items()]

    def retrieve(self,variable=None,dataframe=False,count=False,bbox=None,or_filter=False,*searchArgs,**kwargs):
        '''
        Retrieve data from WFS service


        '''
        if not self._valid:
            raise Exception(self._status)

        if not variable:
            variable = self._client.items()[0][0]


        query_params=dict(typename=variable,propertyname=None)


        # construct query from searchArgs
        if count:
            query_params['resulttype']='hits'

        if bbox:
            query_params['bbox']=bbox

        #query_params.update(kwargs)
        if len(kwargs)>0:
            import owslib.fes as fes
            from owslib.etree import etree
            filter_components = [fes.PropertyIsLike(propertyname=k,literal='%s'%(str(v))) for k,v in kwargs.items()]
            if len(filter_components)==1:
                query_filter = filter_components[0]
            elif or_filter:
                query_filter = fes.Or(filter_components)
            else:
                query_filter = fes.And(filter_components)

            filterxml = etree.tostring(query_filter.toXML()).decode('utf-8')
            filterxml = '<Filter>%s</Filter>'%filterxml
            query_params['filter']=filterxml

        filter_result = False
        try:
            results = self._client.getfeature(**query_params)
        except:
            if 'filter' in query_params:
                query_params.pop('filter')
                filter_result = True
                results = self._client.getfeature(**query_params)
            else:
                raise

        feature_text = results.read()
        if not isinstance(feature_text,str):
            feature_text = feature_text.decode('utf-8')
        tmp_fn = 'tmp.gml'
        open(tmp_fn,'w').write(feature_text)

        from osgeo import ogr
        ds = ogr.Open(tmp_fn)

        # remove tmp file

        layer = ds.GetLayer()

        features = [layer.GetNextFeature() for i in range(layer.GetFeatureCount())]
        if filter_result:
            features = self.filter_features(features,or_filter,kwargs)

        from shapely.wkt import loads

        for f in features:
            f.geom = loads(f.geometry().ExportToWkt())

        if dataframe:
            from geopandas import GeoDataFrame
            feature_dicts = [dict([('geometry',f.geom)] + [(p,f[p]) for p in f.keys()]) for f in features]
            return GeoDataFrame(feature_dicts)

        return features
        # return as geopandas?

    def filter_features(self,features,or_filter,filter_terms):
        result = []
        import re

        for f in features:
            met = False
            for k,v in filter_terms.items():
                comparison = f[k]
                if isinstance(v,str):
                    if re.match(v.replace('%','.*'),comparison):
                        met = True
                else:
                    met = comparison==v

                if met and or_filter:
                    break
                if not met and not or_filter:
                    break

            if met:
                result.append(f)

        return result
