import aprot

class MAC_MeasInitReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportClientSicad',TAaSysComSicad),('cellId',TCellId),('reportId',TMeasurementReportId),('period',TPeriod),('samplingPeriod',TPeriod),('groupList', aprot.bytes(size = 1))]
	
	