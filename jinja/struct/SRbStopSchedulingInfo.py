import aprot

class SRbStopSchedulingInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('dataForwardingType',EDataForwarding)]
	
	