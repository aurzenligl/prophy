import aprot

class MAC_ThroughputMeasurementReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('resultStatus',EStatusLte),('throughputResult',TThroughputResult),('resultCounters',SResultCounters),('throughputResultStationaryUe',TThroughputResult),('resultCountersStationaryUe',SResultCounters)]
	
	