import aprot

class SRbUePacketId(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('rlcDataSendRespCause',ERlcDataSendRespCause),('ueId',TUeId),('radioBearerId',TRadioBearerId),('packetIdLow',TPacketId),('packetIdHigh',TPacketId)]
	
	