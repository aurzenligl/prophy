import aprot

class MAC_StartUlCtrlChannelMeasReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measType',EUlCtrlChannelMeasType),('reportingTimeInterval',TReportingTimeInterval),('receptionSubframe',TSubframes),('expectionSubframe',TSubframes),('ulCtrlChannelParams',UUlCtrlChannelParams)]
	
	