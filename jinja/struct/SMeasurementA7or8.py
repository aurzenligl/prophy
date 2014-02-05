import aprot

class SMeasurementA7or8(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('enableTwoUserMeasurement',TBoolean),('stationaryUeResources',TBoolean)]
	
	