import aprot

class MAC_MeasTermReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('reportId',TMeasurementReportId)]
	
	