import aprot

class MAC_WmpMeasurementReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellId',TCellId),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC_WMP)),('measReportValue', aprot.bytes(size = MAX_NUM_MEAS_REPORT_VALUE_MAC_WMP))]
	
	