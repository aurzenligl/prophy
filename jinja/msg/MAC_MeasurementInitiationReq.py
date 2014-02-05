import aprot

class MAC_MeasurementInitiationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measurementId',TMeasurementId),('reportPeriod',TPeriod),('samplingPeriod',TPeriod),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC))]
	
	