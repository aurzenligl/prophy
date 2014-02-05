import aprot

class MAC_MeasReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportId',TMeasurementReportId),('measurementValues', aprot.bytes(size = 1))]
	
	