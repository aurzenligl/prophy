import aprot

class MAC_MeasurementTerminationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measurementId',TMeasurementId)]
	
	