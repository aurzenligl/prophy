import aprot

class MAC_SystemInfoInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('gpsTimeAvailable',TBoolean)]
	
	