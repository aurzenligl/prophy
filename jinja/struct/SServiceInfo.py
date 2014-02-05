import aprot

class SServiceInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('serviceType',ETestabilityServiceType),('serviceAddr',TAaSysComSicad)]
	
	