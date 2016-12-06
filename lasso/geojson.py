
from .results import SearchResult

class GeoJSONResult(SearchResult):
    def __init__(self,uri,parent):
        self._parent = parent
        self._uri = uri

    def retrieve_all(self):
        import requests
        return requests.get(self._uri).json()

    def _feature_matches(self,f,or_filter=False,**kwargs):
        and_filter = not or_filter
        for k,v in kwargs.items():
            matches = k in f['properties'] and f['properties'][k]==v
            if matches and or_filter: return True
            if and_filter and not matches: return False

        return and_filter

    def retrieve(self,dataframe=False,count=False,or_filter=False,**kwargs):
        result = self.retrieve_all()

        result['features'] = [f for f in result['features'] if self._feature_matches(f,or_filter,**kwargs)]

        if count:
            result['features'] = result['features'][:count]

        if dataframe:
            from geopandas import GeoDataFrame
            return GeoDataFrame.from_features(result['features'])

        return result