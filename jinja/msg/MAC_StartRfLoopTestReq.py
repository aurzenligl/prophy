import aprot

class MAC_StartRfLoopTestReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('reportingTimeInterval',TReportingTimeInterval)]
	
	