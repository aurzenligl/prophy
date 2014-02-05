import aprot

class MAC_UlCtrlChannelMeasReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('resultStatus',EStatusLte),('UlCtrlChannelMeasCounters',SUlCtrlChannelMeasCounters),('container',UlCtrlChannelMeasReportContainer)]
	
	