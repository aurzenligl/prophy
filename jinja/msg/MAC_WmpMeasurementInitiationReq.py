import aprot

class MAC_WmpMeasurementInitiationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellId',TCellId),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC_WMP))]
	
	