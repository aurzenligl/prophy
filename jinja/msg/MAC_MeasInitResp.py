import aprot

class MAC_MeasInitResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportId',TMeasurementReportId),('messageResult',SMessageResult)]
	
	