import aprot

class MAC_TestRlcDataInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('radioBearerId',TRadioBearerId),('size',TL3MsgSize),('data', aprot.bytes(size = 1))]
	
	