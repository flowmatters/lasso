
def neii():
	return CSWCatalog('http://neii.bom.gov.au/services/catalogue/csw')
#    import owslib.csw as csw
#    return csw.CatalogueServiceWeb('http://neii.bom.gov.au/services/catalogue/csw')

def ga():
	return CSWCatalog('http://www.ga.gov.au/geonetwork/srv/en/csw')
#    import owslib.csw as csw
#    return csw.CatalogueServiceWeb('http://www.ga.gov.au/geonetwork/srv/en/csw')

def environment_gov_au():
	services = [
		'http://www.environment.gov.au/mapping/services/ogc_services/World_Heritage_Areas/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/World_Heritage_Areas_label/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/capad/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Commonwealth_Heritage_List/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Commonwealth_Marine_Regions/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Commonwealth_Marine_Reserves/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Commonwealth_Marine_Reserves_IUCN/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Conservation_Management_Zones/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Important_Wetlands/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/EPBC_Referrals/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/IMCRA_Mesoscale/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/IMCRA_Provincial/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Indigenous_Protected_Areas_Declared/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/IBRA7_Regions/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/IBRA7_Subregions/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Key_Ecological_Features/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Key_Ecological_Features_named/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/National_Heritage_List/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Natural_Resource_Management_Regions/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Ramsar_Upstream_Catchments/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Rangelands/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Strategic_Assessment_Areas/MapServer/WFSServer',
		'http://www.environment.gov.au/mapping/services/ogc_services/Ramsar_Wetlands/MapServer/WFSServer'
	]

def CSWCatalog(url):
	import owslib.csw as csw
	return csw.CatalogueServiceWeb(url)

#class Catalog():
#	pass
#
#class CSWCatalog(Catalog):
#	def __init__(self,url):
#		import owslib.csw as csw
#		self.url = url
#		self._catalog = csw.CatalogueServiceWeb(url)
#
#	def search(self,text):
#	    from owslib.fes import PropertyIsLike
#	    q = PropertyIsLike('csw:AnyText',text)
#	    cat.getrecords2([q],esn='full')
#
#class WFSIndex(Catalog):
#	def __init__(self,urls):

# data.gov.au (ckan - plugin for csw?), ands.org.au (rifscs)
# nci thredds, 
# nci csw
# auscover - csw

