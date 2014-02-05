import aprot

class MAC_MeasurementTerminationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('measurementId',TMeasurementId)]
	
	