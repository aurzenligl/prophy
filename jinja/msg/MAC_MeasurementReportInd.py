import aprot

class MAC_MeasurementReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measurementId',TMeasurementId),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC)),('measReportValue', aprot.bytes(size = MAX_NUM_MEAS_REPORT_VALUE_MAC))]
	
	