import aprot

class MAC_MeasTermResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportId',TMeasurementReportId),('messageResult',SMessageResult)]
	
	